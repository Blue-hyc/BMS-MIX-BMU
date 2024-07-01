# -*- coding: utf-8 -*-
import time

from psu_board_base import *
from mix.addon.driver.module.transition_board import *
from ..ic.ad5791 import *
from mix.driver.core.bus.pin import Pin

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class PSU2BoardDef:
    CURRENT_RANGE_5uA = 0
    CURRENT_RANGE_25uA = 1
    CURRENT_RANGE_250uA = 2
    CURRENT_RANGE_2_5mA = 3
    CURRENT_RANGE_25mA = 4
    CURRENT_RANGE_1A = 5
    CURRENT_RANGE_4A = 6
    CURRENT_RANGE_10A = 7

    CURRENT_RANGES = {
        CURRENT_RANGE_5uA:   AD5560Def.AD5560_CURRENT_RANGE_5uA,
        CURRENT_RANGE_25uA:  AD5560Def.AD5560_CURRENT_RANGE_25uA,
        CURRENT_RANGE_250uA: AD5560Def.AD5560_CURRENT_RANGE_250uA,
        CURRENT_RANGE_2_5mA: AD5560Def.AD5560_CURRENT_RANGE_2_5mA,
        CURRENT_RANGE_25mA:  AD5560Def.AD5560_CURRENT_RANGE_25mA,
        CURRENT_RANGE_1A:    AD5560Def.AD5560_CURRENT_RANGE_EXT2,
        CURRENT_RANGE_4A:    AD5560Def.AD5560_CURRENT_RANGE_EXT2,
        CURRENT_RANGE_10A:   AD5560Def.AD5560_CURRENT_RANGE_EXT2,
    }

    R_SENSE = {
        CURRENT_RANGE_5uA:   100000.0,
        CURRENT_RANGE_25uA:  20000.0,
        CURRENT_RANGE_250uA: 2000.0,
        CURRENT_RANGE_2_5mA: 200.0,
        CURRENT_RANGE_25mA:  20.0,
        CURRENT_RANGE_1A:    0.25,
        CURRENT_RANGE_4A:    0.25,
        CURRENT_RANGE_10A:   0.05,
    }

    Clamp_Type = {
        CURRENT_RANGE_5uA:   0.000005,
        CURRENT_RANGE_25uA:  0.000025,
        CURRENT_RANGE_250uA: 0.00025,
        CURRENT_RANGE_2_5mA: 0.0025,
        CURRENT_RANGE_25mA:  0.025,
        CURRENT_RANGE_1A:    1.0,
        CURRENT_RANGE_4A:    4.0,
        CURRENT_RANGE_10A:   10.0,
    }

    GAIN_TYPE = {
        CURRENT_RANGE_5uA:   10.0,
        CURRENT_RANGE_25uA:  10.0,
        CURRENT_RANGE_250uA: 10.0,
        CURRENT_RANGE_2_5mA: 10.0,
        CURRENT_RANGE_25mA:  10.0,
        CURRENT_RANGE_1A:    1.0,
        CURRENT_RANGE_4A:    1.0,
        CURRENT_RANGE_10A:   1.0,
    }

    CS_0R030_R = 8
    CS_0R050_R = 9
    CS_0R250_R = 10

    PS2_Sense_1K_En = 26
    Current_A_Range_En = 27
    Range_50mR_30mR_En = 28
    Sink_2A_En = 29

    EXTERNAL_RSENSE_CS = {
        CURRENT_RANGE_1A:  [1, 0, 0],
        CURRENT_RANGE_4A:  [1, 0, 0],
        CURRENT_RANGE_10A: [0, 1, 0],
    }

    DPS_REFERENCE = 5.0


class PSU2BoardException(Exception):
    def __init__(self, __err):
        self.__err = __err

    def __str__(self):
        return "PSU2Board Exception [{}]".format(self.__err)


class PSU2Board(PSUBoardBase):
    compatible = ['J0H-PSU2-0-001']

    rpc_public_api = ['fv', 'fi', 'reset', 'restore', 'output', 'cc_switch']

    def __init__(self, io_mux, i2c_bus, inh_pin, spi_s0, spi_bus):
        self._spi_s0 = spi_s0
        self.comparer = 0.90
        self._ext_rsense_pins = [Pin(io_mux, PSU2BoardDef.CS_0R030_R, 'output'),
                                 Pin(io_mux, PSU2BoardDef.CS_0R050_R, 'output'),
                                 Pin(io_mux, PSU2BoardDef.CS_0R250_R, 'output')]
        self._ext_output_pin = Pin(io_mux, PSU2BoardDef.Current_A_Range_En, 'output')
        Pin(io_mux, PSU2BoardDef.Sink_2A_En, 'output').set_level(0)

        self._current_range = PSU2BoardDef.CURRENT_RANGE_25mA
        super(PSU2Board, self).__init__(i2c_bus, PSU2BoardDef.DPS_REFERENCE, inh_pin, spi_bus, AD5791(10.0, spi_bus))

    def pre_power_on_init(self):
        pass

    def post_power_on_init(self):
        super(PSU2Board, self).post_power_on_init()
        # self._spi_s0.set_level(0)
        # print 'psu2', hex(self._ad5560.read_register(AD5560Def.AD5560_REG_COMP_2))
        self._spi_s0.set_level(1)
        self._dac.set_output_mode(False)

    def fv(self, volt, clamp_current, current_range):
        assert isinstance(volt, float) or isinstance(volt, int)
        assert isinstance(clamp_current, float) or isinstance(clamp_current, int)
        assert current_range in PSU2BoardDef.CURRENT_RANGES
        # print 'FV called, voltage:', volt, 'current_limit:', clamp_current, 'current_range:', current_range
        self._spi_s0.set_level(0)
        self.output(False)
        self._ad5560.enable_sw_inh(True)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        # switch external r sense
        self.set_external_r_sense(current_range)
        self._ad5560.set_current_range(PSU2BoardDef.CURRENT_RANGES[current_range])
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_MASTER_OUT_INTERNAL)
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_V_SENSE)
        clamp_volt = clamp_current * PSU2BoardDef.R_SENSE[current_range] * AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][
            AD5560Def.AD5560_MI_GAIN]
        if clamp_current > 0:
            self._ad5560.set_clamp(clamp_volt, -0.1)
        else:
            self._ad5560.set_clamp(0.1, clamp_volt)
        self._ad5560.set_comparator(AD5560Def.AD5560_CMP_TYPE_CURRENT, PSU2BoardDef.CURRENT_RANGES[current_range],
                                    0.5 * clamp_volt, 0.2 * clamp_volt)
        self._ad5560.set_dac(volt)
        # sleep 100ms
        time.sleep(0.1)
        self._ad5560.enable_sw_inh(False)
        self._current_range = current_range
        self.output(True)

    def fi(self, current, clamp_volt, current_range):
        assert isinstance(current, float) or isinstance(current, int)
        assert isinstance(clamp_volt, float) or isinstance(clamp_volt, int)
        assert current_range in PSU2BoardDef.CURRENT_RANGES
        # print 'FI called, current:', current, 'volt_limit:', clamp_volt, 'current_range:', current_range
        self.output(False)
        self._spi_s0.set_level(0)
        # switch external r sense
        self.set_external_r_sense(current_range)
        self._ad5560.enable_sw_inh(True)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        self._ad5560.set_current_range(PSU2BoardDef.CURRENT_RANGES[current_range])
        self._ad5560.set_clamp(clamp_volt, -2)
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_SLAVE_FI)
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_I_SENSE)
        # different current range means different CC configuration
        cf = AD5560Def.AD5560_Cf_1
        if current_range == PSU2BoardDef.CURRENT_RANGE_10A:
            if current > 7:
                # for sec_scp
                cc = AD5560Def.AD5560_Cc_0111
            else:
                # for prim_scp
                cc = AD5560Def.AD5560_Cc_1101
            switch = [[3, 1], [2, 1], [1, 1], [0, 1]]
        else:
            cc = AD5560Def.AD5560_Cc_0101
            switch = [[3, 1], [2, 1], [1, 1], [0, 1]]
        # cc3 对大电流的震荡有较好的抑制作用，小电流不使用
        self._ad5560.set_manual_compensation(AD5560Def.AD5560_Rz_500Ohm, AD5560Def.AD5560_Rp_200Ohm,
                                             AD5560Def.AD5560_Gm_300, cf, cc)
        self.cc_switch(switch)
        dac = current * PSU2BoardDef.R_SENSE[current_range] * AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][
            AD5560Def.AD5560_MI_GAIN]
        self._ad5560.set_comparator(AD5560Def.AD5560_CMP_TYPE_CURRENT, PSU2BoardDef.CURRENT_RANGES[current_range],
                                    self.comparer * dac, 0.2 * dac)
        self._spi_s0.set_level(1)
        self._dac.set_output_mode(True)
        self._dac.set_voltage(dac)
        # sleep 100ms
        time.sleep(0.1)
        self._spi_s0.set_level(0)
        self._ad5560.enable_sw_inh(False)
        # self.output(True)
        self._current_range = current_range
        # if 2 < current <= 10:
        #     self.output(True)
        #     time.sleep(0.01)
        #     self.output(False)
        # elif 10 < current < 33:
        #     self.output(True)
        #     time.sleep(0.0008)
        #     self.output(False)

    def cal_fi(self, current, clamp_volt, current_range):
        assert isinstance(current, float) or isinstance(current, int)
        assert isinstance(clamp_volt, float) or isinstance(clamp_volt, int)
        assert current_range in PSU2BoardDef.CURRENT_RANGES
        # print 'FI called, current:', current, 'volt_limit:', clamp_volt, 'current_range:', current_range
        self.output(False)
        self._spi_s0.set_level(0)
        # switch off external r sense
        for i in range(3):
            self._ext_rsense_pins[i].set_level(0)
        self._ad5560.enable_sw_inh(True)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        self._ad5560.set_current_range(PSU2BoardDef.CURRENT_RANGES[current_range])
        self._ad5560.set_clamp(clamp_volt, -0.1)
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_SLAVE_FI)
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_I_SENSE)
        # different current range means different CC configuration
        cf = AD5560Def.AD5560_Cf_1
        if current_range == PSU2BoardDef.CURRENT_RANGE_10A:
            cc = AD5560Def.AD5560_Cc_1001
            switch = [[3, 1], [2, 1], [1, 1], [0, 1]]
        else:
            cc = AD5560Def.AD5560_Cc_0101
            switch = [[3, 1], [2, 1], [1, 1], [0, 1]]
        # cc3 对大电流的震荡有较好的抑制作用，小电流不使用
        self._ad5560.set_manual_compensation(AD5560Def.AD5560_Rz_500Ohm, AD5560Def.AD5560_Rp_200Ohm,
                                             AD5560Def.AD5560_Gm_300, cf, cc)
        self.cc_switch(switch)
        dac = current * PSU2BoardDef.R_SENSE[current_range] * AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][
            AD5560Def.AD5560_MI_GAIN]
        self._ad5560.set_comparator(AD5560Def.AD5560_CMP_TYPE_CURRENT, PSU2BoardDef.CURRENT_RANGES[current_range],
                                    0.95*dac, 0.2*dac)
        self._spi_s0.set_level(1)
        self._dac.set_output_mode(True)
        self._dac.set_voltage(dac)
        # sleep 100ms
        time.sleep(0.1)
        self._spi_s0.set_level(0)
        self._ad5560.enable_sw_inh(False)
        # self.output(True)
        self._current_range = current_range

    def restore(self, zero=True):
        self.output(False)
        self.set_external_r_sense(PSU2BoardDef.CURRENT_RANGE_25mA)
        self._spi_s0.set_level(0)
        self._ad5560.enable_sw_inh(True)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        self._ad5560.set_current_range(PSU2BoardDef.CURRENT_RANGES[PSU2BoardDef.CURRENT_RANGE_25mA])
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_V_SENSE)
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_MASTER_OUT_INTERNAL)
        clamp_volt = 0.01 * PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_25mA] * \
                     AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][
                         AD5560Def.AD5560_MI_GAIN]
        self._ad5560.set_clamp(clamp_volt, -clamp_volt)
        self._spi_s0.set_level(1)
        self._dac.set_voltage(0.0)
        self._spi_s0.set_level(0)
        self._ad5560.set_dac(0.0)
        self.fv(0, 0.01, 3)
        # sleep 100ms
        time.sleep(0.1)
        self._current_range = PSU2BoardDef.CURRENT_RANGE_25mA
        if zero:
            self._ad5560.enable_sw_inh(False)
            self.output(True)

    def analog_current(self, current):
        self._spi_s0.set_level(0)
        self.output(False)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_0)
        self._ad5560.set_current_range(AD5560Def.AD5560_CURRENT_RANGE_EXT1)
        self._ad5560.set_clamp(4.5, -4.5)
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_SLAVE_FI)
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_I_SENSE)
        self._ad5560.set_manual_compensation(AD5560Def.AD5560_Rz_500Ohm, AD5560Def.AD5560_Rp_200Ohm,
                                             AD5560Def.AD5560_Gm_300, AD5560Def.AD5560_Cf_1, AD5560Def.AD5560_Cc_0101)
        self.cc_switch([[0, 1], [1, 1], [2, 1], [3, 1]])
        self._spi_s0.set_level(1)
        self._dac.set_voltage(0.0)
        # sleep 100ms
        time.sleep(0.1)
        self._spi_s0.set_level(0)
        self._ad5560.enable_sw_inh(False)
        # self.output(True)
        self._spi_s0.set_level(1)
        volts = []
        for each in current:
            volts.append(each * PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_1A] *
                         AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_0][AD5560Def.AD5560_MI_GAIN])
        # print volts
        self._dac.set_voltages(400000, 40, volts)

    def analog_enable(self):
        self._spi_s0.set_level(1)
        self._dac.start_convst()

    def range(self, current):
        assert isinstance(current, float) or isinstance(current, int)
        current = fabs(current)
        print PSU2BoardDef.Clamp_Type.keys()
        ordered_list = sorted(PSU2BoardDef.Clamp_Type.keys())
        for i in ordered_list:
            if current <= PSU2BoardDef.Clamp_Type[i]:
                self._current_range = i
                return i
        raise PSU2BoardException("no proper current range found")

    @property
    def current_range(self):
        return self._current_range

    def set_external_r_sense(self, current_range):
        if current_range in PSU2BoardDef.EXTERNAL_RSENSE_CS.keys():
            # for i in range(3):
            #     level = PSU2BoardDef.EXTERNAL_RSENSE_CS[current_range][i]
            #     self._ext_rsense_pins[i].set_level(level)
            levels = PSU2BoardDef.EXTERNAL_RSENSE_CS[current_range]
            for each in range(3):
                self._ext_rsense_pins[each].set_level(levels[each])
            self._ext_output_pin.set_level(1)
        else:
            self._ext_output_pin.set_level(0)
            # time.sleep(0.001)
