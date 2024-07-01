# -*- coding: utf-8 -*-
from mix.addon.driver.ic.ads8900 import *
from mix.addon.driver.ic.pga280 import *
import math
import time
from mix.driver.core.bus.pin import Pin

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class DVMBoardDef:
    DVM_GAIN_0_P_1 = 0
    DVM_GAIN_0_P_2 = 1
    DVM_GAIN_0_P_4 = 2
    DVM_GAIN_0_P_8 = 3
    DVM_GAIN_1_P_6 = 4
    DVM_GAIN_3_P_2 = 5
    DVM_GAIN_6_P_4 = 6
    DVM_GAIN_12_P_8 = 7
    DVM_GAIN_25_P_6 = 8
    DVM_GAIN_51_P_2 = 9
    DVM_GAIN_102_P_4 = 10

    PGA280_GAIN = 0
    GAIN_VALUE = 1

    DVM_GAIN = {
        DVM_GAIN_0_P_1: [0.125, 0.1],
        DVM_GAIN_0_P_2: [0.25, 0.2],
        DVM_GAIN_0_P_4: [0.5, 0.4],
        DVM_GAIN_0_P_8: [1, 0.8],
        DVM_GAIN_1_P_6: [2, 1.6],
        DVM_GAIN_3_P_2: [4, 3.2],
        DVM_GAIN_6_P_4: [8, 6.4],
        DVM_GAIN_12_P_8: [16, 12.8],
        DVM_GAIN_25_P_6: [32, 25.6],
        DVM_GAIN_51_P_2: [64, 51.2],
        DVM_GAIN_102_P_4: [128, 102.4]
    }

    PSU1_SENSE = 0
    PSU1_MEASOUT = 1
    PSU1_HC_1 = 2
    PSU1_MV_1nA = 3
    PSU2_SENSE = 4
    PSU2_MEASOUT = 5
    PSU2_HC_1 = 6
    PSU2_HC_2 = 7
    EXTERNAL_MV = 8
    TEMPERATURE = 9
    I2C_SDA = 10
    I2C_SCL = 11
    ACIR_DISCHARGE = 12
    ACIR_GOING = 13
    PSU2_EXT_CAL = 14

    '''
       pin_id        0  1  2  3  4  5  6  7  acir(8)  acir_disc(9)

    PSU1_SENSE       0  0  0  0  x  x  x  x  x  x
    PSU1_MEASOUT     0  0  0  1  x  x  x  x  x  x
    PSU1_HC_1        0  0  1  x  0  x  x  x  x  x
    PSU1_MV_1nA      0  0  1  x  1  x  x  x  x  x
    PSU2_SENSE       0  1  x  x  x  0  0  x  1  0 
    PSU2_MEASOUT     0  1  x  x  x  0  1  x  x  x  
    PSU2_HC_1        0  1  x  x  x  1  x  0  x  x  
    PSU2_HC_2        0  1  x  x  x  1  x  1  x  x 
    EXTERNAL_MV      1  x  x  x  x  x  x  x  x  x 
    TEMPERATURE      1  x  x  x  x  x  x  x  x  x  
    I2C_SDA          1  x  x  x  x  x  x  x  x  x 
    I2C_SCL          1  x  x  x  x  x  x  x  x  x
    ACIR_DISCHARGE   0  1  x  x  x  0  0  x  0  1
    ACIR_GOING       0  1  x  x  x  0  0  x  0  0    
    
    x: don't care    
    '''

    INPUT_TYPE = {
        PSU1_SENSE: {'bits': [[0, 0], [1, 0], [2, 0], [3, 0]], 'channel': 'CHANNEL_A'},
        PSU1_MEASOUT: {'bits': [[0, 0], [1, 0], [2, 0], [3, 1]], 'channel': 'CHANNEL_A'},
        PSU1_HC_1: {'bits': [[0, 0], [1, 0], [2, 1], [4, 0]], 'channel': 'CHANNEL_A'},
        PSU1_MV_1nA: {'bits': [[0, 0], [1, 0], [2, 1], [4, 1]], 'channel': 'CHANNEL_A'},
        PSU2_SENSE: {'bits': [[0, 0], [1, 1], [5, 0], [6, 0], [8, 1], [9, 0]], 'channel': 'CHANNEL_A'},
        PSU2_MEASOUT: {'bits': [[0, 0], [1, 1], [5, 0], [6, 1]], 'channel': 'CHANNEL_A'},
        PSU2_HC_1: {'bits': [[0, 0], [1, 1], [5, 1], [7, 0]], 'channel': 'CHANNEL_A'},
        PSU2_HC_2: {'bits': [[0, 0], [1, 1], [5, 1], [7, 1]], 'channel': 'CHANNEL_A'},
        EXTERNAL_MV: {'bits': [[0, 1]], 'channel': 'CHANNEL_A'},
        TEMPERATURE: {'bits': [], 'channel': 'CHANNEL_A'},
        I2C_SDA: {'bits': [[0, 1]], 'channel': 'CHANNEL_A'},
        I2C_SCL: {'bits': [[0, 1]], 'channel': 'CHANNEL_A'},
        ACIR_DISCHARGE: {'bits': [], 'channel': 'CHANNEL_A'},
        ACIR_GOING: {'bits': [], 'channel': 'CHANNEL_A'},
        PSU2_EXT_CAL:  {'bits': [[10, 1]], 'channel': 'CHANNEL_B'},
    }

    CS_DMM_GPIO_0 = 12
    CS_DMM_GPIO_1 = 13
    CS_DMM_GPIO_2 = 14
    CS_DMM_GPIO_3 = 15
    CS_DMM_GPIO_4 = 16
    CS_DMM_GPIO_5 = 17
    CS_DMM_GPIO_6 = 18
    CS_DMM_GPIO_7 = 19
    CS_DMM_ACIC = 20
    CS_DMM_ACIC_DISC = 21
    CS_CAL_CUR = 22

    INPUT_SWITCH_PIN = [
        CS_DMM_GPIO_0,
        CS_DMM_GPIO_1,
        CS_DMM_GPIO_2,
        CS_DMM_GPIO_3,
        CS_DMM_GPIO_4,
        CS_DMM_GPIO_5,
        CS_DMM_GPIO_6,
        CS_DMM_GPIO_7,
        CS_DMM_ACIC,
        CS_DMM_ACIC_DISC,
        CS_CAL_CUR
    ]


class DVMBoard(object):
    compatible = ['J0H-DMM0-0-001']

    rpc_public_api = ['set_gain', 'measure_voltage', 'set_input']

    def __init__(self, cs_pin_mux, spi_0, spi_bus=None):
        self._spi_0 = spi_0
        self._pga280 = PGA280(spi_bus)
        self._ads8900 = ADS8900(5.0, spi_bus)
        self._cs_pins = []
        for pin in DVMBoardDef.INPUT_SWITCH_PIN:
            tmp = Pin(cs_pin_mux, pin, 'output')
            self._cs_pins.append(tmp)
            tmp.set_level(0)
        self._gain = 0.8

    def pre_power_on_init(self):
        pass

    def post_power_on_init(self):
        self._spi_0.set_level(0)
        time.sleep(0.1)
        self._pga280.config_gpio_direction(2, 'output')
        self._pga280.config_gpio_direction(5, 'output')
        self._pga280.set_gain(0.125)
        self._pga280.channel_select('CHANNEL_NONE')
        self._pga280.write_gpio(2, 1)
        time.sleep(0.1)
        self._pga280.write_gpio(2, 0)
        time.sleep(0.1)
        self._pga280.write_gpio(2, 1)
        self._spi_0.set_level(1)
        time.sleep(0.1)
        self._ads8900.set_sdo_width(4)

    def set_gain(self, gain):
        assert gain in DVMBoardDef.DVM_GAIN.keys()
        pga280_gain = DVMBoardDef.DVM_GAIN[gain][DVMBoardDef.PGA280_GAIN]
        self._spi_0.set_level(0)
        time.sleep(0.1)
        self._pga280.set_gain(pga280_gain)
        self._spi_0.set_level(1)
        time.sleep(0.1)
        self._gain = DVMBoardDef.DVM_GAIN[gain][DVMBoardDef.GAIN_VALUE]

    def measure_voltage(self, freq, duration, is_average=True):
        assert isinstance(freq, int) and 0 < freq <= 500000
        assert isinstance(duration, int) or isinstance(duration, float) and duration > 0
        voltages = self._ads8900.read_voltage(freq, duration)
        if is_average:
            return math.fsum(voltages) / len(voltages) / self._gain
        for i in range(len(voltages)):
            voltages[i] /= self._gain
            return voltages

    def set_input(self, input_type):
        assert input_type in DVMBoardDef.INPUT_TYPE.keys()
        states = DVMBoardDef.INPUT_TYPE[input_type]['bits']
        channel = DVMBoardDef.INPUT_TYPE[input_type]['channel']
        self._spi_0.set_level(0)
        time.sleep(0.1)
        self._pga280.channel_select('CHANNEL_NONE')
        self._pga280.set_gain(0.125)
        self._pga280.channel_select(channel)
        for each in states:
            pin = each[0]
            level = each[1]
            self._cs_pins[pin].set_level(level)
        # time.sleep(0.05)

    def set_gain_fast(self, gain):
        assert gain in DVMBoardDef.DVM_GAIN.keys()
        pga280_gain = DVMBoardDef.DVM_GAIN[gain][DVMBoardDef.PGA280_GAIN]
        self._spi_0.set_level(0)
        time.sleep(0.05)
        self._pga280.set_gain(pga280_gain)
        self._spi_0.set_level(1)
        time.sleep(0.05)
        self._gain = DVMBoardDef.DVM_GAIN[gain][DVMBoardDef.GAIN_VALUE]

    def set_input_fast(self, input_type):
        assert input_type in DVMBoardDef.INPUT_TYPE.keys()
        states = DVMBoardDef.INPUT_TYPE[input_type]['bits']
        channel = DVMBoardDef.INPUT_TYPE[input_type]['channel']
        self._spi_0.set_level(0)
        time.sleep(0.05)
        self._pga280.channel_select('CHANNEL_NONE')
        self._pga280.set_gain(0.125)
        self._pga280.channel_select(channel)
        for each in states:
            pin = each[0]
            level = each[1]
            self._cs_pins[pin].set_level(level)
        # time.sleep(0.05)
