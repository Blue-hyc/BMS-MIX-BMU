# -*- coding: utf-8 -*-
from mix.driver.core.bus.spi_bus_emulator import *
from math import *
from dac_base import *
from mix.driver.hyc.common.ipcore.mix_ad5761_hyc import MIXAD5761HYC, MIXAD5761HYCDef
import time

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class AD5761Def:
    AD5761_CMD_OFFSET = 16

    AD5761_CMD_NOP = 0
    AD5761_CMD_WRITE_INPUT = 1
    AD5761_CMD_UPDATE_DAC = 2
    AD5761_CMD_WRITE_UPDATE_DAC = 3
    AD5761_CMD_WRITE_CTL = 4
    AD5761_CMD_SOFT_DATA_RST = 7
    AD5761_CMD_DISABLE_CHAN = 9
    AD5761_CMD_READ_INPUT = 10
    AD5761_CMD_READ_DAC = 11
    AD5761_CMD_READ_CTL = 12
    AD5761_CMD_SOFT_RESET = 15

    CMD_Type = [
        AD5761_CMD_NOP,
        AD5761_CMD_WRITE_INPUT,
        AD5761_CMD_UPDATE_DAC,
        AD5761_CMD_WRITE_UPDATE_DAC,
        AD5761_CMD_WRITE_CTL,
        AD5761_CMD_SOFT_DATA_RST,
        AD5761_CMD_DISABLE_CHAN,
        AD5761_CMD_READ_INPUT,
        AD5761_CMD_READ_DAC,
        AD5761_CMD_READ_CTL,
        AD5761_CMD_SOFT_RESET
    ]

    AD5761_SPI_DIR_WRITE = 0
    AD5761_SPI_DIR_READ = 1

    SPI_Type = [
        AD5761_SPI_DIR_WRITE,
        AD5761_SPI_DIR_READ
    ]

    AD5761_OUTPUT_RANGE_MINUS_10_PLUS_10 = 0
    AD5761_OUTPUT_RANGE_0_PLUS_10 = 1
    AD5761_OUTPUT_RANGE_MINUS_5_PLUS_5 = 2
    AD5761_OUTPUT_RANGE_0_PLUS_5 = 3
    AD5761_OUTPUT_RANGE_MINUS_2_5_PLUS_7_5 = 4
    AD5761_OUTPUT_RANGE_MINUS_3_PLUS_3 = 5
    AD5761_OUTPUT_RANGE_0_PLUS_16 = 6
    AD5761_OUTPUT_RANGE_0_PLUS_20 = 7

    Output_Range_Type = [
        AD5761_OUTPUT_RANGE_MINUS_10_PLUS_10,
        AD5761_OUTPUT_RANGE_0_PLUS_10,
        AD5761_OUTPUT_RANGE_MINUS_5_PLUS_5,
        AD5761_OUTPUT_RANGE_0_PLUS_5,
        AD5761_OUTPUT_RANGE_MINUS_2_5_PLUS_7_5,
        AD5761_OUTPUT_RANGE_MINUS_3_PLUS_3,
        AD5761_OUTPUT_RANGE_0_PLUS_16,
        AD5761_OUTPUT_RANGE_0_PLUS_20
    ]

    OUTPUT_MIN = 0
    OUTPUT_MAX = 1

    Output_Span = {
        AD5761_OUTPUT_RANGE_MINUS_10_PLUS_10: {OUTPUT_MIN: -10.0, OUTPUT_MAX: 10.0},
        AD5761_OUTPUT_RANGE_0_PLUS_10: {OUTPUT_MIN: 0.0, OUTPUT_MAX: 10.0},
        AD5761_OUTPUT_RANGE_MINUS_5_PLUS_5: {OUTPUT_MIN: -5.0, OUTPUT_MAX: 5.0},
        AD5761_OUTPUT_RANGE_0_PLUS_5: {OUTPUT_MIN: 0.0, OUTPUT_MAX: 5.0},
        AD5761_OUTPUT_RANGE_MINUS_2_5_PLUS_7_5: {OUTPUT_MIN: -2.5, OUTPUT_MAX: 7.5},
        AD5761_OUTPUT_RANGE_MINUS_3_PLUS_3: {OUTPUT_MIN: -3.0, OUTPUT_MAX: 3.0},
        AD5761_OUTPUT_RANGE_0_PLUS_16: {OUTPUT_MIN: 0.0, OUTPUT_MAX: 16.0},
        AD5761_OUTPUT_RANGE_0_PLUS_20: {OUTPUT_MIN: 0.0, OUTPUT_MAX: 20.0}
    }

    CALCULATION_K = 0
    CALCULATION_B = 1

    Calculation_Params = {
        AD5761_OUTPUT_RANGE_MINUS_10_PLUS_10: {CALCULATION_K: 8.0, CALCULATION_B: 4.0},
        AD5761_OUTPUT_RANGE_0_PLUS_10: {CALCULATION_K: 4.0, CALCULATION_B: 0.0},
        AD5761_OUTPUT_RANGE_MINUS_5_PLUS_5: {CALCULATION_K: 4.0, CALCULATION_B: 2.0},
        AD5761_OUTPUT_RANGE_0_PLUS_5: {CALCULATION_K: 2.0, CALCULATION_B: 0.0},
        AD5761_OUTPUT_RANGE_MINUS_2_5_PLUS_7_5: {CALCULATION_K: 4.0, CALCULATION_B: 1.0},
        AD5761_OUTPUT_RANGE_MINUS_3_PLUS_3: {CALCULATION_K: 2.4, CALCULATION_B: 1.2},
        AD5761_OUTPUT_RANGE_0_PLUS_16: {CALCULATION_K: 6.4, CALCULATION_B: 0.0},
        AD5761_OUTPUT_RANGE_0_PLUS_20: {CALCULATION_K: 8.0, CALCULATION_B: 0.0},
    }


class AD5761(DACBase):
    '''
    AD5761 is a single channel, 16-bit serial input, voltage output, digital-to-analog converter(DAC).

    ClassType = DAC

    Args:
        output_range: instance(int),
        spi_bus:  instance(SPI)/None, Class instance of SPI bus,
                                      If not using the parameter
                                      will create Emulator

    Examples:
        axi = AXI4LiteBus('/dev/quad_spi_0', 256)
        spi = PLSPIBus(axi)
        ad5761 = AD5761(spi)

    '''
    rpc_public_api = ['access', 'config_output_range', 'reset', 'set_voltage']

    def __init__(self, reference, mix_ad5761_hyc=None):
        self.mix_ad5761_hyc = mix_ad5761_hyc
        self._reference = reference
        self._output_range = AD5761Def.AD5761_OUTPUT_RANGE_MINUS_10_PLUS_10
        super(AD5761, self).__init__()

    def spi_switch(self):
        self.mix_ad5761_hyc.chip_select(0, 12500000, 24)

    def access(self, cmd, content=0, op=AD5761Def.AD5761_SPI_DIR_WRITE):
        '''
        AD5761 access internal registers.

        Args:
            cmd:     int, AD5761Def.Output_Range_Type.
            content:.
            op:.

        Examples:
            ad5761.access(AD5761Def.AD5761_OUTPUT_RANGE_MINUS_5_PLUS_5)

        '''
        assert isinstance(cmd, int) and cmd in AD5761Def.CMD_Type
        assert isinstance(op, int) and op in AD5761Def.SPI_Type
        raw = cmd << AD5761Def.AD5761_CMD_OFFSET
        self.spi_switch()
        if AD5761Def.AD5761_SPI_DIR_WRITE == op:
            raw |= content & 0xFFFF
            self.mix_ad5761_hyc.write([raw])
        else:
            return self.mix_ad5761_hyc.write_and_read([raw], 1)[0] & 0xFFFF

    def set_output_range(self, output_range):
        '''
        Set output range of AD5761.

        Args:
            output_range:     int, AD5761Def.Output_Range_Type.

        Examples:
            ad5761.set_output_range(AD5761Def.AD5761_OUTPUT_RANGE_MINUS_5_PLUS_5)

        '''
        assert isinstance(output_range, int) and output_range in AD5761Def.Output_Range_Type
        ctl_regbits = 0x0228 | output_range
        # ctl_regbits &= ~0x0020
        self.access(AD5761Def.AD5761_CMD_WRITE_CTL, ctl_regbits)
        print 'ctl reg:[', self.access(AD5761Def.AD5761_CMD_READ_CTL, op=AD5761Def.AD5761_SPI_DIR_READ), ']'
        self._output_range = output_range

    def reset(self):
        '''
        AD5761 software reset.

        Examples:
            ad5761.reset()

        '''
        self.access(AD5761Def.AD5761_CMD_SOFT_RESET)

    def _volt_to_code(self, volt):
        low = AD5761Def.Output_Span[self._output_range][AD5761Def.OUTPUT_MIN]
        high = AD5761Def.Output_Span[self._output_range][AD5761Def.OUTPUT_MAX]
        assert low <= volt < high
        k = AD5761Def.Calculation_Params[self._output_range][AD5761Def.CALCULATION_K]
        b = AD5761Def.Calculation_Params[self._output_range][AD5761Def.CALCULATION_B]
        dac = int(round((volt / self._reference + b) * pow(2, 16) / k)) & 0xFFFF
        return dac

    def set_voltage(self, volt):
        '''
        AD5761 set output voltage.

        Args:
            volt:     float.

        Examples:
            ad5761.set_voltage(1.2)

        '''
        dac = self._volt_to_code(volt)
        self.access(AD5761Def.AD5761_CMD_WRITE_INPUT, dac)

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
            raw.append((AD5761Def.AD5761_CMD_WRITE_INPUT << AD5761Def.AD5761_CMD_OFFSET) | dac)
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_DATA, raw)
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_NUM, [len(volts)])
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.DA_RATE, [125000000 / freq])
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.REPERTY_TIMES, [times])
        # self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.CONVER_REQ, [0x01])

    def start_convst(self):
        self.spi_switch()
        self.mix_ad5761_hyc.axi4_bus.write_32bit_fix(MIXAD5761HYCDef.CONVER_REQ, [0x01])
