# -*- coding: utf-8 -*-

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class DACBase(object):
    '''
    Base Class for all DAC like AD5761&AD5791
    '''
    def __init__(self):
        return

    def set_voltage(self, volt):
        raise NotImplementedError('Function not defined in Driver IC.')
