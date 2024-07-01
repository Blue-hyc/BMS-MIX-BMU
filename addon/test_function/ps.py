import time

from ..driver.module.psu1_board import *
from ..driver.module.psu2_board import *


PS1 = 'ps_loc1'
PS2 = 'ps_loc2'
PS3 = 'ps_ntc'

LOC = (PS1, PS2, PS3)


class PS(object):

    rpc_public_api = ['fv', 'fi', 'reset']

    def __init__(self, xobjects):
        self._psu = {PS1: xobjects['psu1'], PS2: xobjects['psu2'], PS3: xobjects['psu2']}
        self._calibration = xobjects['calibration']
        self._transition = xobjects['transition']
        self._psu[PS1].restore()
        self._psu[PS2].restore()

    def fv(self, loc, volt, i_limit):
        assert loc in LOC
        assert isinstance(volt, float) or isinstance(volt, int)
        assert isinstance(i_limit, float) or isinstance(i_limit, int)
        try:
            current_range = self._psu[loc].range(i_limit)
            if i_limit <= 0.0011:
                current_range = 4
            if current_range < 0:
                return [-1]
            psu = 0 if loc == PS1 else 1
            cal_volt = self._calibration.cal_fv(psu, current_range, volt)
            print 'FV', cal_volt, i_limit
            # cal_volt = volt
            self._psu[loc].fv(cal_volt, i_limit, current_range)
            # time.sleep(0.1)
            return [0]
        except Exception as e:
            return [-1]

    def fi(self, loc, current, v_limit):
        assert loc in LOC
        assert isinstance(current, float) or isinstance(current, int)
        assert isinstance(v_limit, float) or isinstance(v_limit, int)
        try:
            current_range = self._psu[loc].range(current)
            print 'current_range_def:',  current_range
            if current <= 0.005:
                self._transition.set_pin(0, 11, 0)  # Remove PS3 capacitor when the current is less than 0.005A
            if current < 0.000005:
                current_range = PSU2BoardDef.CURRENT_RANGE_5uA
            elif 0.0001 <= current < 0.0003:
                current_range = PSU2BoardDef.CURRENT_RANGE_2_5mA
            elif 0.0005 <= current < 0.025:
                current_range = PSU2BoardDef.CURRENT_RANGE_25mA
            elif 0.03 <= current < 0.95:
                current_range = PSU2BoardDef.CURRENT_RANGE_1A
            elif 0.95 <= current < 4.0:
                current_range = PSU2BoardDef.CURRENT_RANGE_4A
            if current_range < 0:
                return [-1]
            psu = 0 if loc == PS1 else 1
            cal_current = self._calibration.cal_fi(psu, current_range, current)
            print 'ps.fi:', current, v_limit, current_range
            # cal_current = current
            if -1 == self._psu[loc].fi(cal_current, v_limit, current_range):
                return [-1]
            # time.sleep(0.1)
            self._psu[loc].output(True)
            if current_range == 0:
                time.sleep(1)
            return [0]
        except Exception as e:
            return [-1]

    def reset(self, loc):
        assert loc in LOC
        try:
            self._psu[loc].restore()
            return [0]
        except Exception as e:
            return [-1]
