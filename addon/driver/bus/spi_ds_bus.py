from threading import Lock
from mix.driver.core.bus.gpio import GPIO
from mix.driver.core.bus.pin import Pin

'''
SPI Downstream bus driver.
'''


def lock_spi_mux(f):
    '''
    decorator to add lock and i2c-mux switch around wrapped function
    '''
    def wrapper(self, *args, **kwargs):
        with self.mux[0].mux_lock:
            if type(self.mux[0]) is GPIO:
                self.mux[0].set_level(self.channel)
            elif type(self.mux[0]) is Pin:
                if self.channel == 0:
                    self.mux[0].set_level(0)
                    self.mux[0].set_level(0)
                elif self.channel == 1:
                    self.mux[0].set_level(0)
                    self.mux[0].set_level(1)
                elif self.channel == 2:
                    self.mux[0].set_level(1)
                    self.mux[0].set_level(0)
                elif self.channel == 3:
                    self.mux[0].set_level(1)
                    self.mux[0].set_level(1)
            try:
                ret = f(self, *args, **kwargs)
            finally:
                # self.mux.set_channel_state([[self.channel, 0]])
                pass
        return ret

    return wrapper


class SPIDownstreamBus(object):
    '''
    I2C Downstream bus driverz

    ClassType = I2C

    I2C Downstream bus is the i2c bus coming from a i2c_mux's downstream channel.
    I2C master/root cannot directly talk to devices connecting to i2c downstream bus;
    A i2c mux switch is required to enable the bus beforehands.

    This driver is intended to work as a i2c bus driver but wrap mux switching action inside.
    For example, if we have a cat9555 connecting to channel 0 of i2c-mux (tca9548) on i2c bus 0,
    To read from cat9555, user software needs to do this:
        0. Create instance:
            i2c = I2C('/dev/i2c-0')
            mux = TCA9548(mux_addr, i2c)
            io_exp = CAT9555(i2c, io_exp_addr)

        1. tca9548 channel 0 enable:
            mux.enable_channel(0)
        2. read cat9555 pin:
            io_exp.get_pin(0)
        3. tca9548 channel 0 disable
            mux.disable_channel(0)
    Step 3 is required for avoid address conflict on different i2c-mux channels.

    With this driver, this could be done by less steps:
        0. Create instance:
            i2c = I2C('/dev/i2c-0')
            mux = TCA9548(mux_addr, i2c)
            i2c_ds = I2CDownStreamBus(mux, 0)
            io_exp = CAT9555(i2c_ds, io_exp_addr)
        1. read cat9555 pin:
            io_exp.get_pin(0)

    i2c-mux cascading is supported by passing a i2c-ds-bus as 1st argument of __init__().

    Args:
        mux: instance/None, a i2c mux instance that has a lock and set channel action.
                               Could be a I2CDownstreamBus instance if it is a cascading
                               i2c-mux: mux connecting to another i2c-mux's downstream channel.
        channel: int, (>0), channel number of i2c mux that this bus is coming from.

    Examples:
        # creating instance
        i2c = I2C('/dev/i2c-0')
        mux = TCA9548(mux_addr, i2c)
        i2c_ds = I2CDownStreamBus(mux, 0)

        # use i2c_ds to initiate devices
        io_exp = CAT9555(i2c_ds, io_exp_addr)

        # read cat9555 pin:
        io_exp.get_pin(0)

    '''
    rpc_public_api = ['read', 'write', 'write_and_read']
    # class lock to control lock creating action for i2c_mux;
    LOCK = Lock()

    def __init__(self, mux, spi_bus, channel):
        # channel must be specified int and >= 0.
        assert type(channel) is int
        assert channel >= 0

        if mux:
            self.mux = mux

        # existing tca9548 has _i2c_bus instance.
        self.spi = spi_bus
        # self._dev_name = self.i2c._dev_name
        self.channel = channel

        # mux instance may not have a lock; create one if not.
        # use LOCK here to ensure only 1 lock created for the same mux.
        with SPIDownstreamBus.LOCK:
            if not hasattr(mux[0], 'mux_lock'):
                self.mux[0].mux_lock = Lock()
            else:
                # already has a lock; just use it.
                pass

    # no open() because open() is called once during i2c init.
    def close(self):
        '''
        I2C bus close; will close the root bus device.
        '''
        self.spi.close()

    # @lock_spi_mux
    # def close(self):
    #     '''
    #     Close the spi device
    #
    #     Examples:
    #         axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
    #         spi = PLSPIBus(axi4_bus)
    #         spi.close()
    #
    #     '''
    #     return self.spi.close()

    @lock_spi_mux
    def set_timeout(self, timeout):
        '''
        Set the timeout for waiting for the ipcore state to be ready

        Args:
            timeout:    float, unit s.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            # set 0.1s timeout for polling the ipcore status register
            spi.set_timeout(0.1)

        '''
        self.spi.set_timeout(timeout)

    @lock_spi_mux
    def set_work_mode(self, quad_mode):
        '''
        Set the spi working mode. The MIX QSPI IPcore supports SPI / QPI mode

        Args:
            quad_mode:    int, [0, 1], 0: SPI mode, 1: QPI mode.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            # set the spi working mode to SPI mode.
            spi.set_work_mode(PLSPIDef.SPI_MODE)

        '''
        return self.spi.set_work_mode(quad_mode)

    @lock_spi_mux
    def get_work_mode(self):
        '''
        Get spi working mode

        Returns:
            int, [0, 1], 0: SPI mode, 1: QPI mode.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            ret = spi.set_work_mode()   # ret == 0

        '''
        return self.spi.get_work_mode()

    @lock_spi_mux
    def set_mode(self, mode):
        '''
        Set the spi bus clock polarity and phase mode

        Args:
            mode:   string, ['MODE0', 'MODE1', 'MODE2', 'MODE3'], set mode.
            +---------+---------+----------+
            | Mode    |   CPOL  |   CPHA   |
            +=========+=========+==========+
            |    0    |    0    |     0    |
            +---------+---------+----------+
            |    1    |    0    |     1    |
            +---------+---------+----------+
            |    2    |    1    |     0    |
            +---------+---------+----------+
            |    3    |    1    |     1    |
            +---------+---------+----------+

        Examples:
            # set polarity to 0, phase to 0.
            spi.set_mode("MODE0")

        '''
        return self.spi.set_mode(mode)

    @lock_spi_mux
    def get_mode(self):
        '''
        Get the spi bus clock polarity and phase mode

        Returns:
            string, ['MODE0', 'MODE1', 'MODE2', 'MODE3'], 'MODE0': CPOL=0, CPHA=0
                                                          'MODE1': CPOL=0, CPHA=1
                                                          'MODE2': CPOL=1, CPHA=0
                                                          'MODE3': CPOL=1, CPHA=1

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            ret = spi.get_mode()  # ret == "MODE0"

        '''
        return self.spi.get_mode()

    @lock_spi_mux
    def get_base_clock(self):
        '''
        Get the ipcore base clock frequency

        Returns:
            int, value, unit kHz.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            ret = spi.get_base_clock()  # ret == 125000

        '''
        return self.spi.get_base_clock()

    @lock_spi_mux
    def set_speed(self, speed):
        '''
        Set the spi bus clock speed

        Args:
            speed:  int, [2~20000000], unit Hz, 1000000 means 1000000Hz.

        Examples:
            # set clock speed to 10MHz
            spi.set_speed(10000000)

        '''
        return self.spi.set_speed(speed)

    @lock_spi_mux
    def get_speed(self):
        '''
        Get the spi bus clock speed

        Returns:
            int, value, unit Hz.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            ret = spi.get_speed()   # ret == 10000000

        '''
        return self.spi.get_speed()

    @lock_spi_mux
    def set_cs(self, cs_mode):
        '''
        Set the chip select signal level

        Args:
            cs_mode:    int, [0, 1], 0: CS_LOW, 1: CS_HIGH.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            # set the chip select signal to low level.
            spi.set_cs(PLSPIDef.CS_LOW)

        '''
        return self.spi.set_cs(cs_mode)

    @lock_spi_mux
    def read(self, rd_len):
        '''
        Read data from spi bus. This function will control the chip select signal

        Args:
            rd_len:    int, (>0), Length of read data.

        Returns:
            list, [value], Data to be read, the list element is an integer, bit width: 8 bits.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            spi.read(100)

        '''
        return self.spi.read(rd_len)

    @lock_spi_mux
    def write(self, wr_data):
        '''
        Write data to spi bus. This function will control the chip select signal

        Args:
            wr_data:    list, Data to write, the list element is an integer, bit width: 8 bits.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            spi.set_mode("MODE0")
            spi.write([0x01, 0x02, 0x03, 0x04, 0x05, 0x06])

        '''
        return self.spi.write(wr_data)

    @lock_spi_mux
    def sync_transfer(self, wr_data):
        '''
        This function only supports standard spi mode
        Write data to the spi bus. At the same time, the same length of data is read

        Args:
            wr_data:    list, Data to write, the list element is an integer, bit width: 8 bits.

        Returns:
            list, [value], Data to be read, the list element is an integer, bit width: 8 bits.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            spi.set_mode("MODE0")
            spi.set_work_mode("SPI")
            to_send = [0x01, 0x03, 0x04, 0x06]
            ret = spi.sync_transfer(to_send) # len(ret) == len(to_send)

        '''
        return self.spi.sync_transfer(wr_data)

    @lock_spi_mux
    def async_transfer(self, wr_data, rd_len):
        '''
        This function supports SPI and QPI mode
        First write data to the spi bus, then read data from the spi bus

        Args:
            wr_data:    list, Data to write, the list element is an integer, bit width: 8 bits.
            rd_len:     int, Length of read data.

        Returns:
            list, [value], Data to be read, the list element is an integer, bit width: 8 bits.

        Examples:
            axi4_bus = AXI4LiteBus('/dev/MIX_QSPI', 8192)
            spi = PLSPIBus(axi4_bus)
            spi.set_mode("MODE0")
            spi.set_work_mode("QPI")
            ret = spi.async_transfer([0x01,0x02,0x03,0x04], 3)   # len(ret) == 3

        '''
        return self.spi.async_transfer(wr_data, rd_len)

    @lock_spi_mux
    def transfer(self, wr_data, rd_len, sync=True):
        return self.spi.transfer(wr_data, rd_len, sync)
