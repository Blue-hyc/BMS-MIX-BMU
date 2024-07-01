# -*- coding: utf-8 -*-
from mix.driver.hyc.common.ipcore.mix_ad5761_hyc import MIXAD5761HYC, MIXAD5761HYCDef
from math import *
from cmath import *
from dac_base import DACBase
import time


__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class AD5791Def:
    AD5791_REG_OFFSET = 20
    AD5791_REG_NOP = 0
    AD5791_REG_DAC = 1
    AD5791_REG_CTRL = 2
    AD5791_REG_CLR = 3
    AD5791_REG_SOFT_CTRL = 4

    REGISTERS = [
        AD5791_REG_NOP,
        AD5791_REG_DAC,
        AD5791_REG_CTRL,
        AD5791_REG_CLR,
        AD5791_REG_SOFT_CTRL
    ]

    COMMUNICATION_WRITE = 0x000000
    COMMUNICATION_READ = 0x800000

    COMMUNICATION = [
        COMMUNICATION_WRITE,
        COMMUNICATION_READ
    ]

    AD5791_LDAC_OFFSET = 0
    AD5791_LDAC_MASK = 1 << AD5791_LDAC_OFFSET

    AD5791_CLR_OFFSET = 1
    AD5791_CLR_MASK = 1 << AD5791_CLR_OFFSET

    AD5791_RESET_OFFSET = 2
    AD5791_RESET_MASK = 1 << AD5791_RESET_OFFSET

    AD5791_RBUF_OFFSET = 1
    AD5791_RBUF_MASK = 1 << AD5791_RBUF_OFFSET

    AD5791_OPGND_OFFSET = 2
    AD5791_OPGND_MASK = 1 << AD5791_OPGND_OFFSET

    AD5791_DACTRI_OFFSET = 3
    AD5791_DACTRI_MASK = 1 << AD5791_DACTRI_OFFSET

    AD5791_OUTPUT_NORMAL = 0
    AD5791_OUTPUT_CLAMPED = 1
    AD5791_OUTPUT_TRISTATE = 2

    Output_Type = {
        AD5791_OUTPUT_NORMAL:  (0 << AD5791_DACTRI_OFFSET) | (0 << AD5791_OPGND_OFFSET),
        AD5791_OUTPUT_CLAMPED: AD5791_OPGND_MASK,
        AD5791_OUTPUT_TRISTATE: AD5791_DACTRI_MASK
    }

    AD5791_BIN_OFFSET = 4
    AD5791_BIN_MASK = 1 << AD5791_BIN_OFFSET

    AD5791_SDODIS_OFFSET = 5
    AD5791_SDODIS_MASK = 1 << AD5791_SDODIS_OFFSET

    AD5791_LIN_COMP_OFFSET = 6
    AD5791_LIN_COMP_MASK = 0xF << AD5791_LIN_COMP_OFFSET

    AD5791_REF_INPUT_SPAN_0_10V = 0 << AD5791_LIN_COMP_OFFSET
    AD5791_REF_INPUT_SPAN_10_12V = 0 << AD5791_LIN_COMP_OFFSET
    AD5791_REF_INPUT_SPAN_12_16V = 0 << AD5791_LIN_COMP_OFFSET
    AD5791_REF_INPUT_SPAN_16_19V = 0 << AD5791_LIN_COMP_OFFSET
    AD5791_REF_INPUT_SPAN_19_20V = 0 << AD5791_LIN_COMP_OFFSET

    Input_Span_Type = [
        AD5791_REF_INPUT_SPAN_0_10V,
        AD5791_REF_INPUT_SPAN_10_12V,
        AD5791_REF_INPUT_SPAN_12_16V,
        AD5791_REF_INPUT_SPAN_16_19V,
        AD5791_REF_INPUT_SPAN_19_20V
    ]


class AD5791Exception(Exception):
    def __init__(self, err_str):
        self.err_reason = 'AD5791: %s.' % err_str

    def __str__(self):
        return self.err_reason


class AD5791(DACBase):
    '''
    AD5791 is a single 20-bit, unbuffered voltage-output digital-to-analog converter(DAC) that operates from a bipolar
    supply of up to 33 V.

    ClassType = DAC

    Args:
        reference: instance(float),
        spi_bus:  instance(SPI)/None, Class instance of SPI bus,
                                      If not using the parameter
                                      will create Emulator

    Examples:
        axi = AXI4LiteBus('/dev/quad_spi_0', 256)
        spi = PLSPIBus(axi)
        ad5791 = AD5791(spi)

    '''
    rpc_public_api = ['write_register', 'read_register', 'set_volt', 'set_output_mode']

    def __init__(self, reference, mix_ad5761_hyc=None):
        self.mix_ad5761_hyc = mix_ad5761_hyc
        self._reference = reference
        self._bipolar = False
        super(AD5791, self).__init__()

    def spi_switch(self):
        self.mix_ad5761_hyc.chip_select(0, 10000000, 24)

    def write_register(self, reg, content):
        '''
        AD5791 write specific register.

        Args:
            reg:   instance(int), [0~0xFF], .
            content:  instance(int).

        Returns:
            int.

        Examples:
            ad5791.write_register(AD5791Def.AD5791_REG_CLR, 0x00)

        '''
        assert reg in AD5791Def.REGISTERS
        assert isinstance(content, int)
        raw = AD5791Def.COMMUNICATION_WRITE | (reg << AD5791Def.AD5791_REG_OFFSET) | (content & 0x0FFFFF)
        self.spi_switch()
        self.mix_ad5761_hyc.write([raw])

    def read_register(self, reg):
        '''
        AD5791 read specific register.

        Args:
            reg:   instance(int), [0~0xFF], .

        Returns:
            int.

        Examples:
            rd_data = ad5791.read_register(AD5791Def.AD5791_REG_CLR)
            print(rd_data)

        '''
        assert reg in AD5791Def.REGISTERS
        raw = AD5791Def.COMMUNICATION_READ | (reg << AD5791Def.AD5791_REG_OFFSET)
        self.spi_switch()
        rd = self.mix_ad5761_hyc.write_and_read([raw], 1)
        return rd[0] & 0x0FFFFF

    def set_voltage(self, volt):
        dac = self._volt_to_code(volt)
        self.write_register(AD5791Def.AD5791_REG_DAC, dac)

    def set_output_mode(self, bipolar):
        assert bipolar in [True, False]
        ctrl = self.read_register(AD5791Def.AD5791_REG_CTRL)
        ctrl &= ~(AD5791Def.AD5791_DACTRI_MASK | AD5791Def.AD5791_OPGND_MASK) & 0xFFFFF
        ctrl |= AD5791Def.Output_Type[AD5791Def.AD5791_OUTPUT_NORMAL]
        if bipolar:
            ctrl &= ~AD5791Def.AD5791_RBUF_MASK
        else:
            ctrl |= AD5791Def.AD5791_RBUF_MASK
        self._bipolar = bipolar
        ctrl |= AD5791Def.AD5791_BIN_MASK
        self.write_register(AD5791Def.AD5791_REG_CTRL, ctrl)

    def _volt_to_code(self, volt):
        if self._bipolar:
            assert fabs(volt) < self._reference
            dac = int(round(1.0 * (volt - (0 - self._reference)) * pow(2, 20) / (2 * self._reference))) & 0x0FFFFF
        else:
            assert 0.0 <= volt < self._reference
            dac = int(round(1.0 * volt * (pow(2, 20) - 1) / self._reference)) & 0x0FFFFF
        return dac

    def set_voltages(self, freq, times, volts):
        assert isinstance(volts, list)
        # self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.CONVER_REQ, [0x00])
        self.mix_ad5761_hyc.axi4_bus.write_8bit_inc(MIXAD5761HYCDef.REPERTY_TIMES, [0])
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_NUM, [0])
        self.spi_switch()
        self.mix_ad5761_hyc.axi4_bus.write_8bit_inc(MIXAD5761HYCDef.FIFO_CLR, [0x01])
        raw = []
        for each in volts:
            dac = self._volt_to_code(each)
            raw.append(AD5791Def.COMMUNICATION_WRITE | (AD5791Def.AD5791_REG_DAC << AD5791Def.AD5791_REG_OFFSET) | (dac & 0x0FFFFF))
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_DATA, raw)
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_NUM, [len(volts)])
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_RATE, [125000000 / freq])
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.REPERTY_TIMES, [times])
        # self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.CONVER_REQ, [0x01])

    def start_convst(self):
        self.spi_switch()
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.CONVER_REQ, [0x01])
