import glob
import os
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import scipy.ndimage as ndimage
import supervisely as sly
from cv2 import connectedComponents
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "/mnt/d/datasetninja-raw/intraretinal-cystoid-fluid/2021-training-data-ZA/2021-training-data-ZA"

    ds_name = "ds"
    batch_size = 10

    images_folder_name = "images"
    masks_folder_name = "masks"

    def create_ann(image_path):
        labels = []

        mask_folder = image_path.split(images_folder_name)[0] + masks_folder_name
        mask_path = os.path.join(mask_folder, os.listdir(mask_folder)[0])

        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask_np = np.where(ndimage.binary_fill_holes(mask_np).astype("uint8") == 1, 255, 0)
            img_height = mask_np.shape[0]
            img_wight = mask_np.shape[1]
            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    obj_class = sly.ObjClass("cystic macular edema", sly.Bitmap)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class])
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(dataset_path + "/*/*/*.jpeg")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        anns_batch = [create_ann(image_path) for image_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        api.annotation.upload_anns(img_ids, anns_batch)

        progress.iters_done_report(len(img_names_batch))

    return project
