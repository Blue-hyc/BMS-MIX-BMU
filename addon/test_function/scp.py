from mix.addon.driver.module.psu2_board import *
from mix.driver.smartgiant.common.ipcore.mix_widthmeasure_sg import *
from mix.addon.driver.module.transition_board import *


class SCP(object):

    rpc_public_api = ['prim', 'sec']

    def __init__(self, xobjects):
        self._psu2 = xobjects['psu2']
        self._dvm = xobjects['dvm']
        self._transition = xobjects['transition']
        self._calibration = xobjects['calibration']
        self._width_measure = xobjects['width_measure']

    def prim(self, usl, lsl):
        assert isinstance(usl, float) or isinstance(usl, int)
        assert isinstance(lsl, float) or isinstance(lsl, int)
        try:
            self._psu2.comparer = 0.6
            self._transition.test_item = 'scp'
            cal_lsl = self._calibration.cal_fi(1, PSU2BoardDef.CURRENT_RANGE_10A, lsl)
            self._psu2.fi(cal_lsl, 1, PSU2BoardDef.CURRENT_RANGE_10A)
            self._width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
            self._width_measure.start_measure()
            self._psu2.output(True)
            time.sleep(0.0007)
            rd = self._width_measure.get_width()
            self._psu2.output(False)
            self._width_measure.stop_measure()
            if len(rd) != 0:
                for each in rd:
                    delay_time = each.width / 1000000.0
                    if delay_time < 0.15:
                        continue
                    else:
                        return [0, lsl, delay_time]
            cal_usl = self._calibration.cal_fi(1, PSU2BoardDef.CURRENT_RANGE_10A, usl+0.2)
            self._psu2.fi(cal_usl, 1, PSU2BoardDef.CURRENT_RANGE_10A)
            self._width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
            self._width_measure.start_measure()
            self._transition.set_pin(0, 11, 0)
            self._psu2.output(True)
            time.sleep(0.001)
            rd = self._width_measure.get_width()
            self._psu2.output(False)
            trip_point = 0.0
            delay_time = 1.0
            if len(rd) != 0:
                for each in rd:
                    delay = each.width / 1000000.0
                    if delay < 0.15:
                        continue
                    else:
                        trip_point = usl
                        delay_time = delay
                        break
            self._width_measure.stop_measure()
            self._psu2.comparer = 0.9
        except Exception as e:
            return [-1]
        return [0, trip_point, delay_time]

    def sec(self, usl, lsl):
        assert isinstance(usl, float) or isinstance(usl, int)
        assert isinstance(lsl, float) or isinstance(lsl, int)
        self._psu2.comparer = 0.8
        cal_lsl = self._calibration.cal_fi(1, PSU2BoardDef.CURRENT_RANGE_10A, lsl)
        self._psu2.fi(cal_lsl, 3, PSU2BoardDef.CURRENT_RANGE_10A)
        self._width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
        self._width_measure.start_measure()
        self._psu2.output(True)
        time.sleep(0.0007)
        rd = self._width_measure.get_width()
        self._psu2.output(False)
        self._width_measure.stop_measure()
        if len(rd) != 0:
            for each in rd:
                delay_time = each.width / 1000000.0
                if delay_time < 0.15:
                    continue
                else:
                    return [0, lsl, delay_time]
        cal_usl = self._calibration.cal_fi(1, PSU2BoardDef.CURRENT_RANGE_10A, usl)
        self._psu2.fi(cal_usl, 3, PSU2BoardDef.CURRENT_RANGE_10A)
        self._width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
        self._width_measure.start_measure()
        self._transition.set_pin(0, 11, 0)
        self._psu2.output(True)
        time.sleep(0.001)
        rd = self._width_measure.get_width()
        self._psu2.output(False)
        trip_point = 0.0
        delay_time = 1.0
        if len(rd) != 0:
            for each in rd:
                delay = each.width / 1000000.0
                if delay < 0.15:
                    continue
                else:
                    trip_point = usl
                    delay_time = delay
                    break
        self._width_measure.stop_measure()
        self._psu2.comparer = 0.9
        return [0, trip_point, delay_time]
