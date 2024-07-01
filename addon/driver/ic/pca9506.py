# -*- coding: utf-8 -*-
# from driver.bus.pl_i2c_emulator_plugin import *
from mix.driver.core.bus.i2c_bus_emulator import *
from mix.driver.core.bus.i2c import *
from mix.driver.core.ic.io_expander_base import IOExpanderBase
import time
from mix.driver.core.bus.gpio import *

__author__ = 'wanghong@hyc.cn'
__version__ = '0.1'


class PCA9506Def:
    PCA9506_REG_IP0 = 0x00
    PCA9506_REG_IP1 = 0x01
    PCA9506_REG_IP2 = 0x02
    PCA9506_REG_IP3 = 0x03
    PCA9506_REG_IP4 = 0x04
    PCA9506_REG_OP0 = 0x08
    PCA9506_REG_OP1 = 0x09
    PCA9506_REG_OP2 = 0x0A
    PCA9506_REG_OP3 = 0x0B
    PCA9506_REG_OP4 = 0x0C
    PCA9506_REG_PI0 = 0x10
    PCA9506_REG_PI1 = 0x11
    PCA9506_REG_PI2 = 0x12
    PCA9506_REG_PI3 = 0x13
    PCA9506_REG_PI4 = 0x14
    PCA9506_REG_IOC0 = 0x18
    PCA9506_REG_IOC1 = 0x19
    PCA9506_REG_IOC2 = 0x1A
    PCA9506_REG_IOC3 = 0x1B
    PCA9506_REG_IOC4 = 0x1C
    PCA9506_REG_MSK0 = 0x20
    PCA9506_REG_MSK1 = 0x21
    PCA9506_REG_MSK2 = 0x22
    PCA9506_REG_MSK3 = 0x23
    PCA9506_REG_MSK4 = 0x24

    REGISTERS = [
        PCA9506_REG_IP0,
        PCA9506_REG_IP1,
        PCA9506_REG_IP2,
        PCA9506_REG_IP3,
        PCA9506_REG_IP4,
        PCA9506_REG_OP0,
        PCA9506_REG_OP1,
        PCA9506_REG_OP2,
        PCA9506_REG_OP3,
        PCA9506_REG_OP4,
        PCA9506_REG_PI0,
        PCA9506_REG_PI1,
        PCA9506_REG_PI2,
        PCA9506_REG_PI3,
        PCA9506_REG_PI4,
        PCA9506_REG_IOC0,
        PCA9506_REG_IOC1,
        PCA9506_REG_IOC2,
        PCA9506_REG_IOC3,
        PCA9506_REG_IOC4,
        PCA9506_REG_MSK0,
        PCA9506_REG_MSK1,
        PCA9506_REG_MSK2,
        PCA9506_REG_MSK3,
        PCA9506_REG_MSK4
    ]

    PCA9506_IOC_REGISTERS = [
        PCA9506_REG_IOC0,
        PCA9506_REG_IOC1,
        PCA9506_REG_IOC2,
        PCA9506_REG_IOC3,
        PCA9506_REG_IOC4
    ]

    PCA9506_OP_REGISTERS = [
        PCA9506_REG_OP0,
        PCA9506_REG_OP1,
        PCA9506_REG_OP2,
        PCA9506_REG_OP3,
        PCA9506_REG_OP4,
    ]

    PCA9506_CMD_AI_ENABLE = 0x80

    PIN_MIN_NUM = 0
    PIN_MAX_NUM = 39

    PCA9506_PORT_0 = 0
    PCA9506_PORT_1 = 1
    PCA9506_PORT_2 = 2
    PCA9506_PORT_3 = 3
    PCA9506_PORT_4 = 4

    Port_Type = [
        PCA9506_PORT_0,
        PCA9506_PORT_1,
        PCA9506_PORT_2,
        PCA9506_PORT_3,
        PCA9506_PORT_4
    ]

    PCA9506_PIN_DIR_OUTPUT = 0
    PCA9506_PIN_DIR_INPUT = 1

    Dir_Type = {
        'input': 1,
        'output': 0
    }


class PCA9506Exception(Exception):
    def __init__(self, err_str):
        self.err_reason = '%s.' % (err_str)

    def __str__(self):
        return self.err_reason


class PCA9506(IOExpanderBase):
    '''
    PCA9506 function class

    ClassType = PCA9506

    Args:
        dev_addr: hexmial,  I2C device address of PCA9506.
        i2c_bus:  instance(I2C)/None, Class instance of I2C bus,
                                      If not using the parameter
                                      will create Emulator

    Examples:
        i2c = I2C('/dev/i2c-2')
        pca9506 = PCA9506(0x20, i2c)

    '''
    rpc_public_api = ['set_pin_dir', 'get_pin_dir', 'set_pin', 'get_pin']

    def __init__(self, rst, dev_addr, i2c_bus=None):
        # 7-bit address, excluding read/write bits, lower two bits are variable
        assert dev_addr in range(0x20, 0x28)
        if rst is not None:
            rst.set_level(0)
            time.sleep(0.1)
            rst.set_level(1)
        self.__dev_addr = dev_addr
        self.i2c_bus = i2c_bus
        super(PCA9506, self).__init__()
        if rst is not None:
            self.set_pin_dir(2, 'output')
            self.set_pin(2, 1)
            self.set_pin_dir(5, 'output')
            self.set_pin(5, 1)
            self.set_pin_dir(7, 'output')
            self.set_pin(7, 1)

    def read_register(self, reg, length=1):
        assert isinstance(reg, int) and reg in PCA9506Def.REGISTERS
        assert isinstance(length, int) and 0 < length < 5
        data = [reg]
        if length > 1:
            data[0] |= 0x80
        rd = self.i2c_bus.write_and_read(self.__dev_addr, data, length)
        if length > 1:
            return rd
        else:
            return rd[0]

    def write_register(self, reg, content):
        assert reg in PCA9506Def.REGISTERS
        assert (isinstance(content, int) and 0 <= content <= 0xFF) or \
               (isinstance(content, list) and 1 < len(content) <= 5)
        data = [reg]
        if isinstance(content, list) and 1 < len(content) <= 5:
            data[0] |= 0x80
            data.extend(content)
        else:
            data.append(content)
        self.i2c_bus.write(self.__dev_addr, data)
        time.sleep(0.001)

    def set_pin_dir(self, pin_id, direction):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 39
        assert direction in PCA9506Def.Dir_Type
        port = pin_id / 8
        pin = pin_id % 8
        rd = self.read_register(PCA9506Def.PCA9506_IOC_REGISTERS[port], 1)
        rd &= ~(1 << pin)
        rd |= PCA9506Def.Dir_Type[direction] << pin
        self.write_register(PCA9506Def.PCA9506_IOC_REGISTERS[port], rd)

    def get_pin_dir(self, pin_id):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 39
        port = pin_id / 8
        pin = pin_id % 8
        rd = self.read_register(PCA9506Def.PCA9506_IOC_REGISTERS[port], 1)
        if rd & (1 << pin):
            return 'input'
        return 'output'

    def set_pin(self, pin_id, level):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 39
        assert level in (0, 1)
        # print[pin_id, level]
        port = pin_id / 8
        pin = pin_id % 8
        rd = self.read_register(PCA9506Def.PCA9506_OP_REGISTERS[port], 1)
        if (rd & (1 << pin)) != (level << pin):
            rd &= ~(1 << pin)
            rd |= level << pin
            self.write_register(PCA9506Def.PCA9506_OP_REGISTERS[port], rd)

    def get_pin(self, pin_id):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 39
        port = pin_id / 8
        pin = pin_id % 8
        rd = self.read_register(PCA9506Def.PCA9506_OP_REGISTERS[port], 1)
        if rd & (1 << pin):
            return 1
        return 0
