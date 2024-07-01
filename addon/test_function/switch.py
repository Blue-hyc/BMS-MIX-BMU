import time

from ..driver.module.transition_board import *
from ..driver.module.psu2_board import *
import pdb

SW1 = 'sw.Cp2Cn'
SW2 = 'sw.Cn2Pn'
SW2_1 = 'sw.Pn2Cn'
SW3 = 'sw.Cp2Pp'
SW3_1 = 'sw.Pp2Cp'
SW4 = 'sw.Pp2Pn'
SW4_1 = 'sw.Pn2Pp'
SW4_2 = 'sw.Pp2Pn_S'
SW4_3 = 'sw.Pp2Pn_F'
SW4_4 = 'sw.Pp2Pn_R'
SW5 = 'sw.Cn2Pn_short'
SW6 = 'sw.Cp_sns2Cn_sns'
SW7 = 'sw.Cp2Tp'
SW8 = 'sw.Cp2Tp_R'
SW9 = 'sw.Cn2Cn_sns'
SW9_1 = 'sw.Cn_sns2Cn'
SW10 = 'sw.Cp2Cp_sns'
SW10_1 = 'sw.Cp_sns2Cp'
SW11 = 'sw.Cp_Tp3'
SW11_1 = 'sw.Tp3_Cp'
SW12 = 'sw.Pp_Tp3'
SW12_1 = 'sw.Tp3_Pp'
SW13 = 'sw.Cp_Tp3_short'
SW14 = 'sw.Pp_Tp3_short'
SW15 = 'sw.Pn_SCL'
SW15_1 = 'sw.Pn_SDA'
SW16 = 'sw.Pp_Tp4'
SW16_1 = 'sw.ntc_Pn'
SW16_2 = 'sw.SDA_Pn'
SW16_3 = 'sw.SCL_Pn'
SW16_4 = 'sw.Pp_Tp4_sns'

SWITCH = {
    SW1:    TransitionBoardDef.SWITCH_PS1_CELL_POS_CELL_NEG,
    SW2:    TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG,
    SW2_1:  TransitionBoardDef.SWITCH_PS2_PACK_NEG_CELL_NEG,
    SW3:    TransitionBoardDef.SWITCH_PS3_CELL_POS_PACK_POS,
    SW3_1:  TransitionBoardDef.SWITCH_PS3_PACK_POS_CELL_POS,
    SW4:    TransitionBoardDef.SWITCH_PS4_SENSE,
    SW4_1:  TransitionBoardDef.SWITCH_None,
    SW4_2:  TransitionBoardDef.SWITCH_PS4_SENSE,
    SW4_3:  TransitionBoardDef.SWITCH_None,
    SW4_4:  TransitionBoardDef.SWITCH_DISCHARGE_REGISTER,
    SW5:    TransitionBoardDef.SWITCH_PS1_CELL_NEG_PACK_NEG,
    SW6:    TransitionBoardDef.SWITCH_EXT_MV_CELL_SNS,
    SW7:    TransitionBoardDef.SWITCH_SEC_NTC,
    SW8:    TransitionBoardDef.SWITCH_35K,
    SW9:    TransitionBoardDef.SWITCH_PS3_PTC_CELL_NEG_CELL_NEG_SNS,
    SW9_1:  TransitionBoardDef.SWITCH_PS3_PTC_CELL_NEG_SNS_CELL_NEG,
    SW10:   TransitionBoardDef.SWITCH_PS3_PTC_CELL_POS_CELL_POS_SNS,
    SW10_1: TransitionBoardDef.SWITCH_PS3_PTC_CELL_POS_SNS_CELL_POS,
    SW11:   TransitionBoardDef.SWITCH_CELL_POS_TP3,
    SW11_1: TransitionBoardDef.SWITCH_TP3_CELL_POS,
    SW12:   TransitionBoardDef.SWITCH_PACK_POS_TP3,
    SW12_1: TransitionBoardDef.SWITCH_TP3_PACK_POS,
    SW13:   TransitionBoardDef.SWITCH_CELL_POS_TP3_SHORT,
    SW14:   TransitionBoardDef.SWITCH_PACK_POS_TP3_SHORT,
    SW15:   TransitionBoardDef.SWITCH_PACK_NEG_SCL,
    SW15_1: TransitionBoardDef.SWITCH_PACK_NEG_SDA,
    SW16:   TransitionBoardDef.SWITCH_PTC1,
    SW16_1: TransitionBoardDef.SWITCH_NTC3,
    SW16_2: TransitionBoardDef.SWITCH_EXT_MV_SDA,
    SW16_3: TransitionBoardDef.SWITCH_EXT_MV_SCL,
    SW16_4: TransitionBoardDef.SWITCH_EXT_MV_PACK_POS_TP4_SNS

}


class Switch(object):

    rpc_public_api = ['set', 'get']

    def __init__(self, xobjects):
        self._transition = xobjects['transition']
        self._psu2 = xobjects['psu2']

    def set(self, loc, state):
        assert loc in SWITCH
        assert state in ('ON', 'OFF')

        if loc == 'sw.Cp2Pp' and state == 'ON':
            # discharge cap
            self._transition.set_pin(0, 11, 1)
            self._transition.set_pin(0, 36, 1)
            self._psu2.fv(0, 0.1, 5)
            time.sleep(0.8)
            self._transition.set_pin(0, 11, 0)
            self._transition.set_pin(0, 36, 0)
            self._psu2.restore()
            time.sleep(0.05)
            print 'discharge cap -- switch'

        try:
            switch = SWITCH[loc]
            state = TransitionBoardDef.SWITCH_STATE_ON if state == 'ON' else TransitionBoardDef.SWITCH_STATE_OFF
            print 'switch_set:', loc, state
            if self._transition.test_item == 'scp' and loc == 'sw.Pp_Tp3' and state == 1:
                self._transition.set_switch(34, 1)
                self._transition.test_item = 'normal'
            else:
                self._transition.set_switch(switch, state)
            if loc == 'sw.Pn_SDA':
                if state == 1:
                    self._transition.test_item = 'PTC2'
            if loc == 'sw.Pn_SCL':
                if state == 1:
                    self._transition.test_item = 'PTC3'
            if loc == 'sw.ntc_Pn' and state == 1:
                self._transition.test_item = 'ntc'
            if loc == 'sw.SDA_Pn' or loc == 'sw.SCL_Pn':
                time.sleep(0.1)
            if loc == 'sw.Pp_Tp3_short' and state == 1:
                print 'short'
                pass
            if loc == 'sw.Cn2Pn' or loc == 'sw.Pn2Cn':
                if state == 0:
                    self._psu2.fv(0, 0.01, 3)
                    # self._transition.set_pin(0, 11, 1)
                    time.sleep(0.15)
                    # self._transition.set_pin(0, 11, 0)
            if loc == 'sw.Cp2Pp' or loc == 'sw.Pp2Cp' or loc == 'sw.Tp3_Pp' or loc == 'sw.Cp_Tp3' or loc == 'sw.Tp3_Cp':
                if state == 0:
                    self._psu2.fv(0, 0.01, 3)
                    # self._transition.set_pin(0, 11, 1)
                    time.sleep(0.05)
                    # self._transition.set_pin(0, 11, 0)
            return [0]
        except Exception as e:
            return [-1]

    def get(self, loc):
        assert loc in SWITCH
        try:
            switch = SWITCH[loc]
            state = 'ON' if TransitionBoardDef.SWITCH_STATE_ON == self._transition.get_switch(switch) else 'OFF'
            return [0, state]
        except Exception as e:
            return [-1]
