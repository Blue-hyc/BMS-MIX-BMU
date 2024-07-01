# from addon.driver.ic.ad5791 import *

from mix.driver.core.ic.cat9555 import *
from mix.driver.core.ic.tca9548 import *
from mix.driver.core.bus.pin import *
from time import *
from mix.addon.driver.ic.ad5560 import *
from mix.addon.driver.ic.pca9506 import *
from mix.addon.driver.ic.pga280 import *
from mix.addon.driver.ic.ad5761 import *
from mix.addon.driver.ic.ads8900 import *
import io
import os
from mix.driver.core.bus.gpio import *
from mix.addon.driver.ic.sst26vf064b import *
from mix.addon.driver.ic.ads8332 import *
from mix.addon.driver.ic.tlv5630 import *
from mix.driver.core.bus.i2c_ds_bus import *

from mix.addon.driver.module.dvm_board import *
from mix.addon.driver.module.psu1_board import *
from mix.addon.driver.module.psu2_board import *
from mix.addon.driver.module.transition_board import *
from mix.driver.core.bus.axi4_lite_bus import *
from mix.driver.core.bus.spi import *
import socket
from mix.driver.smartgiant.common.ipcore.mix_qspi_sg import *
from mix.driver.smartgiant.common.ipcore.mix_timer_APL import *
from mix.driver.smartgiant.common.ipcore.mix_signalsource_sg import *
from mix.addon.driver.module.calibration import *
from mix.addon.driver.ic.ltc7106 import *
from threading import Thread
import thread
from mix.driver.smartgiant.common.ipcore.mix_widthmeasure_sg import *

# from mix.addon.driver.ic.timer import *
from mix.addon.driver.module.psu2_board import *
import math
from mix.addon.driver.module.calibration import Calibration
from mix.addon.driver.module.carrier import *
# from mix.driver.smartgiant.common.ipcore.ads8900_spi import *
from mix.addon.driver.ic.tpl0401x import TPL0401x

from mix.lynx.launcher.launcher import *
from mix.addon.driver.module.carrier import *


class testException(Exception):
    def __init__(self, s):
        self._err_reason = s

    def __str__(self):
        return self._err_reason


def errfunc():
    raise testException('this is a test err')

def FAN(speed):
    fan = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH0", 2048))
    fan.open()
    fan.set_signal_type('square')
    fan.output_signal()
    if speed == 'fast':
        fan.set_swg_paramter(1000, 0.008, 0.1, 0.2, 0)
    elif speed == 'slow':
        fan.set_swg_paramter(1000, 0.008, 0.1, 0.4, 0)
    else:
        fan.set_swg_paramter(1000, 0.008, 0.1, 0.2, 0)

def LED(color):
    LED_WHITE = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH1", 2048))
    LED_WHITE.open()
    LED_WHITE.set_signal_type('square')
    LED_WHITE.output_signal()
    LED_BLUE = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH2", 2048))
    LED_BLUE.open()
    LED_BLUE.set_signal_type('square')
    LED_BLUE.output_signal()
    LED_GREEN = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH3", 2048))
    LED_GREEN.open()
    LED_GREEN.set_signal_type('square')
    LED_GREEN.output_signal()
    LED_RED = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH4", 2048))
    LED_RED.open()
    LED_RED.set_signal_type('square')
    LED_RED.output_signal()
    flag = 1.0
    dirction = 0
    while 1:
        sleep(0.01)
        if dirction == 0:
            if flag > 0.005:
                flag -= 0.005
            else:
                dirction = 1
        else:
            if flag <= 0.995:
                flag += 0.005
            else:
                dirction = 0
        if color == 'GREEN':
            LED_GREEN.set_swg_paramter(1000, 0.008, 0.1, flag, 0)
        elif color == 'WHITE':
            LED_WHITE.set_swg_paramter(1000, 0.008, 0.1, flag, 0)
        elif color == 'BLUE':
            LED_BLUE.set_swg_paramter(1000, 0.008, 0.1, flag, 0)

class CAT9555Def:
    I2C_DUT_PULLUP_1K = 0
    I2C_DUT_PULLUP_2K2 = 1
    I2C_DUT_PULLUP_4K7 = 2
    I2C_DUT_PULLUP_47K = 3
    EXP_GPO_CAP = 4
    EXP_GPO_TVS = 5
    DUT_GND_EN = 6

    SWITCH_STATE_ON = 1
    SWITCH_STATE_OFF = 0

    CAT9555_GPIO_LIST = {
        I2C_DUT_PULLUP_1K : {
            SWITCH_STATE_OFF: [[0, 0], [1, 0], [2, 0], [3, 0], [8, 0], [9, 0], [10, 0], [11, 0]],
            SWITCH_STATE_ON:  [[0, 1], [1, 0], [2, 0], [3, 0], [8, 1], [9, 0], [10, 0], [11, 0]]
        },
        I2C_DUT_PULLUP_2K2 : {
            SWITCH_STATE_OFF: [[0, 0], [1, 0], [2, 0], [3, 0], [8, 0], [9, 0], [10, 0], [11, 0]],
            SWITCH_STATE_ON: [[0, 0], [1, 1], [2, 0], [3, 0], [8, 0], [9, 1], [10, 0], [11, 0]]
        },
        I2C_DUT_PULLUP_4K7 : {
            SWITCH_STATE_OFF: [[0, 0], [1, 0], [2, 0], [3, 0], [8, 0], [9, 0], [10, 0], [11, 0]],
            SWITCH_STATE_ON: [[0, 0], [1, 0], [2, 1], [3, 0], [8, 0], [9, 0], [10, 1], [11, 0]]
        },
        I2C_DUT_PULLUP_47K : {
            SWITCH_STATE_OFF: [[0, 0], [1, 0], [2, 0], [3, 0], [8, 0], [9, 0], [10, 0], [11, 0]],
            SWITCH_STATE_ON: [[0, 0], [1, 0], [2, 0], [3, 1], [8, 0], [9, 0], [10, 0], [11, 1]]
        },
        EXP_GPO_CAP : {
            SWITCH_STATE_OFF: [[4, 0]],
            SWITCH_STATE_ON : [[4, 1]]
        },
        EXP_GPO_TVS : {
            SWITCH_STATE_OFF: [[5, 0]],
            SWITCH_STATE_ON: [[5, 1]]
        },
        DUT_GND_EN : {
            SWITCH_STATE_OFF: [[12, 0]],
            SWITCH_STATE_ON: [[12, 1]]
        }
    }



if __name__ == '__main__':
    # width_measure = MIXWidthMeasureSG(AXI4LiteBus("/dev/XVR_WidthMeasure_0", 2048))
    # width_measure.config(TriggarSignalDef.SIGNAL_A_NEG, TriggarSignalDef.SIGNAL_A_POS)
    #
    pca9506 = PCA9506(GPIO(992, 'output'), 0x20, I2C('/dev/i2c-1'))
    tca9548 = TCA9548(0x70, I2C('/dev/i2c-0'))
    # tca9548.set_channel_state([[3, 1]])
    # eeprom = CAT24C32(0x50, I2CDownstreamBus(tca9548, 0))
    cat9555 = CAT9555(0x24, I2CDownstreamBus(tca9548, 3))
    tmp117_board = TMP117(0x48, I2CDownstreamBus(tca9548, 3))
    while True:
        try:
            print tmp117_board.read_temperature()
            # cat9555.set_pin(0, 1)
        except Exception as e:
            continue


    # tpl = TPL0401x(0x3E, I2CDownstreamBus(tca9548, 3))
    # print tpl.read_register()
    # tpl.set_resistance(8.91)
    # tpl.set_resistance(3.98)
    # sw = 3
    # state = 0
    # assert sw in CAT9555Def.CAT9555_GPIO_LIST
    # assert state in (CAT9555Def.SWITCH_STATE_ON, TransitionBoardDef.SWITCH_STATE_OFF)
    # pins_and_level = CAT9555Def.CAT9555_GPIO_LIST[sw][state]
    # # if len(pins_and_level) > 0:
    # for each in pins_and_level:
    #     cat9555.set_pin(each[0], each[1])

    io_exp = PCA9506(GPIO(992, 'output', 0), 32, I2C('/dev/i2c-1'))
    tca9548 = TCA9548(112, I2C('/dev/i2c-0'))

    psu0 = PSU1Board(Pin(io_exp, 6, 'output'), I2CDownstreamBus(tca9548, 0), GPIO(993, 'output', 0), Pin(io_exp, 4, 'output'),
                          Pin(io_exp, 3, 'output'), MIXAD5761HYC('/dev/MIX_AD5761_HYC_0'))
    psu1 = PSU2Board(Pin(io_exp, 8, 'output'), Pin(io_exp, 9, 'output'), Pin(io_exp, 10, 'output'), I2CDownstreamBus(tca9548, 1),
                     GPIO(994, 'output', 0), GPIO(995, 'output'),MIXAD5761HYC('/dev/MIX_AD5761_HYC_1'))
    dmm_0 = DVMBoard(io_exp, GPIO(1005, 'output', 0), MIXADS8900HYC('/dev/MIX_ADS8900_HYC_0'))
    psu0.fv(2.5, 0.01, PSU1BoardDef.CURRENT_RANGE_25mA)
    # psu1.fv(1.5, 0.01, PSU2BoardDef.CURRENT_RANGE_25mA)
    # psu0.fi(-0.05, -1.0, PSU1BoardDef.CURRENT_RANGE_100mA)
    psu0.output(True)
    # ANOLOG CURRENT
    # psu0.analog_current(0.05)
    # psu0.output(True)
    # dmm_0 = DVMBoard(None, io_exp, spi_s0_dmm1, mix_ads8900_hyc_0)
    # dmm_0.set_input(1)
    # dmm_0.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)

    dc = dmm_0.measure_voltage(500000, 0.001)
    print 'dc: [', dc, ']'


    transition = TransitionBoard(Pin(pca9506, 39, 'output'), I2CDownstreamBus(tca9548, 3))
    transition.set_i2c_dut_pull_up(3, 0)
    transition.set_switch(0, 1)

    # pca9506_trans = PCA9506(None, 0x20, I2CDownstreamBus(tca9548, 3))
    # pca9506_trans.set_pin_dir(2, 'output')
    # i = 2
    # j = 10
    # cat9555.set_pin_dir(i, 'output')
    # cat9555.set_pin(i, 1)
    # cat9555.set_pin_dir(j, 'output')
    # cat9555.set_pin(j, 1)
    # tmp117 = TMP117(0x48, I2CDownstreamBus(tca9548, 3))
    # print tmp117.read_temperature()

    # print carrier.read_temperature()

    #
    # psu1_pwr_en = Pin(pca9506, 5, 'output')
    # psu2_pwr_en = Pin(pca9506, 7, 'output')
    # dvm_pwr_en  = Pin(pca9506, 11, 'output')

    # psu1_pwr_en.set_level(1)
    # psu2_pwr_en.set_level(1)
    # dvm_pwr_en.set_level(1)

    # spi_dvm = MIXQSPISG(AXI4LiteBus("/dev/XVR_SPI_CH3_2", 2048))
    # dvm = DVMBoard(Pin(pca9506, 11, 'output'), pca9506, GPIO(999, 'output'), GPIO(998, 'input'), GPIO(1010, 'output'),
    #                spi_dvm)
    #

    # print transition.read_temperature()
    #
    # spi_bus = MIXQSPISG(AXI4LiteBus("/dev/XVR_SPI_CH2_1", 2048))
    #
    # psu2_spi_s0 = GPIO(1001, 'output')
    # psu2 = PSU2Board(Pin(pca9506, 7, 'output'), Pin(pca9506, 8, 'output'), Pin(pca9506, 9, 'output'),
    #                  Pin(pca9506, 10, 'output'), I2CDownstreamBus(tca9548, 1), GPIO(997, "output"), psu2_spi_s0,
    #                  spi_bus)
    #

    # dvm.set_input(DVMBoardDef.PSU2_HC_2)
    # dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
    # r_sense = 0.03
    # psu_gain = 1.0
    # psu2.fi(29, 5, PSU2BoardDef.CURRENT_RANGE_30A)
    # psu2.output(True)
    # sleep(0.1)
    # avg_volt = dvm.measure_voltage(3, 1.0, True)
    # current = avg_volt / r_sense / psu_gain
    # psu2.output(False)
    # print current


    # spi_bus = MIXQSPISG(AXI4LiteBus("/dev/XVR_SPI_CH1_0", 2048))
    # # calibration = Calibration(Pin(pca9506, 4, 'output'), Pin(pca9506, 3, 'output'), spi_bus)
    #
    # psu1 = PSU1Board(Pin(pca9506, 5, 'output'), Pin(pca9506, 6, 'output'), I2CDownstreamBus(tca9548, 0),
    #                  GPIO(996, "output"), Pin(pca9506, 4, 'output'), Pin(pca9506, 3, 'output'),
    #                 spi_bus)
    # psu1.fv(13, 0.1, PSU1BoardDef.CURRENT_RANGE_100mA)


    # eeprom = CAT24C32(0x50, I2CDownstreamBus(tca9548, 0))
    # eeprom.write(0, [1])
    # str = 'HYC'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0x39, msg)
    # str = 'BMSPSU01A'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0x3F, msg)
    # str = '001'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0xAF, msg)
    # # bk = eeprom.read(0, len(msg))
    # # b = []
    # # for i in bk:
    # #     b.append(chr(i))
    # # ret = ''.join(b)
    # # print ret
    #
    # eeprom = CAT24C32(0x50, I2CDownstreamBus(tca9548, 1))
    # eeprom.write(0, [1])
    # str = 'HYC'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0x39, msg)
    # str = 'BMSPSU30A'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0x3F, msg)
    # str = '001'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0xAF, msg)
    # # bk2 = eeprom.read(0, len(msg))
    # # b = []
    # # for i in bk2:
    # #     b.append(chr(i))
    # # ret = ''.join(b)
    # # print ret
    #
    # eeprom = CAT24C32(0x50, I2CDownstreamBus(tca9548, 2))
    # eeprom.write(0, [1])
    # str = 'HYC'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0x39, msg)
    # str = 'BMSDVM05V'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0x3F, msg)
    # str = '001'
    # tmp = list(str)
    # msg = list(struct.unpack('%dB' % len(tmp), str))
    # eeprom.write(0xAF, msg)
    # # bk3 = eeprom.read(0, len(msg))
    # # b = []
    # # for i in bk3:
    # #     b.append(chr(i))
    # # ret = ''.join(b)
    # # print ret
    #

    #FAN&LED Control
    # print('thread1 start')
    # thread.start_new_thread(FAN, ('fast', ))
    # sleep(2)
    # print('thread2 start')
    # thread.start_new_thread(FAN, ('slow', ))
    # sleep(2)
    # print('thread3 start')
    # thread.stop
    # thread.start_new_thread(LED, ('WHITE', ))


# breathing light
#     signalsource = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH1", 2048))
#     signalsource.open()
#     signalsource.set_signal_type('square')
#     signalsource.output_signal()
#     flag = 1.0
#     dirction = 0
#     while True:
#         sleep(0.005)
#         if dirction == 0:
#             if flag > 0.005:
#                 flag -= 0.005
#             else:
#                 dirction = 1
#         else:
#             if flag <= 0.995:
#                 flag += 0.005
#             else:
#                 dirction = 0
#         signalsource.set_swg_paramter(1000, 0.008, 0.1, flag, 0)

    # profile = load_json_file('/mix/addon/config/HYC_BMS.json')
    # switches = profile.pop('SWITCHES')
    # switch_list = profile.pop('SWITCH_LIST')
    # print switches


