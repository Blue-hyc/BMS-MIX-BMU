from mix.lynx.launcher.launcher import *


class PreDefine(object):
    def __init__(self):
        json_file = load_json_file('/mix/addon/config/HYC_BMS.json')
        self._FW = json_file.get("FW Version")

    def FW(self):
        return self._FW
