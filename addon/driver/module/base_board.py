# -*- coding: utf-8 -*-
from ..ic.tmp117 import TMP117

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class BaseBoard(object):

    rpc_public_api = ['read_temperature']

    def __init__(self, i2c_bus):
        self._tmp117 = TMP117(0x48, i2c_bus)

    def read_temperature(self):
        return self._tmp117.read_temperature()


