import glob
import os
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
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


def bucket_black_holes(mask):
    _, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=4)

    repaired_mask = np.copy(mask)

    for label in range(1, len(stats)):
        area = stats[label, cv2.CC_STAT_AREA]

        if area < 500:
            center_x = int(stats[label, cv2.CC_STAT_LEFT] + (stats[label, cv2.CC_STAT_WIDTH] / 2))
            center_y = int(stats[label, cv2.CC_STAT_TOP] + (stats[label, cv2.CC_STAT_HEIGHT] / 2))

            # Calculate the number of white pixels in a 3x3 neighborhood around the black hole
            surrounding_pixels = repaired_mask[
                center_y - 1 : center_y + 2, center_x - 1 : center_x + 2
            ]
            surrounding_white_pixels = np.sum(surrounding_pixels == 255)

            # Calculate the percentage of surrounding white pixels
            percentage_white = (surrounding_white_pixels / 9) * 100  # 9 pixels in total

            # Check if 50% or more of the surrounding pixels are white
            if percentage_white >= 50:
                # Add the black hole to the corresponding bucket
                # if label not in buckets:
                #     buckets[label] = []
                # buckets[label].append((center_x, center_y))

                # Repair the black hole by filling it with white (255)
                repaired_mask[labels == label] = 255

    return repaired_mask


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "/mnt/d/datasetninja-raw/intraretinal-cystoid-fluid/2021-training-data-ZA/2021-training-data-ZA"

    ds_name = "ds"
    batch_size = 30

    images_folder_name = "images"
    masks_folder_name = "masks"

    def create_ann(image_path):
        labels = []

        mask_folder = image_path.split(images_folder_name)[0] + masks_folder_name
        mask_path = os.path.join(mask_folder, os.listdir(mask_folder)[0])

        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask_np = bucket_black_holes(mask_np)
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
