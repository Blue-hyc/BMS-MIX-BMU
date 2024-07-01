# -*- coding: utf-8 -*-
from mix.driver.core.bus.i2c_bus_emulator import *
from mix.driver.core.bus.i2c import *
from ..bus.smbus import *
import time
import math

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class LTC7106Def:
    LTC7106_CMD_OPERATION = 0x01
    LTC7106_CMD_STATUS_BYTE = 0x78
    LTC7106_CMD_PMBUS_REVISION = 0x98
    LTC7106_CMD_MFR_CHIP_CTRL = 0xE2
    LTC7106_CMD_MFR_DAC_CTRL = 0xE4
    LTC7106_CMD_MFR_IOUT_MARGIN_HIGH = 0xE5
    LTC7106_CMD_MFR_IOUT_MAX = 0xE6
    LTC7106_CMD_MFR_SPECIAL_ID = 0xE7
    LTC7106_CMD_MFR_IOUT_COMMAND = 0xE8
    LTC7106_CMD_MFR_IOUT_MARGIN_LOW = 0xED
    LTC7106_CMD_MFR_RAIL_ADDRESS = 0xFA
    LTC7106_CMD_MFR_RESET = 0xFD

    CMD_List = [
        LTC7106_CMD_OPERATION,
        LTC7106_CMD_STATUS_BYTE,
        LTC7106_CMD_PMBUS_REVISION,
        LTC7106_CMD_MFR_CHIP_CTRL,
        LTC7106_CMD_MFR_DAC_CTRL,
        LTC7106_CMD_MFR_IOUT_MARGIN_HIGH,
        LTC7106_CMD_MFR_IOUT_MAX,
        LTC7106_CMD_MFR_SPECIAL_ID,
        LTC7106_CMD_MFR_IOUT_COMMAND,
        LTC7106_CMD_MFR_IOUT_MARGIN_LOW,
        LTC7106_CMD_MFR_RAIL_ADDRESS,
        LTC7106_CMD_MFR_RESET
    ]

    LTC7106_TIMEOUT_STATUS_OFFSET = 3
    LTC7106_TIMEOUT_STATUS_MASK = 1 << LTC7106_TIMEOUT_STATUS_OFFSET

    LTC7106_GPO_OFFSET = 0
    LTC7106_GPO_MASK = 1 << LTC7106_GPO_OFFSET

    LTC7106_STEP_OFFSET = 6
    LTC7106_STEP_0_P_25uA = 0 << LTC7106_STEP_OFFSET
    LTC7106_STEP_1uA = 1 << LTC7106_STEP_OFFSET
    LTC7106_STEP_4uA = 2 << LTC7106_STEP_OFFSET

    Output_Range = {
        LTC7106_STEP_0_P_25uA: {"MIN": -16.0, "MAX": 15.75},
        LTC7106_STEP_1uA: {"MIN": -64.0, "MAX": 63.0},
        LTC7106_STEP_4uA: {"MIN": -256.0, "MAX": 252.0}
    }

    LTC7106_OPERATION_ON = 0x80
    LTC7106_OPERATION_OFF = 0x00
    LTC7106_OPERATION_MARGIN_LOW = 0x98
    LTC7106_OPERATION_MARGIN_HIGH = 0xA8

    Operation_Type = [
        LTC7106_OPERATION_ON,
        LTC7106_OPERATION_OFF,
        LTC7106_OPERATION_MARGIN_LOW,
        LTC7106_OPERATION_MARGIN_HIGH
    ]

    LTC7106_WP_OFFSET = 2
    LTC7106_WP_MASK = 1 << LTC7106_WP_OFFSET


class LTC7106Exception(Exception):
    def __init__(self, dev_name, err_str):
        self._err_reason = '[%s]: %s.' % (dev_name, err_str)

    def __str__(self):
        return self._err_reason


class LTC7106(object):

    rpc_public_api = ['set_gpo', 'config_dac', 'reset', 'set_current', 'read_id', 'operation']

    def __init__(self, dev_addr, i2c_bus):
        self._dev_addr = dev_addr
        self._smbus = SMBus('LTC7106_emulator:'+str(self._dev_addr), i2c_bus)
        self.reset()
        time.sleep(0.5)
        self._range = LTC7106Def.Output_Range[LTC7106Def.LTC7106_STEP_1uA]

    def write_cmd(self, cmd):
        if self.wait_for_not_busy():
            self._smbus.send_byte(self._dev_addr, cmd)
        else:
            raise LTC7106Exception('', 'Device busy')

    def write_byte(self, cmd, byte):
        if self.wait_for_not_busy():
            self._smbus.write_byte(self._dev_addr, cmd, byte)
        else:
            raise LTC7106Exception('', 'Device busy')

    def write_word(self, cmd, word):
        if self.wait_for_not_busy():
            self._smbus.write_word(self._dev_addr, cmd, word)
        else:
            raise LTC7106Exception('', 'Device busy')

    def read_byte(self, cmd):
        if self.wait_for_not_busy():
            return self._smbus.read_byte(self._dev_addr, cmd)[0]
        else:
            raise LTC7106Exception('', 'Device busy')

    def read_word(self, cmd):
        if self.wait_for_not_busy():
            return self._smbus.read_word(self._dev_addr, cmd)
        else:
            raise LTC7106Exception('', 'Device busy')

    def read_block(self, cmd, count):
        if self.wait_for_not_busy():
            return self._smbus.read_block(self._dev_addr, cmd, count)
        else:
            raise LTC7106Exception('', 'Device busy')

    def wait_for_not_busy(self):
        timeout = 3
        while timeout > 0:
            timeout -= 1
            mfr_common = self._smbus.read_byte(self._dev_addr, LTC7106Def.LTC7106_CMD_MFR_CHIP_CTRL)[0]
            # pmbus is not ready
            if mfr_common & LTC7106Def.LTC7106_TIMEOUT_STATUS_MASK:
                mfr_common |= LTC7106Def.LTC7106_TIMEOUT_STATUS_MASK
                self._smbus.write_byte(self._dev_addr, LTC7106Def.LTC7106_CMD_MFR_CHIP_CTRL, mfr_common)
                time.sleep(0.1)
                continue
            else:
                return True
        return False

    def set_gpo(self, level):
        assert level in (0, 1)
        mfr = self.read_byte(LTC7106Def.LTC7106_CMD_MFR_CHIP_CTRL)
        if (mfr & LTC7106Def.LTC7106_GPO_MASK) != (level << LTC7106Def.LTC7106_GPO_OFFSET):
            mfr &= ~LTC7106Def.LTC7106_GPO_MASK
            mfr |= level << LTC7106Def.LTC7106_GPO_OFFSET
            self.write_byte(LTC7106Def.LTC7106_CMD_MFR_CHIP_CTRL, mfr)

    def config_dac(self, step, time_up):
        assert step in LTC7106Def.Output_Range
        assert time_up in range(0, 0x2F)
        dac_ctrl = step | time_up & 0xFF
        self.write_byte(LTC7106Def.LTC7106_CMD_MFR_DAC_CTRL, dac_ctrl)

    def reset(self):
        self.write_cmd(LTC7106Def.LTC7106_CMD_MFR_RESET)

    def set_current(self, value):
        assert self._range["MIN"] <= value <= self._range["MAX"]
        _max = self._range["MAX"]
        _min = self._range["MIN"]
        self.operation(LTC7106Def.LTC7106_OPERATION_OFF)
        self.write_protect(False)
        if value >= 0.0:
            dac = int(round(value*1.0/_max*0x3F)) & 0x3F
        else:
            dac = 0x80 - int(round(value*1.0/_min * 0x3F))
            self.write_byte(LTC7106Def.LTC7106_CMD_MFR_IOUT_MAX, 0x40)
        self.write_byte(LTC7106Def.LTC7106_CMD_MFR_IOUT_COMMAND, dac)
        self.write_protect(True)
        self.operation(LTC7106Def.LTC7106_OPERATION_ON)

    def read_id(self):
        return self.read_word(LTC7106Def.LTC7106_CMD_MFR_SPECIAL_ID)

    def operation(self, op):
        assert op in LTC7106Def.Operation_Type
        self.write_byte(LTC7106Def.LTC7106_CMD_OPERATION, op)

    def write_protect(self, enable=True):
        assert enable in (True, False)
        mfr = self.read_byte(LTC7106Def.LTC7106_CMD_MFR_CHIP_CTRL)
        act = 1 if enable else 0
        act <<= LTC7106Def.LTC7106_WP_OFFSET
        if (mfr & LTC7106Def.LTC7106_WP_MASK) != act:
            mfr &= ~LTC7106Def.LTC7106_WP_MASK
            mfr |= act
            self.write_byte(LTC7106Def.LTC7106_CMD_MFR_CHIP_CTRL, act)



