Dataset **Intraretinal Cystoid Fluid** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/6/4/7y/zhNW0Uo1JjKBNIZCpvpHS0hWxJbApo5DTaWwN80HSuGMY97eRkVv9qZMGqxcQ9tVExCt5mq4MnBpyUmaXQT6TSfCmF5XYCWyIZQURyLFfAog89M8HmanrlM1Fx45.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Intraretinal Cystoid Fluid', dst_path='~/dtools/datasets/Intraretinal Cystoid Fluid.tar')
```
The data in original format can be 🔗[downloaded here](https://www.kaggle.com/datasets/zeeshanahmed13/intraretinal-cystoid-fluid/download?datasetVersionNumber=3)