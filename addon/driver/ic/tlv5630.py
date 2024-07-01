from dac_base import *
from mix.driver.core.bus.spi_bus_emulator import *
from mix.driver.core.bus.pin_emulator import *
import time


class TLV5630Def:
    TLV5630_REG_OFFSET = 12

    TLV5630_REG_DAC_A = 0
    TLV5630_REG_DAC_B = 1
    TLV5630_REG_DAC_C = 2
    TLV5630_REG_DAC_D = 3
    TLV5630_REG_DAC_E = 4
    TLV5630_REG_DAC_F = 5
    TLV5630_REG_DAC_G = 6
    TLV5630_REG_DAC_H = 7
    TLV5630_REG_CTRL0 = 8
    TLV5630_REG_CTRL1 = 9
    TLV5630_REG_Preset = 10
    TLV5630_REG_DAC_A_B = 12
    TLV5630_REG_DAC_C_D = 13
    TLV5630_REG_DAC_E_F = 14
    TLV5630_REG_DAC_G_H = 15

    REGISTERS = [
        TLV5630_REG_DAC_A,
        TLV5630_REG_DAC_B,
        TLV5630_REG_DAC_C,
        TLV5630_REG_DAC_D,
        TLV5630_REG_DAC_E,
        TLV5630_REG_DAC_F,
        TLV5630_REG_DAC_G,
        TLV5630_REG_DAC_H,
        TLV5630_REG_CTRL0,
        TLV5630_REG_CTRL1,
        TLV5630_REG_Preset,
        TLV5630_REG_DAC_A_B,
        TLV5630_REG_DAC_C_D,
        TLV5630_REG_DAC_E_F,
        TLV5630_REG_DAC_G_H
    ]

    TLV5630_DAC_A = 0
    TLV5630_DAC_B = 1
    TLV5630_DAC_C = 2
    TLV5630_DAC_D = 3
    TLV5630_DAC_E = 4
    TLV5630_DAC_F = 5
    TLV5630_DAC_G = 6
    TLV5630_DAC_H = 7

    DAC_list = {
        TLV5630_DAC_A: TLV5630_REG_DAC_A,
        TLV5630_DAC_B: TLV5630_REG_DAC_B,
        TLV5630_DAC_C: TLV5630_REG_DAC_C,
        TLV5630_DAC_D: TLV5630_REG_DAC_D,
        TLV5630_DAC_E: TLV5630_REG_DAC_E,
        TLV5630_DAC_F: TLV5630_REG_DAC_F,
        TLV5630_DAC_G: TLV5630_REG_DAC_G,
        TLV5630_DAC_H: TLV5630_REG_DAC_H,
    }


class TLV5630(object):
    '''
    TLV5630 is a 8-channel, 12-bit voltage-output digital-to-analog converter(DAC).

    ClassType = DAC

    Args:
        ldac_pin: instance(Pin),
        spi_bus:  instance(SPI)/None, Class instance of SPI bus,
                                      If not using the parameter
                                      will create Emulator

    Examples:
        axi = AXI4LiteBus('/dev/quad_spi_0', 256)
        spi = PLSPIBus(axi)
        ad5791 = AD5791(spi)

    '''
    def __init__(self, ldac_pin=None, spi_bus=None):
        if ldac_pin is None:
            self._ldac_pin = PinEmulator('TLV5630_LDAC_Pin_Emulator')
        else:
            self._ldac_pin = ldac_pin
        if spi_bus is None:
            self._spi_bus = SPIBusEmulator('TLV5630_Emulator', 256)
        else:
            self._spi_bus = spi_bus
        self._ldac_pin.set_level(1)
        self.write(TLV5630Def.TLV5630_REG_CTRL0, 0x006)

    def write(self, reg, content):
        raw = (reg << TLV5630Def.TLV5630_REG_OFFSET) | (content & 0x0FFF)
        data = [(raw & 0xFF00) >> 8, raw & 0x00FF]
        self._spi_bus.write(data)

    def set_voltage(self, channel, volt):
        isinstance(channel, int) and channel in TLV5630Def.DAC_list
        isinstance(volt, float)
        dac = int(round(volt * 4096 / (2 * 2))) & 0x0FFF
        self.write(TLV5630Def.DAC_list[channel], dac)
        self._ldac_pin.set_level(1)
        time.sleep(0.01)
        self._ldac_pin.set_level(0)
        time.sleep(0.01)
        self._ldac_pin.set_level(1)




