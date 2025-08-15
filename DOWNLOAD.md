Dataset **Intraretinal Cystoid Fluid** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMTk2OV9JbnRyYXJldGluYWwgQ3lzdG9pZCBGbHVpZC9pbnRyYXJldGluYWwtY3lzdG9pZC1mbHVpZC1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJ5WlcvR1BNaERvTHVYVUU3R3pzNFFtbXhIaS9WelVWaUxTblNwN0cvUHRjPSJ9?response-content-disposition=attachment%3B%20filename%3D%22intraretinal-cystoid-fluid-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Intraretinal Cystoid Fluid', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/zeeshanahmed13/intraretinal-cystoid-fluid/download?datasetVersionNumber=3).