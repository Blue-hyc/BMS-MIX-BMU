# -*- coding: utf-8 -*-
import time

from mix.driver.hyc.common.ipcore.mix_ads8900_hyc import MIXADS8900HYC, MIXADS8900HYCDef
from mix.driver.hyc.common.ipcore.mix_ads8900_hyc_emulator import MIXADS8900HYCEmulator

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class ADS8900Def:
    ADS8900_REG_OFFSET = 8

    ADS8900_REG_PD_CNTL = 0x004
    ADS8900_REG_SDI_CNTL = 0x008
    ADS8900_REG_SDO_CNTL = 0x00C
    ADS8900_REG_DATA_CNTL = 0x010
    ADS8900_REG_PATN_LSB = 0x014
    ADS8900_REG_PATN_MID = 0x015
    ADS8900_REG_PATN_MSB = 0x016
    ADS8900_REG_OFST_CAL = 0x020
    ADS8900_REG_REF_MRG = 0x030

    REGISTERS = [
        ADS8900_REG_PD_CNTL,
        ADS8900_REG_SDI_CNTL,
        ADS8900_REG_SDO_CNTL,
        ADS8900_REG_DATA_CNTL,
        ADS8900_REG_PATN_LSB,
        ADS8900_REG_PATN_MID,
        ADS8900_REG_PATN_MSB,
        ADS8900_REG_OFST_CAL,
        ADS8900_REG_REF_MRG
    ]

    ADS8900_CMD_OFFSET = 17

    ADS8900_CMD_NOP = 0x00
    ADS8900_CMD_CLR_BITS = 0x10
    ADS8900_CMD_RD_REG = 0x11
    ADS8900_CMD_WR_REG = 0x12
    ADS8900_CMD_SET_BITS = 0x13

    CMD_Type = [
        ADS8900_CMD_NOP,
        ADS8900_CMD_CLR_BITS,
        ADS8900_CMD_RD_REG,
        ADS8900_CMD_WR_REG,
        ADS8900_CMD_SET_BITS
    ]

    ADS8900_SDI_MODE_OFFSET = 0
    ADS8900_SDI_MODE_MASK = 3 << ADS8900_SDI_MODE_OFFSET

    ADS8900_SDI_MODE_0 = 0
    ADS8900_SDI_MODE_1 = 1
    ADS8900_SDI_MODE_2 = 2
    ADS8900_SDI_MODE_3 = 3

    SDI_Type = {
        'MODE0': ADS8900_SDI_MODE_0,
        'MODE1': ADS8900_SDI_MODE_1,
        'MODE2': ADS8900_SDI_MODE_2,
        'MODE3': ADS8900_SDI_MODE_3
    }

    ADS8900_SDO_WIDTH_OFFSET = 2
    ADS8900_SDO_WIDTH_MASK = 3 << ADS8900_SDO_WIDTH_OFFSET

    SDO_WIDTH = {
        1: 0,
        2: 2,
        4: 3
    }


class ADS8900Exception(Exception):
    def __init__(self, err_str):
        self.err_reason = '%s.' % err_str

    def __str__(self):
        return self.err_reason


class ADS8900(object):
    '''
    The ADS8900 is a high-speed, single-channel, high-precision, 20-bit successive-approximation-register(SAR) ADC.

    Examples:
        mix_ads8900_hyc = MIXADS8900HYC('/dev/MIX_ADS8900_HYC_0')
        ads8900 = ADS8900(5.0, spi_bus)
    '''

    def __init__(self, reference, mix_ads8900_hyc=None):
        if mix_ads8900_hyc is None:
            self.mix_ads8900_hyc = MIXADS8900HYCEmulator('ads8900_emulator')
        else:
            self.mix_ads8900_hyc = mix_ads8900_hyc
        self._reference = reference
        self._sdo_mode = 0

    def write_register(self, reg, content):
        '''
        ADS8900 write specific register.

        Args:
            reg:   instance(int), [0~0xFF], .
            content:  instance(int).

        Examples:
            ads8900.write_register(ADS8900Def.ADS8900_REG_SDI_CNTL, 0x00)

        '''
        assert reg in ADS8900Def.REGISTERS
        assert isinstance(content, int)
        raw = (ADS8900Def.ADS8900_CMD_WR_REG << ADS8900Def.ADS8900_CMD_OFFSET) | \
              (reg << ADS8900Def.ADS8900_REG_OFFSET) | (content & 0xFF)
        self.spi_switch()
        self.mix_ads8900_hyc.write([raw])

    def read_register(self, reg):
        '''
        ADS8900 read specific register.

        Args:
            reg:   instance(int), [0~0xFF], .

        Returns:
            int.

        Examples:
            rd = ads8900.read_register(ADS8900Def.ADS8900_REG_SDI_CNTL)

        '''
        assert reg in ADS8900Def.REGISTERS
        raw = (ADS8900Def.ADS8900_CMD_RD_REG << ADS8900Def.ADS8900_CMD_OFFSET) | (reg << ADS8900Def.ADS8900_REG_OFFSET)
        self.spi_switch()
        return self.mix_ads8900_hyc.write_and_read([raw], 1)[0] >> 14

    def set_sdo_width(self, width):
        '''
        ADS8900 set SDO data width.

        Args:
            width:   instance(int), in list ADS8900Def.SDO_WIDTH, .

        Examples:
            ads8900.set_sdo_width(4)

        '''
        assert width in ADS8900Def.SDO_WIDTH.keys()
        reg = self.read_register(ADS8900Def.ADS8900_REG_SDO_CNTL)
        if (reg & ADS8900Def.ADS8900_SDO_WIDTH_MASK) != \
                (ADS8900Def.SDO_WIDTH[width] << ADS8900Def.ADS8900_SDO_WIDTH_OFFSET):
            reg &= ~ADS8900Def.ADS8900_SDO_WIDTH_MASK
            reg |= ADS8900Def.SDO_WIDTH[width] << ADS8900Def.ADS8900_SDO_WIDTH_OFFSET
            self.write_register(ADS8900Def.ADS8900_REG_SDO_CNTL, reg)
            self._sdo_mode = ADS8900Def.SDO_WIDTH[width]
        re = self.read_register(ADS8900Def.ADS8900_REG_SDO_CNTL)
        print re

    def set_sdi_mode(self, mode):
        '''
        ADS8900 set SDI mode.

        Args:
            mode:   instance(int), in list ADS8900Def.SDI_Type, .

        Examples:
            ads8900.set_sdi_mode('MODE2')

        '''
        assert mode in ADS8900Def.SDI_Type.keys()
        self.write_register(ADS8900Def.ADS8900_REG_SDI_CNTL, ADS8900Def.SDI_Type[mode])

    def spi_switch(self):
        self.mix_ads8900_hyc.chip_select(0x01, 8000000, 22, qspi=False if self._sdo_mode == 0 else True)

    def read_voltage(self, freq, duration):
        '''
        ADS8900 read voltage with specific frequency and times.

        Args:
            freq:   int, [1~500000], unit is Hz.
            duration:   float or int, sample time in Second.

        Returns:
            list of voltage sampled by ADS8900, unit is V.

        Examples:
            voltages = ads8900.read_voltage(1000, 1)

        '''
        times = int(freq * duration)
        # assert times <= 8000
        if times > 8000:
            times = 8000
        self.spi_switch()
        self.mix_ads8900_hyc.axi4_bus.write_32bit_fix(MIXADS8900HYCDef.AD_SAMP_RATE, [int(125000000 / freq)])
        self.mix_ads8900_hyc.axi4_bus.write_32bit_fix(MIXADS8900HYCDef.AD_SAMP_NUM, [times])
        self.mix_ads8900_hyc.axi4_bus.write_32bit_fix(MIXADS8900HYCDef.AD_SAMP_REQ, [0x01])
        while True:
            if 0 == self.mix_ads8900_hyc.axi4_bus.read_8bit_fix(MIXADS8900HYCDef.SPI_BUSY, 1)[0]:
                break
        codes = []
        for each in range(times):
            raw = self.mix_ads8900_hyc.axi4_bus.read_32bit_fix(MIXADS8900HYCDef.AD_DATA, 1)[0]
            # if raw == 0xFFFFFF:
            #     raise ADS8900Exception('Abnormal data received')
            codes.append(raw)
        volts = []
        for each in codes:
            # ffffffff/mmmmmmmm/llll/rr00
            #      ffffffff/mmmmmmmm/llll
            if each <= 0x7FFFFF:
                tmp = 1.0 * each / 0x7FFFF * self._reference
            else:
                tmp = -1.0 * (0x1000000 - each) / 0x7FFFF * self._reference
            volts.append(tmp)
        return volts
