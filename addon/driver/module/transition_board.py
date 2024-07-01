# -*- coding: utf-8 -*-
from ..ic.pca9506 import *
from ..ic.tmp117 import *
# from mix.driver.core.ic.cat9555 import *
from mix.driver.core.bus.i2c_ds_bus import *
from mix.driver.core.ic.tca9548 import *
from mix.addon.driver.ic.tpl0401x import TPL0401x, TPL0401xDef
from mix.driver.core.ic.cat24cxx import CAT24C32


__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class TransitionBoardDef:
    SWITCH_None = 9999
    SWITCH_PS1_CELL_POS_CELL_NEG = 0
    SWITCH_PS1_CELL_NEG_PACK_NEG = 1
    SWITCH_PS2_CELL_NEG_PACK_NEG = 2
    SWITCH_PS2_PACK_NEG_CELL_NEG = 3
    SWITCH_PS3_CELL_POS_PACK_POS = 4
    SWITCH_PS3_PACK_POS_CELL_POS = 5
    SWITCH_PS4_PACK_POS_NEG = 6
    SWITCH_PS4_FORCE = 7
    SWITCH_PS4_SENSE = 8
    SWITCH_DISCHARGE_REGISTER = 9
    SWITCH_SEC_NTC = 10
    SWITCH_35K = 11
    SWITCH_PS3_PTC_CELL_POS_SNS_CELL_POS = 12
    SWITCH_PS3_PTC_CELL_POS_CELL_POS_SNS = 13
    SWITCH_PS3_PTC_CELL_NEG_CELL_NEG_SNS = 14
    SWITCH_PS3_PTC_CELL_NEG_SNS_CELL_NEG = 15
    SWITCH_EXT_MV_CELL = 16
    SWITCH_EXT_MV_PACK = 17
    SWITCH_EXT_MV_CELL_SNS = 18
    SWITCH_PS1_CELL_POS_CELL_NEG_SHUT_DOWN = 19
    SWITCH_CAL_PS1 = 20
    SWITCH_CAL_PS1_I = 21
    SWITCH_CAL_PS1_nA = 22
    SWITCH_CAL_PS3 = 23
    SWITCH_CAL_PS3_I = 24
    SWITCH_CAL_PS3_uA = 42

    SWITCH_CELL_POS_TP3 = 25
    SWITCH_PACK_POS_TP3 = 26
    SWITCH_PACK_POS_TP3_SCP = 34
    SWITCH_CELL_POS_TP3_SHORT = 27
    SWITCH_PACK_POS_TP3_SHORT = 28

    SWITCH_TP3_CELL_POS = 29
    SWITCH_TP3_PACK_POS = 30
    SWITCH_CELL_POS_TP3_A = 31
    SWITCH_CELL_POS_TP3_B = 32
    SWITCH_CELL_POS_TP3_C = 33
    SWITCH_CAL_PS1_uA = 35

    SWITCH_PACK_NEG_SCL = 36
    SWITCH_PACK_NEG_SDA = 37
    SWITCH_EXT_MV_SCL = 38
    SWITCH_EXT_MV_SDA = 39
    SWITCH_PTC1 = 40
    SWITCH_NTC3 = 41
    SWITCH_EXT_MV_PACK_POS_TP4_SNS = 43

    SWITCH_STATE_ON = 1
    SWITCH_STATE_OFF = 0

    BMU_TRAN = 1
    PACK_TRAN = 0

    WATCH_SWITCH_LIST = {
        SWITCH_PS1_CELL_POS_CELL_NEG: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[0, 1], [1, 1], [2, 1], [15, 0]],
                PACK_TRAN: []
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[0, 0], [1, 0], [2, 0], [15, 1]],
                PACK_TRAN: []
            }
        },
        SWITCH_PS2_CELL_NEG_PACK_NEG: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[6, 0], [3, 0]],
                PACK_TRAN: [[3, 0], [5, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[6, 1], [3, 0]],
                PACK_TRAN: [[3, 1], [5, 1], [11, 1], [36, 1]]
            }
        },
        SWITCH_PS2_PACK_NEG_CELL_NEG: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[7, 0], [4, 0]],
                PACK_TRAN: [[2, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[7, 1], [4, 0]],
                PACK_TRAN: [[2, 1], [11, 1], [36, 1]]
            }
        },
        SWITCH_PS3_CELL_POS_PACK_POS: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[3, 0], [4, 0]],
                PACK_TRAN: [[1, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[3, 1], [4, 0]],
                PACK_TRAN: [[1, 1], [11, 1], [36, 1]]
            }
        },
        SWITCH_PS3_PACK_POS_CELL_POS: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[4, 0], [7, 0]],
                PACK_TRAN: [[4, 0], [0, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[4, 1], [7, 0]],
                PACK_TRAN: [[4, 1], [0, 1], [11, 1], [36, 1]]
            }
        },
        # SWITCH_PS4_PACK_POS_NEG: {
        #     SWITCH_STATE_OFF: [[6, 0], [12, 0], [30, 0]],
        #     SWITCH_STATE_ON:  [[6, 1], [12, 1], [30, 1]]
        # },
        # SWITCH_PS4_FORCE: {
        #     SWITCH_STATE_OFF: [[6, 0], [12, 0]],
        #     SWITCH_STATE_ON:  [[6, 1], [12, 1]]
        # },
        SWITCH_SEC_NTC: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[3, 0], [10, 0]],
                PACK_TRAN: [[11, 0], [36, 0]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[3, 1], [10, 1]],
                PACK_TRAN: [[11, 0], [36, 0]]
            }
        },
        SWITCH_35K: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[9, 0]],
                PACK_TRAN: []
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[9, 1]],
                PACK_TRAN: []
            }
        },
        SWITCH_PS4_SENSE: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[6, 0]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[6, 1]]
            }
        },
        SWITCH_DISCHARGE_REGISTER: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[10, 0]]
            },
            SWITCH_STATE_ON:  {
                BMU_TRAN: [],
                PACK_TRAN: [[10, 1]]
            }
        },
        SWITCH_CELL_POS_TP3: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[3, 0], [12, 0]],
                PACK_TRAN: [[11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[3, 1], [12, 1]],
                PACK_TRAN: [[11, 1], [36, 1]]
            }
        },
        # SWITCH_CELL_POS_TP3_A: {
        #     SWITCH_STATE_OFF: [[4, 0], [8, 1], [14, 0], [24, 0], [30, 0]],
        #     SWITCH_STATE_ON: [[4, 1], [8, 1], [14, 0], [24, 1], [30, 1]]
        # },
        # SWITCH_CELL_POS_TP3_B: {
        #     SWITCH_STATE_OFF: [[4, 0], [8, 1], [14, 0], [25, 0], [30, 0]],
        #     SWITCH_STATE_ON: [[4, 1], [8, 1], [14, 0], [25, 1], [30, 1]]
        # },
        # SWITCH_CELL_POS_TP3_C: {
        #     SWITCH_STATE_OFF: [[4, 0], [8, 1], [14, 0], [26, 0], [30, 0]],
        #     SWITCH_STATE_ON: [[4, 1], [8, 1], [14, 0], [26, 1], [30, 1]]
        # },
        SWITCH_TP3_CELL_POS: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[4, 0], [11, 0]],
                PACK_TRAN: [[11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[4, 1], [11, 1]],
                PACK_TRAN: [[11, 1], [36, 1]]
            }
        },
        SWITCH_PACK_POS_TP3: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[12, 0]],
                PACK_TRAN: [[0, 0], [4, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[12, 1]],
                PACK_TRAN: [[0, 1], [4, 1], [11, 1], [36, 1]]
            }
        },
        SWITCH_PACK_POS_TP3_SCP: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[12, 0]],
                PACK_TRAN: [[0, 0], [4, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[12, 1]],
                PACK_TRAN: [[0, 1], [4, 1], [11, 0], [36, 0]]
            }
        },
        SWITCH_TP3_PACK_POS: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[11, 0]],
                PACK_TRAN: [[1, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[11, 1]],
                PACK_TRAN: [[1, 1], [11, 1], [36, 1]]
            }
        },
        SWITCH_CELL_POS_TP3_SHORT: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[13, 0]],
                PACK_TRAN: []
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[13, 1]],
                PACK_TRAN: []
            }
        },
        SWITCH_PACK_POS_TP3_SHORT: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[14, 0]],
                PACK_TRAN: []
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[14, 1]],
                PACK_TRAN: []
            }
        },
        SWITCH_PACK_NEG_SDA: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 1], [29, 0], [2, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 0], [29, 1], [2, 1], [11, 0], [36, 0]]
            }
        },
        SWITCH_PACK_NEG_SCL: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 1], [30, 0], [2, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 0], [30, 1], [2, 1], [11, 0], [36, 0]]
            }
        },
        SWITCH_EXT_MV_SDA: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 1], [9, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 0], [9, 1], [11, 0], [36, 0]]
            }
        },
        SWITCH_EXT_MV_SCL: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 1], [8, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[32, 0], [8, 1], [11, 0], [36, 0]]
            }
        },
        SWITCH_PTC1: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[16, 0], [17, 0]],
                PACK_TRAN: [[0, 0], [4, 0], [11, 1], [36, 1]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[16, 1], [17, 1]],
                PACK_TRAN: [[0, 1], [4, 1], [11, 0], [36, 0]]
            }
        },
        SWITCH_NTC3: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [],
                PACK_TRAN: [[28, 0], [5, 0], [3, 0], [11, 1], [34, 0]]
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[28, 1], [5, 1], [3, 1], [11, 0], [34, 0]]
            }
        },
        SWITCH_EXT_MV_PACK_POS_TP4_SNS: {
            SWITCH_STATE_OFF: {
                BMU_TRAN: [[22, 0]],
                PACK_TRAN: []
            },
            SWITCH_STATE_ON: {
                BMU_TRAN: [[22, 1]],
                PACK_TRAN: []
            }
        },
        SWITCH_CAL_PS1: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [[0, 0], [1, 0], [2, 0], [19, 1], [20, 1]],             # PS1_CELL_CAL
                PACK_TRAN: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                            [11, 0], [12, 0], [13, 0], [22, 0], [23, 0], [24, 0], [25, 1], [26, 1], [27, 0], [28, 0],
                            [29, 0], [30, 0], [31, 0], [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0]]
            }
        },
        SWITCH_CAL_PS1_I: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [[0, 0], [1, 0], [2, 0], [19, 1], [20, 1]],
                PACK_TRAN: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                              [11, 0], [12, 0], [13, 0], [22, 1], [23, 0], [24, 0], [25, 0], [26, 1], [27, 0], [28, 0],
                              [29, 0], [30, 0], [31, 0], [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0]]
            }
        },
        SWITCH_CAL_PS1_nA: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [[0, 0], [1, 0], [2, 0], [19, 1], [20, 1]],
                PACK_TRAN: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                              [11, 0], [12, 0], [13, 0], [22, 0], [23, 0], [24, 1], [25, 0], [26, 1], [27, 0], [28, 0],
                              [29, 0], [30, 0], [31, 0], [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0]]
            }
        },
        SWITCH_CAL_PS1_uA: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [[0, 0], [1, 0], [2, 0], [19, 1], [20, 1]],
                PACK_TRAN: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                              [11, 0], [12, 0], [13, 0], [22, 0], [23, 1], [24, 0], [25, 0], [26, 1], [27, 0], [28, 0],
                              [29, 0], [30, 0], [31, 0], [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0]]
            }
        },
        SWITCH_CAL_PS3: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[0, 1], [1, 0], [2, 0], [3, 1], [4, 1], [5, 1], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                            [11, 1], [12, 0], [13, 0], [22, 0], [23, 0], [24, 0], [25, 1], [26, 1], [28, 0], [29, 0],
                            [30, 0], [31, 0], [34, 0], [35, 0]]
            }
        },
        SWITCH_CAL_PS3_I: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[0, 1], [1, 0], [2, 0], [3, 1], [4, 1], [5, 1], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                            [11, 1], [12, 0], [13, 0], [22, 1], [23, 0], [24, 0], [25, 0], [26, 1], [28, 0], [29, 0],
                            [30, 0], [31, 0], [34, 0], [35, 0], [36, 1]]
            }
        },
        SWITCH_CAL_PS3_uA: {
            SWITCH_STATE_ON: {
                BMU_TRAN: [],
                PACK_TRAN: [[0, 1], [1, 0], [2, 0], [3, 1], [4, 1], [5, 1], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                            [11, 0], [12, 0], [13, 0], [22, 1], [23, 0], [24, 0], [25, 0], [26, 1], [28, 0], [29, 0],
                            [30, 0], [31, 0], [34, 0], [35, 0], [36, 0]]
            }
        }
    }

    SWITCH_RESET_STATE = {
        BMU_TRAN: [[0, 1], [1, 1], [2, 1], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                   [11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0],
                   [21, 0], [22, 0], [23, 0], [24, 0], [25, 0], [26, 0], [27, 0], [28, 0], [29, 0], [30, 0],
                   [31, 0], [32, 0], [33, 0], [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0]],
        PACK_TRAN: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                    [11, 1], [12, 0], [13, 0], [22, 0], [23, 0], [24, 0], [25, 0], [26, 0], [28, 0], [29, 0],
                    [30, 0], [31, 0], [32, 1], [33, 1], [34, 0], [35, 0], [36, 0], [37, 0], [38, 0], [39, 0]]
        }

    I2C_PULL_UP_1K = 'pull_up_1k'
    I2C_PULL_UP_2_2K = 'pull_up_2.2k'
    I2C_PULL_UP_4_7K = 'pull_up_4.7k'
    I2C_PULL_UP_47K = 'pull_up_47k'
    I2C_PULL_UP_NONE = 'pull_up_cutoff'

    EXP_GPO_CAP = 8
    EXP_GPO_TVS = 9
    DUT_GND_EN = 10

    I2C_SWITCH_LIST = {
        I2C_PULL_UP_1K: [[14, 1], [15, 0], [16, 0], [17, 0], [18, 1], [19, 0], [20, 0], [21, 0], [27, 1]],
        I2C_PULL_UP_2_2K: [[14, 0], [15, 1], [16, 0], [17, 0], [18, 0], [19, 1], [20, 0], [21, 0], [27, 1]],
        I2C_PULL_UP_4_7K: [[14, 0], [15, 0], [16, 1], [17, 0], [18, 0], [19, 0], [20, 1], [21, 0], [27, 1]],
        I2C_PULL_UP_47K: [[14, 0], [15, 0], [16, 0], [17, 1], [18, 0], [19, 0], [20, 0], [21, 1], [27, 1]],
        I2C_PULL_UP_NONE: [[14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [27, 1]]
    }

    VOLTAGE_OVERSHOOT_SWITCH = {
        EXP_GPO_CAP: {
                         SWITCH_STATE_OFF: [[13, 0]],
                         SWITCH_STATE_ON: [[13, 1]]
                     },
        EXP_GPO_TVS: {
                         SWITCH_STATE_OFF: [[5, 0]],
                         SWITCH_STATE_ON: [[5, 1]]
                     },
    }

    PULL_UP_VOLTAGE_CONFIG = {
        1.2: 2.42,
        1.8: 3.59,
        3.3: 6.62,
        5: 9.92
    }


class TransitionBoard(object):

    rpc_public_api = ['set_switch', 'get_switch', 'set_pin', 'get_pin', 'reset_all_switch', 'set_dut_pull_up_voltage',
                      'set_dut_pull_up', 'set_voltage_overshoot_switch']

    def __init__(self, i2c_bus=None):
        self._tpl0401 = TPL0401x(0x3E, i2c_bus)
        # self._cat9555 = CAT9555(0x24, i2c_bus)
        self._pca9506_pack = PCA9506(None, 0x21, i2c_bus)
        self._pca9506_bmu = PCA9506(None, 0x22, i2c_bus)
        self._tpl0401.set_resistance(2.42)
        # for i in range(16):
        #     self._cat9555.set_pin_dir(i, 'output')
        self.set_dut_pull_up(TransitionBoardDef.I2C_PULL_UP_NONE)
        for i in range(40):
            self._pca9506_pack.set_pin_dir(i, 'output')
        for i in range(40):
            self._pca9506_bmu.set_pin_dir(i, 'output')
        self.test_item = 'normal'
        self.reset_all_switch()

    def set_dut_pull_up_voltage(self, volt):
        if 1.19 < volt < 1.21:
            volt = 1.2
        elif 1.79 < volt < 1.81:
            volt = 1.8
        assert volt in TransitionBoardDef.PULL_UP_VOLTAGE_CONFIG.keys()
        assume_resistance = TransitionBoardDef.PULL_UP_VOLTAGE_CONFIG[volt]
        self._tpl0401.set_resistance(assume_resistance)

    def set_pin(self, board, pin_id, level):
        if board == 0:
            self._pca9506_pack.set_pin(pin_id, level)
        if board == 1:
            self._pca9506_bmu.set_pin(pin_id, level)
        return [0]

    def get_pin(self, board, pin_id):
        if board == 0:
            level = self._pca9506_pack.get_pin(pin_id)
        if board == 1:
            level = self._pca9506_bmu.get_pin(pin_id)
        return [0, level]

    def set_switch(self, sw, state):
        assert sw in TransitionBoardDef.WATCH_SWITCH_LIST
        assert state in [TransitionBoardDef.SWITCH_STATE_ON, TransitionBoardDef.SWITCH_STATE_OFF]
        pack_pins_and_level = TransitionBoardDef.WATCH_SWITCH_LIST[sw][state][TransitionBoardDef.PACK_TRAN]
        bmu_pins_and_level = TransitionBoardDef.WATCH_SWITCH_LIST[sw][state][TransitionBoardDef.BMU_TRAN]
        # if len(pins_and_level) > 0:
        for each in pack_pins_and_level:
            self._pca9506_pack.set_pin(each[0], each[1])
        for each in bmu_pins_and_level:
            self._pca9506_bmu.set_pin(each[0], each[1])

            # scp cap discharge delay

    def get_switch(self, sw):
        assert sw in TransitionBoardDef.WATCH_SWITCH_LIST.keys()
        pack_pins_and_level = TransitionBoardDef.WATCH_SWITCH_LIST \
            [sw][TransitionBoardDef.SWITCH_STATE_ON][TransitionBoardDef.PACK_TRAN]
        bmu_pins_and_level = TransitionBoardDef.WATCH_SWITCH_LIST[sw] \
            [TransitionBoardDef.SWITCH_STATE_ON][TransitionBoardDef.BMU_TRAN]
        # if len(pins_and_level) == 0:
        # return TransitionBoardDef.SWITCH_STATE_OFF
        for each in pack_pins_and_level:
            level = self._pca9506_pack.get_pin(each[0])
            # return OFF directly once mismatch occurred.
            if level != each[1]:
                return TransitionBoardDef.SWITCH_STATE_OFF
        for each in bmu_pins_and_level:
            level = self._pca9506_bmu.get_pin(each[0])
            # return OFF directly once mismatch occurred.
            if level != each[1]:
                return TransitionBoardDef.SWITCH_STATE_OFF
        return TransitionBoardDef.SWITCH_STATE_ON

    def reset_all_switch(self):
        for each in TransitionBoardDef.SWITCH_RESET_STATE[0]:
            pin = each[0]
            level = each[1]
            self._pca9506_pack.set_pin(pin, level)
        for each in TransitionBoardDef.SWITCH_RESET_STATE[1]:
            pin = each[0]
            level = each[1]
            self._pca9506_bmu.set_pin(pin, level)

            # time.sleep(0.01)

    def set_dut_pull_up(self, pull_up):
        assert pull_up in TransitionBoardDef.I2C_SWITCH_LIST.keys()
        pins_and_level = TransitionBoardDef.I2C_SWITCH_LIST[pull_up]
        for each in pins_and_level:
            self._pca9506_pack.set_pin(each[0], each[1])

    def set_voltage_overshoot_switch(self, sw, state):
        assert sw in TransitionBoardDef.VOLTAGE_OVERSHOOT_SWITCH.keys()
        assert state in [TransitionBoardDef.SWITCH_STATE_ON, TransitionBoardDef.SWITCH_STATE_OFF]
        pins_and_level = TransitionBoardDef.VOLTAGE_OVERSHOOT_SWITCH[sw][state]
        for each in pins_and_level:
            self._pca9506_pack.set_pin(each[0], each[1])
