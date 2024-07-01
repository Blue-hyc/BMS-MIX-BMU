# -*- coding: utf-8 -*-
from mix.driver.smartgiant.common.ipcore.mix_signalsource_sg import *
import time
from threading import Thread

LED_COLOR = ['white', 'green', 'blue', 'red', 'yellow']
FAN_TYPE = ['slow', 'fast']


class LedFan(Thread):
    def __init__(self):
        super(LedFan, self).__init__()
        self.led_color = 'white'
        self.fan_type = 'slow'
        self.start()

    def set_led_color(self, led_color):
        assert led_color in LED_COLOR
        self.led_color = led_color

    def set_fan_type(self, fan_type):
        assert fan_type in FAN_TYPE
        self.fan_type = fan_type

    def run(self):
        signalsource = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH0", 2048))
        signalsource.open()
        signalsource.set_signal_type('square')
        signalsource.output_signal()
        signalsource1 = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH1", 2048))
        signalsource1.open()
        signalsource1.set_signal_type('square')
        signalsource1.output_signal()
        signalsource2 = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH2", 2048))
        signalsource2.open()
        signalsource2.set_signal_type('square')
        signalsource2.output_signal()
        signalsource3 = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH3", 2048))
        signalsource3.open()
        signalsource3.set_signal_type('square')
        signalsource3.output_signal()
        signalsource4 = MIXSignalSourceSG(AXI4LiteBus("/dev/XVR_PWM_CH4", 2048))
        signalsource4.open()
        signalsource4.set_signal_type('square')
        signalsource4.output_signal()
        flag = 1.0
        dirction = 0
        alarm = 0
        i = 0
        while True:
            time.sleep(0.012)
            if dirction == 0:
                if flag > 0.005:
                    if flag < 0.3:
                        time.sleep(0.015)
                    flag -= 0.005
                    if flag < 0.005:
                        time.sleep(0.1)
                else:
                    dirction = 1
            else:
                if flag <= 0.995:
                    if flag < 0.3:
                        time.sleep(0.015)
                    flag += 0.005
                else:
                    dirction = 0
            if self.led_color == 'yellow':
                while True:
                    time.sleep(0.001)
                    i += 1
                    if i == 300:
                        alarm = 0.9 if alarm == 0 else 0
                        i = 0
                    # if self.led_color != 'yellow':
                    #     break
                    signalsource1.set_swg_paramter(1000, 0.005, 1, 0, 0)
                    signalsource2.set_swg_paramter(1000, 0.005, 1, 0, 0)
                    signalsource3.set_swg_paramter(1000, 0.005, 1, alarm, 0)
                    signalsource4.set_swg_paramter(1000, 0.005, 1, alarm, 0)
            if self.led_color == 'white':
                signalsource1.set_swg_paramter(1000, 0.005, 1, flag, 0)
                signalsource2.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource3.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource4.set_swg_paramter(1000, 0.005, 1, 0, 0)
            if self.led_color == 'green':
                signalsource1.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource2.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource3.set_swg_paramter(1000, 0.005, 1, 0.2, 0)
                signalsource4.set_swg_paramter(1000, 0.005, 1, 0, 0)
            if self.led_color == 'blue':
                signalsource1.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource2.set_swg_paramter(1000, 0.005, 1, flag, 0)
                signalsource3.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource4.set_swg_paramter(1000, 0.005, 1, 0, 0)
            if self.led_color == 'red':
                signalsource1.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource2.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource3.set_swg_paramter(1000, 0.005, 1, 0, 0)
                signalsource4.set_swg_paramter(1000, 0.005, 1, 0.2, 0)
            if self.fan_type == 'fast':
                signalsource.set_swg_paramter(1000, 0.005, 1, 1, 0)
            if self.fan_type == 'slow':
                signalsource.set_swg_paramter(1000, 0.005, 1, 1, 0)
