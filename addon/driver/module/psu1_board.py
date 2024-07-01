# -*- coding: utf-8 -*-
from psu_board_base import *
from ..ic.ad5560 import *
from ..ic.ad5761 import *
from ..ic.ad5791 import *

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class PSU1BoardDef:
    # CURRENT_RANGE_40nA = 0
    CURRENT_RANGE_5uA = 0
    CURRENT_RANGE_25uA = 1
    CURRENT_RANGE_250uA = 2
    CURRENT_RANGE_2_5mA = 3
    CURRENT_RANGE_25mA = 4
    CURRENT_RANGE_100mA = 5

    CURRENT_RANGES = {
        # CURRENT_RANGE_40nA: AD5560Def.AD5560_CURRENT_RANGE_5uA,
        CURRENT_RANGE_5uA: AD5560Def.AD5560_CURRENT_RANGE_5uA,
        CURRENT_RANGE_25uA: AD5560Def.AD5560_CURRENT_RANGE_25uA,
        CURRENT_RANGE_250uA: AD5560Def.AD5560_CURRENT_RANGE_250uA,
        CURRENT_RANGE_2_5mA: AD5560Def.AD5560_CURRENT_RANGE_2_5mA,
        CURRENT_RANGE_25mA: AD5560Def.AD5560_CURRENT_RANGE_25mA,
        CURRENT_RANGE_100mA: AD5560Def.AD5560_CURRENT_RANGE_EXT1,
    }

    R_SENSE = {
        # CURRENT_RANGE_40nA: 1000000.0,
        CURRENT_RANGE_5uA:  1000000.0,
        CURRENT_RANGE_25uA: 20000.0,
        CURRENT_RANGE_250uA: 2000.0,
        CURRENT_RANGE_2_5mA: 200.0,
        CURRENT_RANGE_25mA: 20.0,
        CURRENT_RANGE_100mA: 0.5
    }

    Clamp_Type = {
        # CURRENT_RANGE_40nA: 0.00000004,
        CURRENT_RANGE_5uA: 0.000005,
        CURRENT_RANGE_25uA: 0.000025,
        CURRENT_RANGE_250uA: 0.00025,
        CURRENT_RANGE_2_5mA: 0.0025,
        CURRENT_RANGE_25mA: 0.025,
        CURRENT_RANGE_100mA: 0.2
    }

    GAIN_TYPE = {
        # CURRENT_RANGE_40nA:  10.0,
        CURRENT_RANGE_5uA: 1.0,
        CURRENT_RANGE_25uA: 10.0,
        CURRENT_RANGE_250uA: 10.0,
        CURRENT_RANGE_2_5mA: 10.0,
        CURRENT_RANGE_25mA: 10.0,
        CURRENT_RANGE_100mA: 1.0
    }

    DPS_REFERENCE = 2.5


class PSU1Board(PSUBoardBase):
    compatible = ['J0H-PSU1-0-001']

    rpc_public_api = ['fv', 'fi', 'reset', 'restore', 'output', 'post_power_on_init']

    def __init__(self, cs_na_pin, i2c_bus, inh_pin, spi_s1, spi_s0, spi_bus):
        self._spi_ss = [spi_s1, spi_s0]
        self._cs_na_pin = cs_na_pin
        self._cs_na_pin.set_level(0)
        self._current_range = PSU1BoardDef.CURRENT_RANGE_100mA
        super(PSU1Board, self).__init__(i2c_bus, PSU1BoardDef.DPS_REFERENCE, inh_pin, spi_bus, AD5791(10.0, spi_bus))

    def pre_power_on_init(self):
        pass

    def post_power_on_init(self):
        super(PSU1Board, self).post_power_on_init()
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(1)
        self._dac.set_output_mode(True)

    def fv(self, volt, clamp_current, current_range):
        assert isinstance(volt, float) or isinstance(volt, int)
        assert isinstance(clamp_current, float) or isinstance(clamp_current, int)
        assert current_range in PSU1BoardDef.CURRENT_RANGES
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(0)
        # time.sleep(0.1)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        # for measurement of shutdown current consumption
        level = 1 if current_range == PSU1BoardDef.CURRENT_RANGE_5uA else 0
        self._cs_na_pin.set_level(level)
        self._ad5560.set_current_range(PSU1BoardDef.CURRENT_RANGES[current_range])
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_MASTER_OUT_INTERNAL)
        # we use 'sense' instead of 'measout_v' to measure voltage and 'measout_i' to FV MI for
        # shutdown current measurement
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_I_SENSE)
        clamp_volt = clamp_current * PSU1BoardDef.R_SENSE[current_range] * AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][
            AD5560Def.AD5560_MI_GAIN]
        if clamp_current > 0:
            self._ad5560.set_clamp(clamp_volt, -0.1)
        else:
            self._ad5560.set_clamp(0.1, clamp_volt)
        self._ad5560.set_dac(volt)
        # sleep 100ms
        time.sleep(0.1)
        self._ad5560.enable_sw_inh(False)
        self._current_range = current_range
        self.output(True)

    def fi(self, current, clamp_volt, current_range):
        assert isinstance(current, float) or isinstance(current, int)
        assert isinstance(clamp_volt, float) or isinstance(clamp_volt, int)
        assert current_range in PSU1BoardDef.CURRENT_RANGES
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(0)
        # time.sleep(0.1)
        self._cs_na_pin.set_level(0)
        self.output(False)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        self._ad5560.set_current_range(PSU1BoardDef.CURRENT_RANGES[current_range])
        if clamp_volt > 0:
            self._ad5560.set_clamp(clamp_volt, -0.1)
        else:
            self._ad5560.set_clamp(0.1, clamp_volt)
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_SLAVE_FI)
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_I_SENSE)
        self._ad5560.set_manual_compensation(AD5560Def.AD5560_Rz_500Ohm, AD5560Def.AD5560_Rp_200Ohm,
                                             AD5560Def.AD5560_Gm_300, AD5560Def.AD5560_Cf_1, AD5560Def.AD5560_Cc_0101)
        self.cc_switch([[0, 1], [1, 1], [2, 1], [3, 1]])
        dac = current * PSU1BoardDef.R_SENSE[current_range] * \
              AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][AD5560Def.AD5560_MI_GAIN]
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(1)
        # time.sleep(0.1)
        self._dac.set_voltage(dac)
        # sleep 100ms
        time.sleep(0.1)
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(0)
        # time.sleep(0.1)
        self._ad5560.enable_sw_inh(False)
        self._current_range = current_range

    def restore(self, zero=True):
        self._cs_na_pin.set_level(0)
        self.output(False)
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(0)
        self._ad5560.enable_sw_inh(True)
        self._ad5560.enable_pd(False)
        self._ad5560.set_gain(AD5560Def.AD5560_GAIN_1)
        self._ad5560.set_current_range(PSU1BoardDef.CURRENT_RANGES[PSU1BoardDef.CURRENT_RANGE_100mA])
        self._ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_V_SENSE)
        self._ad5560.set_mode(AD5560Def.AD5560_MODE_MASTER_OUT_INTERNAL)
        clamp_volt = 0.01 * PSU1BoardDef.R_SENSE[PSU1BoardDef.CURRENT_RANGE_100mA] * \
                     AD5560Def.GAIN_Type[AD5560Def.AD5560_GAIN_1][AD5560Def.AD5560_MI_GAIN]
        self._ad5560.set_clamp(clamp_volt, -clamp_volt)
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(1)
        # time.sleep(0.1)
        self._dac.set_voltage(0.0)
        self._spi_ss[0].set_level(0)
        self._spi_ss[1].set_level(0)
        # time.sleep(0.1)
        self._ad5560.set_dac(0.0)
        # sleep 100ms
        time.sleep(0.1)
        self._ad5560.enable_sw_inh(False)
        self._current_range = PSU1BoardDef.CURRENT_RANGE_100mA
        if zero:
            self.output(True)

    def range(self, current):
        assert isinstance(current, float) or isinstance(current, int)
        current = abs(current)
        for i in PSU1BoardDef.Clamp_Type:
            if current <= PSU1BoardDef.Clamp_Type[i]:
                self._current_range = i
                return i
        return -1

    @property
    def current_range(self):
        return self._current_range

    def set_na_r_sense(self, enable):
        assert enable in bool
        level = 1 if enable else 0
        self._cs_na_pin.set_level(level)
