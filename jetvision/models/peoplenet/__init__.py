# Here we do lazy loading of the model weights

import os

FILEPATH = os.path.abspath(__file__)
DIRPATH = os.path.dirname(FILEPATH)


class PeopleNet:
    DLA0 = DIRPATH + "/peoplenet_dla0.txt"
    DLA1 = DIRPATH + "/peoplenet_dla1.txt"
    GPU = DIRPATH + "/peoplenet_gpu.txt"

    @staticmethod
    def _download():
        # Lazy loading of peoplenet model
        MODEL_URL = "https://api.ngc.nvidia.com/v2/models/nvidia/tlt_peoplenet/versions/pruned_v2.0/zip"

        import urllib.request
        from zipfile import PyZipFile

        print("Downloading pretrained weights for the model. This may take a while...")
        urllib.request.urlretrieve(
            MODEL_URL, filename="/tmp/tlt_peoplenet_pruned_v2.0.zip"
        )
        # TODO: progressbar here would be nice. Keras has something like that:
        # https://github.com/keras-team/keras/blob/5550cb0c96c508211b1f0af4aa5af6caff7385a2/keras/utils/data_utils.py#L276

        pzf = PyZipFile("/tmp/tlt_peoplenet_pruned_v2.0.zip")
        pzf.extractall(path=DIRPATH + "/tlt_peoplenet_pruned_v2.0")


if not os.path.isfile(
    DIRPATH + "/tlt_peoplenet_pruned_v2.0/resnet18_peoplenet_int8_dla.txt"
):
    PeopleNet._download()
