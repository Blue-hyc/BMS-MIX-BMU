# -*- coding: utf-8 -*-
import time
import struct
from mix.addon.driver.ic.ds2482 import DS2482
from mix.addon.driver.ic.tmp117 import TMP117
from mix.driver.core.ic.cat24cxx import CAT24C32


class Carrier(object):

    rpc_public_api = ['read_temperature', 'read_carrier', 'write_carrier']

    def __init__(self, i2c_bus):
        self._io = DS2482(0x18, i2c_bus)
        self._tmp117 = TMP117(0x48, i2c_bus)
        self._eeprom = CAT24C32(0x50, i2c_bus)

    def read_temperature(self):
        self._tmp117.reset()
        time.sleep(0.01)
        return self._tmp117.read_temperature()

    def read_carrier(self, is_str=True):
        rd = self._eeprom.read(0, 11)
        try:
            carrier_id = bytearray(rd).decode('ascii')
            if not carrier_id.isalnum():
                carrier_id = 'HYCCARRIER1'
        except Exception as e:
            carrier_id = 'HYCCARRIER1'
        if not is_str:
            tmp = list(carrier_id)
            carrier_id = list(struct.unpack('%dB' % len(tmp), carrier_id))
        return carrier_id

    def write_carrier(self, carrier_id):
        self._eeprom.write(0, carrier_id)
