# -*- coding: utf-8 -*-
from mix.driver.core.bus.i2c_bus_emulator import *
from mix.driver.core.bus.pin import Pin
import math
import os
import time


__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class TMP117Exception(Exception):
    def __init__(self, err_str):
        self.err_reason = 'TMP117: %s.' % err_str

    def __str__(self):
        return self.err_reason


class TMP117Def:
    Device_Addr_List = [
        0x48,  # ground
        0x49,  # v+
        0x4A,  # sda
        0x4B  # scl
    ]

    TMP117_REG_TEMP_RESULT = 0x00
    TMP117_REG_CONFIGURATION = 0x01
    TMP117_REG_THIGH_LIMIT = 0x02
    TMP117_REG_TLOW_LIMIT = 0x03
    TMP117_REG_EEPROM_UL = 0x04
    TMP117_REG_EEPROM1 = 0x05
    TMP117_REG_EEPROM2 = 0x06
    TMP117_REG_TEMP_OFFSET = 0x07
    TMP117_REG_EEPROM3 = 0x08
    TMP117_REG_DEVICE_ID = 0x0F

    REGISTERS = [
        TMP117_REG_TEMP_RESULT,
        TMP117_REG_CONFIGURATION,
        TMP117_REG_THIGH_LIMIT,
        TMP117_REG_TLOW_LIMIT,
        TMP117_REG_EEPROM_UL,
        TMP117_REG_EEPROM1,
        TMP117_REG_EEPROM2,
        TMP117_REG_TEMP_OFFSET,
        TMP117_REG_EEPROM3,
        TMP117_REG_DEVICE_ID
    ]

    TMP117_MOD_OFFSET = 10
    TMP117_MOD_MASK = 3 << TMP117_MOD_OFFSET

    TMP117_MOD_CONTINUOUS = 0 << TMP117_MOD_OFFSET
    TMP117_MOD_SHUTDOWN = 1 << TMP117_MOD_OFFSET
    TMP117_MOD_ONE_SHOT = 3 << TMP117_MOD_OFFSET

    Mode_Type = [
        TMP117_MOD_CONTINUOUS,
        TMP117_MOD_SHUTDOWN,
        TMP117_MOD_ONE_SHOT
    ]

    TMP117_CONV_OFFSET = 7
    TMP117_CONV_MASK = 7 << TMP117_CONV_OFFSET

    TMP117_AVG_OFFSET = 5
    TMP117_AVG_MASK = 3 << TMP117_AVG_OFFSET

    TMP117_AVG_NONE = 0 << TMP117_AVG_OFFSET
    TMP117_AVG_8 = 1 << TMP117_AVG_OFFSET
    TMP117_AVG_32 = 2 << TMP117_AVG_OFFSET
    TMP117_AVG_64 = 3 << TMP117_AVG_OFFSET

    AVG_Type = {
        'None': TMP117_AVG_NONE,
        'AVG_8': TMP117_AVG_8,
        'AVG_32': TMP117_AVG_32,
        'AVG_64': TMP117_AVG_64
    }

    TMP117_DATA_READY_OFFSET = 13
    TMP117_DATA_READY_MASK = 1 << TMP117_DATA_READY_OFFSET


class TMP117(object):
    '''
    The TMP117 class.

    Args:
    dev_addr:    hexmial,        I2C device address.
    i2c_bus:     instance(I2C)/None,  instance of I2C bus, if not using this parameter,
                                      will create Emulator.

    Examples:
        i2c = I2C('/dev/i2c_0')
        tmp117  = TMP117(0x48, i2c)
    '''
    rpc_public_api = ['write_register', 'read_register', 'reset', 'get_id', 'read_temperature']

    def __init__(self, dev_addr, i2c_bus=None):
        assert dev_addr in TMP117Def.Device_Addr_List
        if i2c_bus is None:
            self._i2c_bus = I2CBusEmulator('TMP117_emulator', 256)
        else:
            self._i2c_bus = i2c_bus
        self._dev_addr = dev_addr

    def write_register(self, reg, content):
        '''
        TMP117 write register.

        Args:
            reg:     instance(int), in TMP117Def.REGISTERS.
            content: instance(int), data to be sent.

        Examples:
            tmp.write_register(TMP117Def.TMP117_REG_EEPROM1, 0x10)

        '''
        assert isinstance(reg, int) and reg in TMP117Def.REGISTERS
        assert isinstance(content, int)
        data = [reg, (content & 0xFF00) >> 8, content & 0x00FF]
        self._i2c_bus.write(self._dev_addr, data)

    def read_register(self, reg):
        '''
        TMP117 read register.

        Args:
            reg:   instance(int), in TMP117Def.REGISTERS.

        Examples:
            print tmp.read_register(TMP117Def.TMP117_REG_EEPROM1)

        '''
        assert isinstance(reg, int) and reg in TMP117Def.REGISTERS
        rd = self._i2c_bus.write_and_read(self._dev_addr, [reg], 2)
        return ((rd[0] << 8) | rd[1]) & 0xFFFF

    def reset(self):
        '''
        TMP117 reset.

        Examples:
            tmp117.reset()

        '''
        ctl = self.read_register(TMP117Def.TMP117_REG_CONFIGURATION)
        ctl |= 0x0002
        self.write_register(TMP117Def.TMP117_REG_CONFIGURATION, ctl)

    def read_temperature(self):
        '''
        TMP117 read temperature in specific average mode.

        Examples:
            print tmp.read_temperature()

        '''
        ctl = self.read_register(TMP117Def.TMP117_REG_CONFIGURATION)
        ctl &= ~TMP117Def.TMP117_MOD_MASK
        ctl |= TMP117Def.TMP117_MOD_ONE_SHOT
        ctl &= ~TMP117Def.TMP117_AVG_MASK
        ctl |= TMP117Def.AVG_Type['None']
        self.write_register(TMP117Def.TMP117_REG_CONFIGURATION, ctl)
        time.sleep(0.016)
        retry = 0
        while retry < 3:
            ctl = self.read_register(TMP117Def.TMP117_REG_CONFIGURATION)
            if ctl & TMP117Def.TMP117_DATA_READY_MASK:
                raw = self.read_register(TMP117Def.TMP117_REG_TEMP_RESULT)
                if raw < 0x8000:
                    result = 1.0 * raw / 0x8000 * 256.0
                else:
                    result = -1.0 * (0x10000 - raw) / 0x8000 * 256.0
                return result
            retry += 1
            time.sleep(0.1)
        raise TMP117Exception('read temperature fail')

