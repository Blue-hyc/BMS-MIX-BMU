from ..driver.module.dvm_board import *
from ..driver.module.psu1_board import *
from ..driver.module.psu2_board import *
from mix.driver.smartgiant.common.ipcore.mix_widthmeasure_sg import *
import time
import thread


class Combo(object):

    rpc_public_api = ['OvpUvp', 'OverI', 'OverIrelease', 'otp', 'ptc']

    def __init__(self, xobjects):
        self._psu1 = xobjects['psu1']
        self._psu2 = xobjects['psu2']
        self._dvm = xobjects['dvm']
        self._transition = xobjects['transition']
        self._calibration = xobjects['calibration']
        self._width_measure = xobjects['width_measure']
        self._counter = 0
        thread.start_new_thread(self.tick, (0,))

    def OvpUvp(self, volt, v_threshold, timeout, test_type):
        assert isinstance(volt, float) or isinstance(volt, int)
        assert isinstance(v_threshold, float) or isinstance(v_threshold, int)
        assert isinstance(timeout, int)
        assert test_type in ['protection', 'release']
        try:
            self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            v_final = 0.0
            print 'ovp volt', volt
            cal_volt = self._calibration.cal_fv(0, PSU1BoardDef.CURRENT_RANGE_25mA, volt)
            delay_time = timeout
            # self._psu1.fv(cal_volt, 0.02, PSU1BoardDef.CURRENT_RANGE_25mA)
            # if 4.23 < volt < 4.24:
            #     time.sleep(1)
            self._psu1._ad5560.set_dac(cal_volt)
            self._counter = 0
            record = time.time()
            while (1.0 * self._counter) < timeout:
                v_final = self._dvm.measure_voltage(1000, 0.01)
                # print 'v_final', v_final
                if test_type == 'protection':
                    if v_final > v_threshold:
                        counter = time.time()
                        delay_time = int((counter - record) * 1000)
                        break
                else:
                    if abs(v_final) < v_threshold:
                        counter = time.time()
                        delay_time = int((counter - record) * 1000)
                        break
            # self._psu2.output(False)
        except Exception as e:
            return [-1]
        return [0, v_final, delay_time]

    def OverI(self, current, v_limit, i_start, i_threshhold, timeout):
        assert isinstance(current, float) or isinstance(current, int)
        assert isinstance(v_limit, float) or isinstance(v_limit, int)
        assert isinstance(i_start, float) or isinstance(i_start, int)
        assert isinstance(i_threshhold, float) or isinstance(i_threshhold, int)
        assert isinstance(timeout, int)
        try:
            self._psu2.comparer = 0.90
            self._dvm.set_input(DVMBoardDef.PSU2_HC_2)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_6_P_4)
            self._width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
            current_range = PSU2BoardDef.CURRENT_RANGE_4A
            cal_current = self._calibration.cal_fi(1, current_range, current)
            self._psu2.fi(cal_current, v_limit, current_range)
            self._width_measure.start_measure()
            self._psu2.output(True)
            #  Due to the function 'sleep' may not be so accuracy, add 0.5ms delay here to make the width_measure has
            #  enough time to catch falling and rising of the CPOH.
            time.sleep(timeout/1000000.0+0.001)
            rd = self._width_measure.get_width()
            # i_final = self._dvm.measure_voltage(1000, 0.01) / PSU2BoardDef.R_SENSE[current_range]
            self._psu2.output(False)
            self._width_measure.stop_measure()
            delay_time = timeout / 1000.0
            i_final = current
            if len(rd) != 0:
                for each in rd:
                    delay_time = each.width / 1000000.0
                    if delay_time < 8.0:
                        delay_time = timeout / 1000.0
                        continue
                    else:
                        i_final = 0.0
                        break
            self._psu2.comparer = 0.90
            return [0, i_final, delay_time]
        except Exception as e:
            return [-1]

    # def OverI(self, current, v_limit, i_start, i_threshhold, timeout):
    #     assert isinstance(current, float) or isinstance(current, int)
    #     assert isinstance(v_limit, float) or isinstance(v_limit, int)
    #     assert isinstance(i_start, float) or isinstance(i_start, int)
    #     assert isinstance(i_threshhold, float) or isinstance(i_threshhold, int)
    #     assert isinstance(timeout, int)
    #     dvm_gain = DVMBoardDef.DVM_GAIN_6_P_4
    #     dvm_input = DVMBoardDef.PSU2_HC_1
    #     self._dvm.set_input(dvm_input)
    #     self._dvm.set_gain(dvm_gain)
    #     self._width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
    #     current_range = PSU2BoardDef.CURRENT_RANGE_2A
    #     cal_current = self._calibration.cal_fi(1, current_range, current)
    #     self._psu2.fi(cal_current, v_limit, current_range)
    #     self._width_measure.start_measure()
    #     self._psu2.output(True)
    #     #  Due to the function 'sleep' may not be so accuracy, add 0.5ms delay here to make the width_measure has enough
    #     #  time to catch falling and rising of the CPOH.
    #     time.sleep(timeout/1000000.0+0.0005)
    #     rd = self._width_measure.get_width()
    #     i_final = self._dvm.measure_voltage(1000, 0.003) / PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_2A]
    #     self._psu2.output(False)
    #     i_final = self._calibration.cal_mi(1, current_range, i_final)
    #     self._width_measure.stop_measure()
    #     delay_time = timeout / 1000.0
    #     if len(rd) != 0:
    #         for each in rd:
    #             delay_time = each.width / 1000000.0
    #             if delay_time < 2.0:
    #                 delay_time = timeout / 1000.0
    #                 continue
    #             i_final = 0.0
    #             # time.sleep(0.6)
    #             break
    #     return [0, i_final, delay_time]

    def tick(self, val):
        while True:
            time.sleep(0.001)
            self._counter += 1

    def OverIrelease(self, v_set, v_threshold, i_limit, timeout):
        assert isinstance(v_set, float) or isinstance(v_set, int)
        assert isinstance(v_threshold, float) or isinstance(v_threshold, int)
        assert isinstance(i_limit, float) or isinstance(i_limit, int)
        assert isinstance(timeout, int)
        try:
            v_threshold = abs(0.5 * v_set)
            self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            record = 0
            step = 0
            v_final = 0.0
            self._psu2.fv(v_set, i_limit, PSU2BoardDef.CURRENT_RANGE_1A)
            delay_time = timeout
            self._counter = 0
            while (1.0 * self._counter) < timeout:
                v_final = abs(self._dvm.measure_voltage(1000, 0.01))
                if step == 0:
                    if v_final > v_threshold:
                        record = self._counter
                        step = 1
                    continue
                if v_final < v_threshold:
                    delay_time = 1.0 * (self._counter - record)
                    break
            return [0, v_final, delay_time]
        except Exception as e:
            return [-1]

    def otp(self, v_threshold, timeout):
        assert isinstance(v_threshold, float)
        assert isinstance(timeout, int)
        try:
            v_threshold = abs(v_threshold)
            self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            delay_time = timeout
            self._transition.set_switch(TransitionBoardDef.SWITCH_35K, 1)
            self._counter = 0
            while (1.0 * self._counter) < timeout:
                v_final = self._dvm.measure_voltage(1000, 0.01)
                v_final = abs(v_final)
                if v_final > v_threshold:
                    delay_time = 1.0 * self._counter
                    break
            return [0, v_final, delay_time]
        except Exception as e:
            return [-1]

    def ptc(self, v_set, i_limit, duration, hertz):
        assert isinstance(v_set, float)
        assert isinstance(duration, float)
        assert isinstance(i_limit, float)
        assert isinstance(hertz, int)
        v_final = 0.0
        i1 = 0.0
        i2 = 0.0
        return [0, v_final, i1, i2]
