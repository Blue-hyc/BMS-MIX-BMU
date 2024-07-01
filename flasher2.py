import time

from mix.driver.core.ic.cat24cxx import CAT24C32
from mix.driver.core.ic.tca9548 import TCA9548
from mix.addon.driver.ic.pca9506 import PCA9506
from mix.driver.core.bus.i2c import I2C
from mix.driver.core.bus.i2c_ds_bus import I2CDownstreamBus
import struct
from mix.driver.core.module.mixmodulehelper import BytesHelper
from mix.driver.core.bus.gpio import GPIO
from mix.driver.core.bus.pin import Pin
import datetime


if __name__ == '__main__':
    io_mux = PCA9506(GPIO(992, 'output'), 32, I2C("/dev/i2c-1"))
    tp166 = Pin(io_mux, 7, 'output')
    tp166.set_level(1)
    # tp166.set_level(0)
    rst_pin = Pin(io_mux, 2, 'output')
    rst_pin.set_level(0)
    time.sleep(0.1)
    rst_pin.set_level(1)
    i2c_mux = TCA9548(112, I2C("/dev/i2c-0"))
    eeprom = CAT24C32(0x50, I2CDownstreamBus(i2c_mux, 1))
    all_data = [0xFF for i in range(eeprom.chip_size)]
    eeprom.write(0, all_data)
    ro_data = []
    eeprom.write(0, [4])
    ro_data.append(4)
    eeprom.write(1, [0x20, 0x00])
    ro_data.extend([0x20, 0x00])
    ppp = 'J0H'
    tmp = list(ppp)
    ppp = list(struct.unpack('%dB' % len(tmp), ppp))
    eeprom.write(3, ppp)
    ro_data.extend(ppp)
    eeprom.write(6, [0x00, 0x01, 0x02, 0x03])
    ro_data.extend([0x00, 0x01, 0x02, 0x03])
    eeprom.write(0x0A, [0x00, 0x00, 0x00, 0x00])
    ro_data.extend([0x00, 0x00, 0x00, 0x00])
    eeee = 'PSU2'
    tmp = list(eeee)
    eeee = list(struct.unpack('%dB' % len(tmp), eeee))
    eeprom.write(0x0E, eeee)
    ro_data.extend(eeee)

    rev = '0'
    tmp = list(rev)
    rev = list(struct.unpack('%dB' % len(tmp), rev))
    eeprom.write(0x12, rev)
    ro_data.extend(rev)

    eeprom.write(0x13, [0])
    ro_data.append(0)

    eeprom.write(0x14, [0x01])
    ro_data.append(0x01)

    cfg = '001'
    tmp = list(cfg)
    cfg = list(struct.unpack('%dB' % len(tmp), cfg))
    eeprom.write(0x15, cfg)
    ro_data.extend(cfg)

    num_cal = 1
    eeprom.write(0x18, [num_cal])
    ro_data.append(num_cal)

    cal_size = 200
    size_list = [cal_size & 0xFF, (cal_size & 0xFF00) >> 8, (cal_size & 0xFF0000) >> 16, (cal_size & 0xFF000000) >> 24]
    eeprom.write(0x19, size_list)
    ro_data.extend(size_list)

    '''
    Module condition is represented by a single byte, and values represent:
    0: New module and passes OQC
    1: Module repaired and passes OQC
    2: Bad Module - should not be used. Note, launcher may not load a module with bad condition
    3-255: Reservered
    '''
    eeprom.write(0x1D, [0x00])
    ro_data.append(0x00)

    reserved = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    eeprom.write(0x1E, reserved)
    ro_data.extend(reserved)

    ro_hash = BytesHelper.sha1_hash(bytearray(ro_data))
    eeprom.write(0x2C, ro_hash)

    # data = eeprom.read(0, 4096)
    # for i in range(len(data)):
    #     print i, ':', data[i], ','

    print 'success'



