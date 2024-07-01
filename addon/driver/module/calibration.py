# -*- coding: utf-8 -*-
from ..ic.sst26vf064b import *
import ctypes
import logging
import struct
from mix.addon.driver.module.psu2_board import PSU2BoardDef
from mix.addon.driver.module.psu1_board import PSU1BoardDef
import time
import pdb


def float2hex(f):
    # 可以解码，但如何修改内存呢？
    a = struct.unpack('<I', struct.pack('<f', f))[0]
    raw = [a & 0xff, (a & 0xff00) >> 8, (a & 0xff0000) >> 16, (a & 0xff000000) >> 24]
    return raw


def hex2float(h):
    h = str(h)
    i = int(h, 10)
    return struct.unpack('<f', struct.pack('<I', i))[0]


class CalStruct:
    def __init__(self, raw):
        assert isinstance(raw, list) and len(raw) == 94
        # for i in raw:
        #     assert isinstance(i, int) and 0 <= i <= 255
        # print raw
        self.CalibrationType = raw[0]
        self.PsChannel = raw[1]
        self.AD5560Ch = raw[2]
        self.CurrentRange = raw[3]
        self.flag = raw[4]
        self.force_flag = raw[5]
        self.measure_flag = raw[6]
        self.pos_neg_flag = raw[7]
        self.version_h = raw[8]
        self.version_l = raw[9]
        self.force_K = []
        for i in range(8):
            hex_val = raw[10 + 4 * i] | (raw[11 + 4 * i] << 8) | (raw[12 + 4 * i] << 16) | (raw[13 + 4 * i] << 24)
            self.force_K.append(hex2float(hex_val))
        self.force_B = hex2float(raw[42] | (raw[43] << 8) | (raw[44] << 16) | (raw[45] << 24))
        self.measure_K = []
        for i in range(8):
            hex_val = raw[46 + 4 * i] | (raw[47 + 4 * i] << 8) | (raw[48 + 4 * i] << 16) | (raw[49 + 4 * i] << 24)
            self.measure_K.append(hex2float(hex_val))
        self.measure_B = []
        for i in range(2):
            hex_val = raw[78 + 4 * i] | (raw[79 + 4 * i] << 8) | (raw[80 + 4 * i] << 16) | (raw[81 + 4 * i] << 24)
            self.measure_B.append(hex2float(hex_val))
        self.reserve = [0.0, 0.0]


class CalibrationDef:
    BOARD_ID_START_BLOCK = 0
    BOARD_ID_START_PAGE = 0

    CALIBRATION_START_BLOCK = 5
    CALIBRATION_START_PAGE = 256

    CAL_V_TYPE_MAX = 1
    CAL_I_TYPE_MAX = 6

    # pos&neg * psu * ad5560ch * current_range *
    CAL_VOLTAGE_NUM = 2 * 2 * 1 * 8 * CAL_V_TYPE_MAX
    CAL_CURRENT_NUM = 2 * 2 * 1 * 8 * CAL_I_TYPE_MAX
    CAL_INFO_TOTAL_NUM = CAL_VOLTAGE_NUM + CAL_CURRENT_NUM

    CAL_TYPE_NONE = 0
    CAL_TYPE_FV = 1
    CAL_TYPE_FI = 2

    CAL_CURRENT_RANGE_MAX = 8


class Calibration(object):
    instance = None

    def __new__(cls, spi_s1, spi_s0, spi_bus=None):
        if cls.instance is None:
            cls.instance = _Calibration(spi_s1, spi_s0, spi_bus)
        return cls.instance


def cal_sector(cal_type, psu, ad5560ch, ex_type, current_range, pos_neg_flag):
    if cal_type == CalibrationDef.CAL_TYPE_FV:
        index = ex_type + current_range * CalibrationDef.CAL_V_TYPE_MAX + \
                ad5560ch * (CalibrationDef.CAL_CURRENT_RANGE_MAX * CalibrationDef.CAL_V_TYPE_MAX) + \
                psu * (1 * CalibrationDef.CAL_CURRENT_RANGE_MAX * CalibrationDef.CAL_V_TYPE_MAX) + \
                pos_neg_flag * (2 * 1 * CalibrationDef.CAL_CURRENT_RANGE_MAX * CalibrationDef.CAL_V_TYPE_MAX)
    elif cal_type == CalibrationDef.CAL_TYPE_FI:
        index = ex_type + current_range * CalibrationDef.CAL_I_TYPE_MAX + \
                ad5560ch * (CalibrationDef.CAL_CURRENT_RANGE_MAX * CalibrationDef.CAL_I_TYPE_MAX) + \
                psu * (1 * CalibrationDef.CAL_CURRENT_RANGE_MAX * CalibrationDef.CAL_I_TYPE_MAX) + \
                pos_neg_flag * (2 * 1 * CalibrationDef.CAL_CURRENT_RANGE_MAX * CalibrationDef.CAL_I_TYPE_MAX) + \
                CalibrationDef.CAL_VOLTAGE_NUM
    else:
        index = -1
    return index


class _Calibration(object):
    def __init__(self, spi_s1, spi_s0, spi_bus=None):
        self._spi_ss = [spi_s1, spi_s0]
        self._spi_ss[0].set_level(1)
        self._spi_ss[1].set_level(0)
        time.sleep(0.1)
        self._spi_bus = spi_bus
        self._flash = SST26VF064B(spi_bus)
        self.gCalInfo = []
        for i in range(CalibrationDef.CAL_INFO_TOTAL_NUM):
            raw = self.read_flash(i)
            self.gCalInfo.append(raw)

    def cal_fv(self, psu, current_range, volt):
        pos_neg_flag = 0 if volt >= 0 else 1
        index = cal_sector(CalibrationDef.CAL_TYPE_FV, psu, 0, 0, current_range, pos_neg_flag)
        cal = CalStruct(self.gCalInfo[index])
        if cal.CalibrationType != CalibrationDef.CAL_TYPE_FV:
            return volt
        cal_volt = (volt - cal.force_B) / cal.force_K[0]
        return cal_volt

    def cal_fi(self, psu, current_range, current):
        pos_neg_flag = 0 if current >= 0 else 1
        ext_type = 0
        if psu == 1:
            if current_range == PSU2BoardDef.CURRENT_RANGE_1A:
                tmp = abs(current)
                if tmp < 0.03:
                    ext_type = 0
                elif 0.03 <= tmp < 0.25:
                    ext_type = 1
                elif 0.25 <= tmp < 0.75:
                    ext_type = 2
                elif 0.75 <= tmp < 1.0:
                    ext_type = 3
            if current_range == PSU2BoardDef.CURRENT_RANGE_4A:
                tmp = abs(current)
                if tmp < 0.8:
                    ext_type = 0
                elif 0.8 <= tmp < 1.5:
                    ext_type = 1
                elif 1.5 <= tmp < 4.0:
                    ext_type = 2
        index = cal_sector(CalibrationDef.CAL_TYPE_FI, psu, 0, ext_type, current_range, pos_neg_flag)
        # print 'from gCalInfo', self.gCalInfo[index]
        cal = CalStruct(self.gCalInfo[index])
        if cal.CalibrationType != CalibrationDef.CAL_TYPE_FI:
            return current
        cal_current = (current - cal.force_B) / cal.force_K[0]
        return cal_current

    def cal_mv(self, psu, current_range, volt):
        pos_neg_flag = 0 if volt >= 0 else 1
        index = cal_sector(CalibrationDef.CAL_TYPE_FV, psu, 0, 0, current_range, pos_neg_flag)
        cal = CalStruct(self.gCalInfo[index])
        if cal.CalibrationType != CalibrationDef.CAL_TYPE_FV:
            return volt
        linear_volt = cal.measure_K[7] * volt + cal.measure_B[1]
        if current_range == 5:
            return linear_volt
        cal_volt = 0.0
        for i in range(cal.measure_flag):
            cal_volt += cal.measure_K[cal.measure_flag - 1 - i] * pow(linear_volt, cal.measure_flag - i)
        cal_volt += cal.measure_B[0]
        return cal_volt

    def cal_mi(self, psu, current_range, current):
        pos_neg_flag = 0 if current >= 0 else 1
        ext_type = 0
        if psu == 1:
            if current_range == PSU2BoardDef.CURRENT_RANGE_1A:
                tmp = abs(current)
                if tmp < 0.03:
                    ext_type = 0
                elif 0.03 <= tmp < 0.25:
                    ext_type = 1
                elif 0.25 <= tmp < 0.75:
                    ext_type = 2
                elif 0.75 <= tmp < 1.0:
                    ext_type = 3
            if current_range == PSU2BoardDef.CURRENT_RANGE_4A:
                tmp = abs(current)
                if tmp < 0.8:
                    ext_type = 0
                elif 0.8 <= tmp < 1.5:
                    ext_type = 1
                elif 1.5 <= tmp < 4.0:
                    ext_type = 2
        if current_range == PSU1BoardDef.CURRENT_RANGE_25mA:
            index = cal_sector(CalibrationDef.CAL_TYPE_FI, psu, 0, ext_type, current_range, 0)
        else:
            index = cal_sector(CalibrationDef.CAL_TYPE_FI, psu, 0, ext_type, current_range, pos_neg_flag)
        cal = CalStruct(self.gCalInfo[index])
        if cal.CalibrationType != CalibrationDef.CAL_TYPE_FI:
            return current
        if cal.measure_K[7] == 0:
            return current
        linear_current = cal.measure_K[7] * current + cal.measure_B[1]
        # print linear_current, '=', cal.measure_K[7], '*', current, '+', cal.measure_B[1]
        if current_range == PSU1BoardDef.CURRENT_RANGE_25mA:
            return linear_current
        if current_range == PSU1BoardDef.CURRENT_RANGE_2_5mA:
            return linear_current
        # return linear_current
        if psu == 0:
            return linear_current
        if psu == 1 and current_range == PSU2BoardDef.CURRENT_RANGE_10A:
            return linear_current
        if psu == 1 and current_range == PSU2BoardDef.CURRENT_RANGE_2_5mA:
            return linear_current
        if cal.measure_K[cal.measure_flag - 1] == 0:
            return current
        cal_current = 0.0
        for i in range(cal.measure_flag):
            cal_current += cal.measure_K[cal.measure_flag - 1 - i] * pow(linear_current, cal.measure_flag - i)
            # print cal.measure_K[cal.measure_flag - 1 - i], '*', linear_current, '^', cal.measure_flag - i, '+'
        cal_current += cal.measure_B[0]
        # print cal.measure_B[0], '=', cal_current
        # raise Exception('')
        return cal_current

    def write(self, data):
        if len(data) != 94:
            return -1
        cal_str = CalStruct(data)
        if cal_str.PsChannel > 1:
            return -1
        if cal_str.AD5560Ch > 0:
            return -1
        index = cal_sector(cal_str.CalibrationType, cal_str.PsChannel, cal_str.AD5560Ch, cal_str.flag,
                           cal_str.CurrentRange, cal_str.pos_neg_flag)
        tmp = self.gCalInfo
        self.gCalInfo[index] = data
        if -1 == self.write_flash():
            self.gCalInfo = tmp
            return -1
        return 0

    def read(self, data):
        cal_str = CalStruct(data)
        index = cal_sector(cal_str.CalibrationType, cal_str.PsChannel, cal_str.AD5560Ch, cal_str.flag,
                           cal_str.CurrentRange, cal_str.pos_neg_flag)
        return self.gCalInfo[index]

    def write_flash(self):
        self._spi_ss[0].set_level(1)
        self._spi_ss[1].set_level(0)
        time.sleep(0.1)
        self._flash.erase_block(CalibrationDef.CALIBRATION_START_BLOCK)
        page = 94 * CalibrationDef.CAL_INFO_TOTAL_NUM / 256
        remain = 94 * CalibrationDef.CAL_INFO_TOTAL_NUM % 256
        tmp = []
        for i in self.gCalInfo:
            tmp.extend(i)
        for i in range(page):
            if -1 == self._flash.page_program(CalibrationDef.CALIBRATION_START_PAGE + i, 0, tmp[256 * i:256 * i + 256]):
                return -1
        if remain:
            if -1 == self._flash.page_program(CalibrationDef.CALIBRATION_START_PAGE + page, 0,
                                     tmp[256 * page:256 * page + remain]):
                return -1
        return 0

    def read_flash(self, sector):
        addr = SST26VF064BDef.BlockAddr[CalibrationDef.CALIBRATION_START_BLOCK] + sector * 94
        self._spi_ss[0].set_level(1)
        self._spi_ss[1].set_level(0)
        time.sleep(0.1)
        return self._flash.read_flash(addr, 94)

    def read_board_id(self, is_str=True):
        self._spi_ss[0].set_level(1)
        self._spi_ss[1].set_level(0)
        time.sleep(0.1)
        rd = self._flash.read_flash(SST26VF064BDef.BlockAddr[CalibrationDef.BOARD_ID_START_BLOCK], 16)
        try:
            board_id = bytearray(rd[0:6]).decode('ascii')
            if not board_id.isalnum():
                board_id = 'V00000'
        except Exception as e:
            board_id = 'V00000'
        if not is_str:
            tmp = list(board_id)
            board_id = list(struct.unpack('%dB' % len(tmp), board_id))
        return board_id

    def write_board_id(self, board_id):
        self._spi_ss[0].set_level(1)
        self._spi_ss[1].set_level(0)
        time.sleep(0.1)
        self._flash.erase_sector(0)
        self._flash.page_program(SST26VF064BDef.BlockAddr[CalibrationDef.BOARD_ID_START_BLOCK], 0, board_id)
