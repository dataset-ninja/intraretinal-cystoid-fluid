Dataset **Intraretinal Cystoid Fluid** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzE5NjlfSW50cmFyZXRpbmFsIEN5c3RvaWQgRmx1aWQvaW50cmFyZXRpbmFsLWN5c3RvaWQtZmx1aWQtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiRno5dytGYk9ZM21wRTZQVHhpbzU2SGMydmNxUU0vL0lpK3NpSjNpWG5aND0ifQ==)

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