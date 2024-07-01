# -*- coding: utf-8 -*-
from mix.driver.core.bus.i2c_bus_emulator import I2CBusEmulator
from mix.driver.core.bus.i2c import I2C


class DS2482Def:
    STATUS = 0xF0
    READ_DATA = 0xE1
    CONFIGURATION = 0xC3

    REGISTERS = [
        STATUS,
        READ_DATA,
        CONFIGURATION
    ]

    ADDR_LIST = [0x18, 0x19, 0x1A, 0x1B]


class DS2482(object):
    def __init__(self, dev_addr, i2c_bus=None):
        assert dev_addr in DS2482Def.ADDR_LIST
        if i2c_bus:
            self.i2c_bus = i2c_bus
        else:
            self.i2c_bus = I2CBusEmulator('ds2482_emulator', 256)
        self.__dev_addr = dev_addr



