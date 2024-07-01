# coding=utf-8
from mix.addon.driver.module.dvm_board import *
from mix.addon.driver.module.psu2_board import *
from mix.addon.driver.module.psu1_board import *
import math
from mix.addon.driver.module.transition_board import *


V2 = 'mm.V2'
V_cell = 'mm.Vcell'
V_pack = 'mm.Vpack'
V_sns = 'mm.Vsns'
V_sda = 'mm.Vsda'
V_scl = 'mm.Vscl'
A1 = 'mm.a1'
A2 = 'mm.a2'
V_ntc = 'mm.ntc'
A_ntc = 'mm.a_ntc'
V_tp4 = 'mm.Tp4'

VOLTAGE_LOC = {
    V2:     {'input': DVMBoardDef.PSU2_SENSE, 'cal': 0},
    # both psu1_sense & ext_mv can be used.
    V_cell: {'input': DVMBoardDef.PSU1_SENSE, 'cal': 0},
    V_pack: {'input': DVMBoardDef.EXTERNAL_MV, 'cal': 0},
    V_sns:  {'input': DVMBoardDef.EXTERNAL_MV, 'cal': 0},
    V_sda:  {'input': DVMBoardDef.I2C_SDA, 'cal': 0},
    V_scl:  {'input': DVMBoardDef.I2C_SCL, 'cal': 0},
    V_ntc:  {'input': DVMBoardDef.PSU2_SENSE, 'cal': 0},
    V_tp4:  {'input': DVMBoardDef.EXTERNAL_MV, 'cal': 0},
}

CURRENT_LOC = {
    A1: {
        PSU1BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.PSU1_MV_1nA,
        PSU1BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_100mA: DVMBoardDef.PSU1_HC_1,
    },
    A2: {
        PSU2BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_1A:    DVMBoardDef.PSU2_HC_2,
        PSU2BoardDef.CURRENT_RANGE_4A:    DVMBoardDef.PSU2_HC_2,
        PSU2BoardDef.CURRENT_RANGE_10A:   DVMBoardDef.PSU2_HC_2,
    },
    A_ntc: {
        PSU2BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_1A:    DVMBoardDef.PSU2_HC_2,
        PSU2BoardDef.CURRENT_RANGE_4A:    DVMBoardDef.PSU2_HC_2,
        PSU2BoardDef.CURRENT_RANGE_10A:   DVMBoardDef.PSU2_HC_2,
    },
}

GAIN_TYPE = {
    A1: {
        PSU1BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.DVM_GAIN_102_P_4,
        PSU1BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_100mA: DVMBoardDef.DVM_GAIN_51_P_2,
    },
    A2: {
        PSU2BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_1A:    DVMBoardDef.DVM_GAIN_3_P_2,
        PSU2BoardDef.CURRENT_RANGE_4A:    DVMBoardDef.DVM_GAIN_3_P_2,
        PSU2BoardDef.CURRENT_RANGE_10A:   DVMBoardDef.DVM_GAIN_3_P_2,
    },
    A_ntc: {
        PSU2BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_1A:    DVMBoardDef.DVM_GAIN_3_P_2,
        PSU2BoardDef.CURRENT_RANGE_4A:    DVMBoardDef.DVM_GAIN_3_P_2,
        PSU2BoardDef.CURRENT_RANGE_10A:   DVMBoardDef.DVM_GAIN_3_P_2,
    },
}


class MM(object):

    rpc_public_api = ['v', 'i', 'iPolling']

    def __init__(self, xobjects):
        self._dvm = xobjects['dvm']
        self._psu1 = xobjects['psu1']
        self._psu2 = xobjects['psu2']
        self._calibration = xobjects['calibration']
        self._transition = xobjects['transition']
        try:
            file_dir = '/mix/MIX_config.csv'
            csv = open(file_dir, 'r')
            t = csv.readline().split(',')
            self.ntc3_offset = t[0]
            t = csv.readline().split(',')
            self.ptc23_offset = t[0:2]
            csv.close()
        except Exception as e:
            self.ptc23_offset = [0, 0]
        self.flag = 1

    def v(self, loc):
        assert loc in VOLTAGE_LOC
        try:
            dvm_input = VOLTAGE_LOC[loc]['input']
            self._dvm.set_input(dvm_input)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            volt = self._dvm.measure_voltage(1000, 1.0)
            # print 'mm.v:', volt
            cal_volt = self._calibration.cal_mv(VOLTAGE_LOC[loc]['cal'], PSU1BoardDef.CURRENT_RANGE_100mA, volt)
            if self._transition.test_item == 'ntc':
                ntc3_temp = 25 + float(self.ntc3_offset)
                ntc3_temp_offset = round(math.exp(3380 / (273.15 + ntc3_temp)) * 10000 * math.exp(-3380 / 298.15),
                                         2) - 10000
                ntc3_volt_offset = ntc3_temp_offset / 1000000
                cal_volt += ntc3_volt_offset
                print 'ntc3_volt_offset', ntc3_volt_offset
                self._transition.test_item = 'normal'
            if self._transition.test_item == 'PTC2':
                ptc23_volt_offset = 0.00025 * float(self.ptc23_offset[0])
                cal_volt += ptc23_volt_offset
                print 'ptc2_volt_offset', cal_volt
                self._transition.test_item = 'normal'
            elif self._transition.test_item == 'PTC3':
                ptc23_volt_offset = 0.00025 * float(self.ptc23_offset[1])
                cal_volt += ptc23_volt_offset
                print 'ptc3_volt_offset', cal_volt
                self._transition.test_item = 'normal'
            print 'volt:', volt
            # cal_volt = volt
            return [0, cal_volt]
        except Exception as e:
            return [-1]

    def i(self, loc):
        assert loc in CURRENT_LOC
        try:
            # identify different current range
            psu = 0 if loc == A1 else 1
            current_range = self._psu1.current_range if loc == A1 else self._psu2.current_range
            r_sense = PSU1BoardDef.R_SENSE[current_range] if loc == A1 else PSU2BoardDef.R_SENSE[current_range]
            psu_gain = PSU1BoardDef.GAIN_TYPE[current_range] if loc == A1 else PSU2BoardDef.GAIN_TYPE[current_range]
            dvm_input = CURRENT_LOC[loc][current_range]
            dvm_gain = GAIN_TYPE[loc][current_range]
            self._dvm.set_input(dvm_input)
            self._dvm.set_gain(dvm_gain)
            if loc == A2 and current_range > PSU2BoardDef.CURRENT_RANGE_10A:
                volt = self._dvm.measure_voltage(1000, 0.002)
            else:
                volt = self._dvm.measure_voltage(1000, 1.0)
            current = volt / r_sense / psu_gain
            print 'current：', current
            cal_current = self._calibration.cal_mi(psu, current_range, current)
            print 'cal_current:', cal_current, current_range
            print 'MI range:', current_range

            # cal_current = current
            return [0, cal_current]
        except Exception as e:
            return [-1]

    def iPolling(self, loc, durations, hertz):
        assert loc in CURRENT_LOC
        assert isinstance(durations, int)
        assert isinstance(hertz, int)
        try:
            # identify different current range
            current_range = self._psu1.current_range if loc == A1 else self._psu2.current_range
            r_sense = PSU1BoardDef.R_SENSE[current_range] if loc == A1 else PSU2BoardDef.R_SENSE[current_range]
            dvm_input = CURRENT_LOC[loc][current_range]
            dvm_gain = GAIN_TYPE[loc][current_range]
            self._dvm.set_input(dvm_input)
            self._dvm.set_gain(dvm_gain)
            volt = self._dvm.measure_voltage(hertz, durations/1000.0)
            current = volt / r_sense / 10.0
            psu = 0 if loc == A1 else 1
            cal_current = self._calibration.cal_mi(psu, current_range, current)
            return [0, cal_current]
        except Exception as e:
            return [-1]
