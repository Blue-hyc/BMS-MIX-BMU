# -*- coding: utf-8 -*-
from ..ic.ad5560 import *
from ..ic.dac_base import *
import os
import time
from mix.driver.core.bus.pin import *
from mix.driver.core.ic.cat9555 import *

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class PSUBoardBaseDef:
    CS_CCO = 0x01
    CS_CC1 = 0x02
    CS_CC2 = 0x04
    CS_CC3 = 0x08

    CC_LIST = (
        CS_CCO,
        CS_CC1,
        CS_CC2,
        CS_CC3
    )

    RESET_PIN_ID = 4
    LOAD_PIN_ID = 5
    DAC_CLEAR_PIN_ID = 7

    I2C_CAT9555_ADDR = 0x20


class PSUBoardBase(object):
    compatible = []

    def __init__(self, i2c_ds, reference, inh_pin, ps_spi, dac):
        assert isinstance(dac, DACBase)
        self.cc = None
        self._clr_pin = None
        self._load_pin = None
        self._reset_pin = None
        self._ad5560 = AD5560(reference, ps_spi)
        self._dac = dac
        self._inh = inh_pin
        self.output(False)
        self._io = CAT9555(PSUBoardBaseDef.I2C_CAT9555_ADDR, i2c_ds)

    def pre_power_on_init(self):
        pass

    def post_power_on_init(self):
        self._reset_pin = Pin(self._io, PSUBoardBaseDef.RESET_PIN_ID, 'output')
        self.reset()
        self._load_pin = Pin(self._io, PSUBoardBaseDef.LOAD_PIN_ID, 'output')
        self._load_pin.set_level(0)
        self._clr_pin = Pin(self._io, PSUBoardBaseDef.DAC_CLEAR_PIN_ID, 'output')
        self._clr_pin.set_level(1)
        self.cc = []
        for i in range(4):
            self.cc.append(Pin(self._io, i, 'output'))
        self.cc_switch([[0, 1], [1, 1], [2, 1], [3, 1]])

    def fv(self, volt, clamp_current, current_range):
        raise NotImplementedError('Function not defined in subclass.')

    def fi(self, current, clamp_volt, current_range):
        raise NotImplementedError('Function not defined in subclass.')

    def restore(self, zero=True):
        raise NotImplementedError('Function not defined in subclass.')

    def range(self, current):
        raise NotImplementedError('Function not defined in subclass.')

    def output(self, enable=True):
        # self._ad5560.enable_hw_inh(not enable)
        level = 1 if enable else 0
        self._inh.set_level(level)

    def cc_switch(self, cc):
        '''
        PSU Base set CC capacity.

        Args:
             cc: ist of list,  [[cc_pin, 0/1], ...]
                                    0<= cc_pin < 3

        Examples:
             psu.cc_switch([[0, 1], [1, 0])

        '''
        assert isinstance(cc, list) and len(cc) <= 4
        for index in range(len(cc)):
            assert isinstance(cc[index], list) and len(cc[index]) == 2
            assert cc[index][0] in range(4)
            pin = cc[index][0]
            assert cc[index][1] in range(2)
            level = cc[index][1]
            self.cc[pin].set_level(level)

    def reset(self):
        self._reset_pin.set_level(1)
        time.sleep(0.01)
        self._reset_pin.set_level(0)
        time.sleep(0.01)
        self._reset_pin.set_level(1)

