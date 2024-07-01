# -*- coding: utf-8 -*-
from mix.driver.hyc.common.ipcore.mix_ads8900_hyc import *
from mix.driver.hyc.common.ipcore.mix_ads8900_hyc_emulator import MIXADS8900HYCEmulator

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class PGA280Def:
    PGA280_REG_OFFSET = 8

    PGA280_REG_0 = 0
    PGA280_REG_1 = 1
    PGA280_REG_2 = 2
    PGA280_REG_3 = 3
    PGA280_REG_4 = 4
    PGA280_REG_5 = 5
    PGA280_REG_6 = 6
    PGA280_REG_7 = 7
    PGA280_REG_8 = 8
    PGA280_REG_9 = 9
    PGA280_REG_A = 10
    PGA280_REG_B = 11
    PGA280_REG_C = 12

    REGISTERS = [
        PGA280_REG_0,
        PGA280_REG_1,
        PGA280_REG_2,
        PGA280_REG_3,
        PGA280_REG_4,
        PGA280_REG_5,
        PGA280_REG_6,
        PGA280_REG_7,
        PGA280_REG_8,
        PGA280_REG_9,
        PGA280_REG_A,
        PGA280_REG_B,
        PGA280_REG_C,
    ]

    COMMUNICATION_CMD_OFFSET = 12

    COMMUNICATION_WRITE = 4
    COMMUNICATION_READ = 8

    PGA280_OUTPUT_GAIN_OFFSET = 7
    PGA280_OUTPUT_GAIN_MASK = 1 << PGA280_OUTPUT_GAIN_OFFSET

    PGA280_OUTPUT_GAIN_x1 = 0
    PGA280_OUTPUT_GAIN_x1_AND_3_DIV_8 = 1

    OutputGain = {
        1: PGA280_OUTPUT_GAIN_x1,
        1.375: PGA280_OUTPUT_GAIN_x1_AND_3_DIV_8
    }

    PGA280_SW_D12 = 0x0001
    PGA280_SW_C2 = 0x0002
    PGA280_SW_C1 = 0x0004
    PGA280_SW_B2 = 0x0008
    PGA280_SW_B1 = 0x0010
    PGA280_SW_A2 = 0x0020
    PGA280_SW_A1 = 0x0040
    PGA280_SW_G2 = 0x0100
    PGA280_SW_G1 = 0x0200
    PGA280_SW_F2 = 0x0400
    PGA280_SW_F1 = 0x0800

    Switch = [
        PGA280_SW_D12,
        PGA280_SW_C2,
        PGA280_SW_C1,
        PGA280_SW_B2,
        PGA280_SW_B1,
        PGA280_SW_A2,
        PGA280_SW_A1,
        PGA280_SW_G2,
        PGA280_SW_G1,
        PGA280_SW_F2,
        PGA280_SW_F1
    ]

    PGA280_INPUT_GAIN_OFFSET = 3
    PGA280_INPUT_GAIN_MASK = 0xF << PGA280_INPUT_GAIN_OFFSET

    PGA280_INPUT_GAIN_x1_DIV_8 = 0
    PGA280_INPUT_GAIN_x1_DIV_4 = 1
    PGA280_INPUT_GAIN_x1_DIV_2 = 2
    PGA280_INPUT_GAIN_x1 = 3
    PGA280_INPUT_GAIN_x2 = 4
    PGA280_INPUT_GAIN_x4 = 5
    PGA280_INPUT_GAIN_x8 = 6
    PGA280_INPUT_GAIN_x16 = 7
    PGA280_INPUT_GAIN_x32 = 8
    PGA280_INPUT_GAIN_x64 = 9
    PGA280_INPUT_GAIN_x128 = 10

    InputGain = {
        0.125: PGA280_INPUT_GAIN_x1_DIV_8,
        0.25: PGA280_INPUT_GAIN_x1_DIV_4,
        0.5: PGA280_INPUT_GAIN_x1_DIV_2,
        1: PGA280_INPUT_GAIN_x1,
        2: PGA280_INPUT_GAIN_x2,
        4: PGA280_INPUT_GAIN_x4,
        8: PGA280_INPUT_GAIN_x8,
        16: PGA280_INPUT_GAIN_x16,
        32: PGA280_INPUT_GAIN_x32,
        64: PGA280_INPUT_GAIN_x64,
        128: PGA280_INPUT_GAIN_x128
    }

    PGA280_CHANNEL_A = 'CHANNEL_A'
    PGA280_CHANNEL_B = 'CHANNEL_B'
    PGA280_CHANNEL_NONE = 'CHANNEL_NONE'

    Channel = [
        PGA280_CHANNEL_A,
        PGA280_CHANNEL_B,
        PGA280_CHANNEL_NONE
    ]

    GPIO_Dir_Type = [
        'input',
        'output'
    ]


class PGA280(object):
    '''
    PGA280 function class.

    Args:
    mix_ads8900_hyc:    instance of MIX_ADS8900_HYC, emulator will be created if it is None.

    Examples:
        mix_ads8900_hyc = MIXADS8900HYC('/dev/MIX_ADS8900_HYC_0')
        pga280 = PGA280(mix_ads8900_hyc)
    '''

    def __init__(self, mix_ads8900_hyc=None):
        if mix_ads8900_hyc is None:
            self.mix_ads8900_hyc = MIXADS8900HYCEmulator('pga280_emulator')
        else:
            self.mix_ads8900_hyc = mix_ads8900_hyc

    def write_register(self, reg, content):
        '''
        PGA280 write specific register.

        Args:
            reg:      int, PGA280 register.
            content:  int, data to be sent.

        Examples:
            pga280.write_register(PGA280Def.PGA280_REG_0, 0x00)

        '''
        assert reg in PGA280Def.REGISTERS
        assert isinstance(content, int)
        raw = (PGA280Def.COMMUNICATION_WRITE << PGA280Def.COMMUNICATION_CMD_OFFSET) | \
              (reg << PGA280Def.PGA280_REG_OFFSET) | (content & 0xFF)
        self.spi_switch()
        self.mix_ads8900_hyc.write([raw])

    def read_register(self, reg):
        '''
        PGA280 read specific register.

        Args:
            reg:   int, PGA280 register.

        Returns:
            int, data read from register.

        Examples:
            rd = pga280.read_register(PGA280Def.PGA280_REG_0)

        '''
        assert reg in PGA280Def.REGISTERS
        raw = (PGA280Def.COMMUNICATION_READ << PGA280Def.COMMUNICATION_CMD_OFFSET) | \
              (reg << PGA280Def.PGA280_REG_OFFSET)
        self.spi_switch()
        return self.mix_ads8900_hyc.write_and_read([raw], 1)[0] & 0x00FF

    def set_gain(self, input_gain=0.125, output_gain=1):
        '''
        PGA280 set input & output gain.

        Args:
            input_gain:   instance(float) or instance(int), in list PGA280Def.InputGain.
            output_gain:  instance(float) or instance(int), in list PGA280Def.OutputGain.

        Examples:
            pga280.set_gain(0.125, 1)

        '''
        assert input_gain in PGA280Def.InputGain.keys()
        assert output_gain in PGA280Def.OutputGain.keys()
        reg0bits = self.read_register(PGA280Def.PGA280_REG_0)
        _input = PGA280Def.InputGain[input_gain] << PGA280Def.PGA280_INPUT_GAIN_OFFSET
        _output = PGA280Def.OutputGain[output_gain] << PGA280Def.PGA280_OUTPUT_GAIN_OFFSET
        if (_input != (reg0bits & PGA280Def.PGA280_INPUT_GAIN_MASK)) or \
                (_output != (reg0bits & PGA280Def.PGA280_OUTPUT_GAIN_MASK)):
            reg0bits &= ~(PGA280Def.PGA280_INPUT_GAIN_MASK | PGA280Def.PGA280_OUTPUT_GAIN_MASK)
            reg0bits |= _input | _output
            self.write_register(PGA280Def.PGA280_REG_0, reg0bits)

    def spi_switch(self):
        self.mix_ads8900_hyc.chip_select(0x03, 6250000, 16)

    def set_switch(self, switch, state):
        '''
        PGA280 set internal switch.

        Args:
            switch:   instance(int), in list PGA280Def.Switch.
            state:  instance(int), in [0, 1], 0 means OFF while 1 means ON.

        Examples:
            pga280.set_switch(PGA280.PGA280_SW_D12, 1)

        '''
        assert switch in PGA280Def.Switch
        assert state in [0, 1]
        if switch >= PGA280Def.PGA280_SW_G2:
            reg7bits = self.read_register(PGA280Def.PGA280_REG_7)
            switch >>= 8
            reg7bits &= ~switch
            if state:
                reg7bits |= switch
            self.write_register(PGA280Def.PGA280_REG_7, reg7bits)
        else:
            reg7bits = self.read_register(PGA280Def.PGA280_REG_6)
            reg7bits &= ~switch
            if state:
                reg7bits |= switch
            self.write_register(PGA280Def.PGA280_REG_6, reg7bits)

    def channel_select(self, channel):
        '''
        PGA280 select input channel.

        Args:
            channel:   instance(string), in list PGA280Def.Channel.

        Examples:
            pga280.channel_select('CHANNEL_A')

        '''
        assert channel in PGA280Def.Channel
        if PGA280Def.PGA280_CHANNEL_A == channel:
            self.set_switch(PGA280Def.PGA280_SW_B1, 0)
            self.set_switch(PGA280Def.PGA280_SW_B2, 0)
            self.set_switch(PGA280Def.PGA280_SW_A1, 1)
            self.set_switch(PGA280Def.PGA280_SW_A2, 1)
        elif PGA280Def.PGA280_CHANNEL_B == channel:
            self.set_switch(PGA280Def.PGA280_SW_A1, 0)
            self.set_switch(PGA280Def.PGA280_SW_A2, 0)
            self.set_switch(PGA280Def.PGA280_SW_B1, 1)
            self.set_switch(PGA280Def.PGA280_SW_B2, 1)
        else:
            self.set_switch(PGA280Def.PGA280_SW_A1, 0)
            self.set_switch(PGA280Def.PGA280_SW_A2, 0)
            self.set_switch(PGA280Def.PGA280_SW_B1, 0)
            self.set_switch(PGA280Def.PGA280_SW_B2, 0)

    def config_gpio_direction(self, pin_id, direction):
        '''
        PGA280 set direction of the given pin.

        Args:
            pin_id:   instance(int), 0 <= pin_id <= 6.
            direction: instance(str), ['output', 'input']

        Examples:
            pga280.config_gpio_direction(0, 'output')

        '''
        assert isinstance(pin_id, int) and 0 <= pin_id <= 6
        assert direction in PGA280Def.GPIO_Dir_Type
        reg8bits = self.read_register(PGA280Def.PGA280_REG_8)
        reg8bits &= ~(1 << pin_id)
        if direction == 'output':
            reg8bits |= 1 << pin_id
        self.write_register(PGA280Def.PGA280_REG_8, reg8bits)

    def read_gpio(self, pin_id):
        '''
        PGA280 get level of the given pin.

        Args:
            pin_id:   instance(int), 0 <= pin_id <= 6.

        Returns:
            instance(int) , 0 for low level and 1 for high level.

        Examples:
            level = pga280.read_gpio(0)
            print level

        '''
        assert isinstance(pin_id, int) and 0 <= pin_id <= 6
        reg5bits = self.read_register(PGA280Def.PGA280_REG_5)
        if (1 << pin_id) & reg5bits:
            return 1
        return 0

    def write_gpio(self, pin_id, level):
        '''
        PGA280 set pin's output level.

        Args:
            pin_id:   instance(int), 0 <= pin_id <= 6.
            level: instance(int), in [0, 1].

        Examples:
            pga280.write_gpio(0, 1)

        '''
        assert isinstance(pin_id, int) and 0 <= pin_id <= 6
        assert level in [0, 1]
        reg5bits = self.read_register(PGA280Def.PGA280_REG_5)
        reg5bits &= ~(1 << pin_id)
        if level:
            reg5bits |= 1 << pin_id
        self.write_register(PGA280Def.PGA280_REG_5, reg5bits)

    def reset(self):
        '''
        PGA280 software reset.

        Examples:
            pga280.reset()

        '''
        reg1bits = 0x01
        self.write_register(PGA280Def.PGA280_REG_1, reg1bits)
