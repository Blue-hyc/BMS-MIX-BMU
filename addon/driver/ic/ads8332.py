# -*- coding: utf-8 -*-
from mix.driver.core.bus.spi_bus_emulator import *
from mix.driver.core.bus.spi import *
from mix.driver.core.bus.pin import Pin
from mix.driver.core.bus.pin_emulator import *
import time

__author__ = 'wanghong'
__version__ = '1.0'


class ADS8332Def:
    ADS8332_CHANNEL_0 = 0
    ADS8332_CHANNEL_1 = 1
    ADS8332_CHANNEL_2 = 2
    ADS8332_CHANNEL_3 = 3
    ADS8332_CHANNEL_4 = 4
    ADS8332_CHANNEL_5 = 5
    ADS8332_CHANNEL_6 = 6
    ADS8332_CHANNEL_7 = 7

    Channels = [
        ADS8332_CHANNEL_0,
        ADS8332_CHANNEL_1,
        ADS8332_CHANNEL_2,
        ADS8332_CHANNEL_3,
        ADS8332_CHANNEL_4,
        ADS8332_CHANNEL_5,
        ADS8332_CHANNEL_6,
        ADS8332_CHANNEL_7
    ]

    ADS8332_CMD_OFFSET = 12
    ADS8332_CMD_MASK = 0x000F << ADS8332_CMD_OFFSET
    ADS8332_CMD_CHANNEL_0 = 0
    ADS8332_CMD_CHANNEL_1 = 1
    ADS8332_CMD_CHANNEL_2 = 2
    ADS8332_CMD_CHANNEL_3 = 3
    ADS8332_CMD_CHANNEL_4 = 4
    ADS8332_CMD_CHANNEL_5 = 5
    ADS8332_CMD_CHANNEL_6 = 6
    ADS8332_CMD_CHANNEL_7 = 7
    ADS8332_CMD_WAKE_UP = 11
    ADS8332_CMD_READ_CFR = 12
    ADS8332_CMD_READ_DATA = 13
    ADS8332_CMD_WRITE_CFR = 14
    ADS8332_CMD_DEFAULT_MODE = 15

    CMD_Type = [
        ADS8332_CMD_CHANNEL_0,
        ADS8332_CMD_CHANNEL_1,
        ADS8332_CMD_CHANNEL_2,
        ADS8332_CMD_CHANNEL_3,
        ADS8332_CMD_CHANNEL_4,
        ADS8332_CMD_CHANNEL_5,
        ADS8332_CMD_CHANNEL_6,
        ADS8332_CMD_CHANNEL_7,
        ADS8332_CMD_WAKE_UP,
        ADS8332_CMD_READ_CFR,
        ADS8332_CMD_READ_DATA,
        ADS8332_CMD_WRITE_CFR,
        ADS8332_CMD_DEFAULT_MODE,
    ]

    Channel_CMD_Type = {
        ADS8332_CHANNEL_0: ADS8332_CMD_CHANNEL_0,
        ADS8332_CHANNEL_1: ADS8332_CMD_CHANNEL_1,
        ADS8332_CHANNEL_2: ADS8332_CMD_CHANNEL_2,
        ADS8332_CHANNEL_3: ADS8332_CMD_CHANNEL_3,
        ADS8332_CHANNEL_4: ADS8332_CMD_CHANNEL_4,
        ADS8332_CHANNEL_5: ADS8332_CMD_CHANNEL_5,
        ADS8332_CHANNEL_6: ADS8332_CMD_CHANNEL_6,
        ADS8332_CHANNEL_7: ADS8332_CMD_CHANNEL_7,
    }

    ADS8332_SAMPLE_TIMES = 1000

    ADS8332_SPI_DIR_WRITE = 0
    ADS8332_SPI_DIR_READ = 1

    SPI_Type = [
        ADS8332_SPI_DIR_WRITE,
        ADS8332_SPI_DIR_READ
    ]


class ADS8332(object):

    rpc_public_api = ['read_voltage']
    
    def __init__(self, convst_pin=None, cs_pin=None, spi_bus=None):
        if convst_pin is None:
            self._convst_pin = PinEmulator("ADS8332_CONV")
        else:
            self._convst_pin = convst_pin
        if spi_bus is None:
            self._spi_bus = SPIBusEmulator("ADS8332_Emulator")
        else:
            self._spi_bus = spi_bus
        self._cs_pin = cs_pin
        self._cs_pin.set_level(1)
        self._convst_pin.set_level(1)
        cfr = 0x077C
        self.access(ADS8332Def.ADS8332_CMD_WRITE_CFR, cfr)
        # sleep 10us
        cfr = 0x077D
        self.access(ADS8332Def.ADS8332_CMD_WRITE_CFR, cfr)

    def access(self, cmd, content=0, op=ADS8332Def.ADS8332_SPI_DIR_WRITE):
        assert isinstance(cmd, int) and cmd in ADS8332Def.CMD_Type
        assert isinstance(op, int) and op in ADS8332Def.SPI_Type
        self._cs_pin.set_level(1)
        self._cs_pin.set_level(0)
        if ADS8332Def.ADS8332_SPI_DIR_READ == op:
            raw = (cmd << ADS8332Def.ADS8332_CMD_OFFSET) | 0x0000
            wd = [(raw & 0xFF00) >> 8, raw & 0x00FF]
            rd = self._spi_bus.transfer(wd, 2)
            # print 'rd'
            # print rd
            self._cs_pin.set_level(1)
            data = (rd[0] << 8) | rd[1]
            # cfr: xxxx dddd dddd dddd
            # data:dddd dddd dddd dddd
            # print hex(data)
            return data
        else:
            raw = (cmd << ADS8332Def.ADS8332_CMD_OFFSET) | (content & 0x0FFF)
            # print 'ads8332 write:'
            # print bin(raw)
            wd = [(raw & 0xFF00) >> 8, raw & 0x00FF]
            self._spi_bus.write(wd)
            self._cs_pin.set_level(1)
            
    # def read_data(self):
    #     self._cs_pin.set_level(1)
    #     self._cs_pin.set_level(0)
    #     raw = (ADS8332Def.ADS8332_CMD_READ_DATA << ADS8332Def.ADS8332_CMD_OFFSET) | 0x0000
    #     wd = [(raw & 0xFF00) >> 8, raw & 0x00FF]
    #     rd = self._spi_bus.transfer(wd, 2)
    #     self._cs_pin.set_level(1)
    #     data = (rd[0] << 8) | rd[1]
    #     print hex(data)
    #     return data
    #
    # def read_cfr(self):
    #     self._cs_pin.set_level(1)
    #     self._cs_pin.set_level(0)
    #     raw = (ADS8332Def.ADS8332_CMD_READ_DATA << ADS8332Def.ADS8332_CMD_OFFSET) | 0x0000
    #     wd = [(raw & 0xFF00) >> 8, raw & 0x00FF]
    #     rd = self._spi_bus.transfer(wd, 2)
    #     self._cs_pin.set_level(1)
    #     data = (rd[0] << 8) | rd[1]
    #     print hex(data)
    #     return data

    def read_voltage(self, channel):
        assert isinstance(channel, int) and channel in ADS8332Def.Channels
        self.access(ADS8332Def.Channel_CMD_Type[channel])
        #sleep 10us
        times = ADS8332Def.ADS8332_SAMPLE_TIMES
        volt = 0.0
        while times > 0:
            #sleep 10us
            self._convst_pin.set_level(0)
            #sleep 1us
            self._convst_pin.set_level(1)
            #sleep 5us
            raw = self.access(ADS8332Def.ADS8332_CMD_READ_DATA, 0, ADS8332Def.ADS8332_SPI_DIR_READ)
            volt += 1.0 * raw / 65536 * 2.5
            times -= 1
        return volt/ADS8332Def.ADS8332_SAMPLE_TIMES



