from mix.driver.core.ic.io_expander_base import IOExpanderBase

class TCA6408Def:
    TCA6408_REG_Input = 0x00
    TCA6408_REG_Output = 0x01
    TCA6408_REG_Polarity = 0x02
    TCA6408_REG_Configuration = 0x03

    REGISTERS = [
        TCA6408_REG_Input,
        TCA6408_REG_Output,
        TCA6408_REG_Polarity,
        TCA6408_REG_Configuration
    ]

    TCA6408_PORT_0 = 0x1
    TCA6408_PORT_1 = 0x2
    TCA6408_PORT_2 = 0x4
    TCA6408_PORT_3 = 0x8
    TCA6408_PORT_4 = 0x10
    TCA6408_PORT_5 = 0x20
    TCA6408_PORT_6 = 0x40
    TCA6408_PORT_7 = 0x80

    PORT = [
        TCA6408_PORT_0,
        TCA6408_PORT_1,
        TCA6408_PORT_2,
        TCA6408_PORT_3,
        TCA6408_PORT_4,
        TCA6408_PORT_5,
        TCA6408_PORT_6,
        TCA6408_PORT_7
    ]

    TCA6408_PIN_DIR_OUTPUT = 1
    PCA6408_PIN_DIR_INPUT = 0

    Dir_Type = {
        'input': 1,
        'output': 0
    }


class TCA6408(IOExpanderBase):
    def __init__(self, dev_addr, i2c_bus=None):
        self.__dev_addr = dev_addr
        self.i2c_bus = i2c_bus
        super(TCA6408, self).__init__()

    def read_register(self, reg):
        assert isinstance(reg, int) and reg in TCA6408Def.REGISTERS
        data = [reg]
        rd = self.i2c_bus.write_and_read(self.__dev_addr, data, 1)
        return rd[0]

    def write_register(self, reg, content):
        assert reg in TCA6408Def.REGISTERS
        data = [reg]
        data.append(content)
        self.i2c_bus.write(self.__dev_addr, data)

    def set_pin_dir(self, pin_id, direction):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 7
        rd = self.read_register(TCA6408Def.TCA6408_REG_Configuration)
        rd &= ~(1 << pin_id)
        rd |= TCA6408Def.Dir_Type[direction] << pin_id
        self.write_register(TCA6408Def.TCA6408_REG_Configuration, rd)

    def get_pin_dir(self, pin_id):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 7
        port = pin_id / 8
        pin = pin_id % 8
        rd = self.read_register(TCA6408Def.TCA6408_REG_Configuration)
        if rd & (1 << pin):
            return 'input'
        return 'output'

    def set_pin(self, pin_id, level):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 7
        assert level in (0, 1)
        # print[pin_id, level]
        rd = self.read_register(TCA6408Def.TCA6408_PIN_DIR_OUTPUT)
        if (rd & (1 << pin_id)) != (level << pin_id):
            rd &= ~(1 << pin_id)
            rd |= level << pin_id
            self.write_register(TCA6408Def.TCA6408_PIN_DIR_OUTPUT, rd)

    def get_pin(self, pin_id):
        assert isinstance(pin_id, int) and 0 <= pin_id <= 7
        rd = self.read_register(TCA6408Def.TCA6408_REG_Input)
        if rd & (1 << pin_id):
            return 1
        return 0
