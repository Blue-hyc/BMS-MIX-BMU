# -*- coding: utf-8 -*-
from tinyrpcx import public
# from driver.bus.gpio import GPIO
class LEDS(object):
    def __init__(self,info):
        #get GPIO Pin_55 & Pin_54
        self.gpio_55=info['gpio_55']
        self.gpio_54=info['gpio_54']
    
    #LED_54(IO_35_L11N) turn on 
    @public
    def led_54_on(self):
        self.gpio_54.set_level(1)
        return 'OK'

    #LED_54(IO_35_L11N) turn off
    @public
    def led_54_off(self):
        self.gpio_54.set_level(0)
        return 'OK'

    #LED_55(IO_35_L11P) turn on 
    @public
    def led_55_on(self):
        self.gpio_55.set_level(1)
        return 'OK'

    #Led_55(IO_35_L11P) turn off
    @public
    def led_55_off(self):
        self.gpio_55.set_level(0)
        return 'OK'
    
