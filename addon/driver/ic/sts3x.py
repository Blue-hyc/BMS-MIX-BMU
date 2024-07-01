# -*- coding: utf-8 -*-
from mix.driver.core.bus.i2c import I2C


class STS3X(object):
    def __init__(self, dev_addr, i2c_bus):
        self._dev_addr = dev_addr
        self._i2c_bus = i2c_bus

    def read_temperature(self):
        rd = self._i2c_bus.write_and_read(self._dev_addr, [0x2C, 0x06], 3)
        raw = (rd[0] << 8) | rd[1]
        temp = 175.0 * raw / 65535 - 45
        return temp
