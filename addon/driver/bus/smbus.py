#!/usr/bin/python
# -*- coding: utf-8 -*-
from mix.driver.core.bus.i2c_bus_emulator import I2CBusEmulator


__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class SMBusException(Exception):
    def __init__(self, err):
        self.__err = err

    def __str__(self):
        return self.__err


class SMBus(object):
    '''
    SMBus class
    '''
    def __init__(self, dev_name, i2c_bus=None):
        if i2c_bus is None:
            self.__i2c_bus = I2CBusEmulator(dev_name, 256)
        else:
            self.__i2c_bus = i2c_bus
        self.__pec = False

    @property
    def pec(self):
        return self.__pec

    @pec.setter
    def pec(self, enable):
        self.__pec = enable

    def write_byte(self, address, cmd, byte):
        wr_data = []
        wr_data.append(cmd)
        wr_data.append(byte)
        if self.__pec:
            data = [address << 1]
            data.append(cmd)
            data.append(byte)
            pec = self.__cal_pec(0, data)
            wr_data.append(pec)
        self.__i2c_bus.write(address, wr_data)

    def write_word(self, address, cmd, word):
        '''

        :param address:
        :param cmd:
        :param word:
        :return:
        '''
        wr_data = []
        wr_data.append(cmd)
        wr_data.append(word & 0x00FF)
        wr_data.append((word & 0xFF00) >> 8)
        if self.__pec:
            data = [address << 1]
            data.append(cmd)
            data.extend(wr_data[1:3])
            pec = self.__cal_pec(0, data)
            wr_data.append(pec)
        self.__i2c_bus.write(address, wr_data)

    def read_byte(self, address, cmd):
        '''
        :param address:
        :param cmd:
        :param count:
        :return:
        '''
        if self.__pec:
            data = []
            data.append(address << 1)
            data.append(cmd)
            data.append(address << 1 | 0x01)
            pec = self.__cal_pec(0, data)
            rd_data = self.__i2c_bus.write_and_read(address, [cmd], 2)  # +1 for pec
            # confirm pec
            pec = self.__cal_pec(pec, rd_data[0])
            if pec == rd_data[1]:
                return rd_data[0]
            else:
                raise SMBusException('PEC IS NOT CORRECT')
        else:
            rd_data = self.__i2c_bus.write_and_read(address, [cmd], 1)
            return rd_data

    def read_word(self, address, cmd):
        '''
        :param address:
        :param cmd:
        :param count:
        :return:
        '''
        if self.__pec:
            data = []
            data.append(address << 1)
            data.append(cmd)
            data.append(address << 1 | 0x01)
            pec = self.__cal_pec(0, data)
            rd_data = self.__i2c_bus.write_and_read(address, [cmd], 3)  # +1 for pec
            # confirm pec
            pec = self.__cal_pec(pec, rd_data[0:2])
            if pec == rd_data[2]:
                return rd_data[1] << 8 | rd_data[0]
            else:
                raise SMBusException('PEC IS NOT CORRECT')
        else:
            rd_data = self.__i2c_bus.write_and_read(address, [cmd], 2)
            return rd_data[1] << 8 | rd_data[0]

    def read_block(self, address, cmd, count):
        '''
        :param address:
        :param cmd:
        :param count:
        :return:
        '''
        if self.__pec:
            data = []
            data.append(address << 1)
            data.append(cmd)
            data.append(address << 1 | 0x01)
            pec = self.__cal_pec(0, data)
            rd_data = self.__i2c_bus.write_and_read(address, [cmd], count + 2)  # +2 for pec & block size
            # confirm pec
            # rd_data = [block_count, byte 1, byte 2, ..., byte n, pec]
            if rd_data[0] > count:  # size is not correct
                return
            pec = self.__cal_pec(pec, rd_data[0:count + 1])
            if pec == rd_data[count + 1]:
                return rd_data[1:count + 1]
            else:
                raise SMBusException('PEC IS NOT CORRECT')
        else:
            rd_data = self.__i2c_bus.write_and_read(address, [cmd], count)
            return rd_data

    def send_byte(self, address, cmd):
        '''

        :param address:
        :param cmd:
        :return:
        '''
        wr_data = []
        wr_data.append(cmd)
        if self.__pec:
            data = [address << 1]
            data.append(cmd)
            pec = self.__cal_pec(0, data)
            wr_data.append(pec)
        self.__i2c_bus.write(address, wr_data)

    def wait_for_ack(self, address, cmd):
        timeout = 8192
        while timeout > 0:
            data = self.__i2c_bus.write_and_read(address, [cmd], 1)
            if data is None:
                continue
            else:
                return True
        return False

    def __cal_pec(self, seed, data):
        '''
        :param seed:
        :param data:
        :return:
        '''
        pec = seed
        for index in range(len(data)):
            pec ^= data[index]
            for y in range(8):
                if pec & 0x80:
                    pec = (pec << 1) ^ 0x07
                else:
                    pec <<= 1
        return pec & 0xFF



