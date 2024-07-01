# -*- coding: utf-8 -*-
from mix.driver.hyc.common.ipcore.mix_ad5761_hyc import MIXAD5761HYC


__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class SST26VF064BDef:
    TOTAL_PAGE_INDEX = 32767  # 0--32767   总共32768页
    TOTAL_SECTOR_INDEX = 2047  # 0--2047    总共2048sector

    Reset_Enable_CMD = 0x66  # 首先拉低ce脚，然后发送66，拉高ce脚
    Reset_Memory_CMD = 0x99  # 再次拉低ce脚，然后发送99,拉高ce脚，reset完成进入读模式 spi 8.。。。。
    Enable_Quad_IO_CMD = 0x38  # SQI模式
    Reset_Quad_IO_CMD = 0xff  # 某种特殊情况下需要两次才能回到spi模式
    Read_Status_Register_CMD = 0x05
    Write_Status_Register_CMD = 0x01
    Read_Configuration_Register_CMD = 0x35
    Read_Memory_CMD = 0x03  # 必须达到40Mhz，此命令只在spi模式有效，读取地址自动增加；命令后发送地址A[23：0]，ce为低
    Read_Memory_at_Higher_Speed_CMD = 0x0b  # 两种总线都支持，指令支持频率可达104Mhz（2.7—-3.6），80Mhz(2.3-3.6) Read-locked会全读出00H
    SPI_Quad_Output_Read_CMD = 0x6b
    SPI_Quad_IO_Read_CMD = 0xeb
    SPI_Dual_Output_Read_CMD = 0x3b  #
    SPI_Dual_IO_Read_CMD = 0xbb
    Set_Burst_Length_CMD = 0xc0  # both SPI and SQI  8位:00  16位:01  32位:02   64位:03
    SQI_Read_Burst_with_Wrap_CMD = 0x0c
    SPI_Read_Burst_with_Wrap_CMD = 0xec  # similar to SPI Quad I/O Read For example, if the burst
    JEDEC_ID_Read_CMD = 0x9f  # bf 26 device ID
    Quad_IO_J_ID_Read_CMD = 0xaf
    Serial_Flash_Discoverable_Parameters_CMD = 0x5a  #
    Write_Enable_CMD = 0x06
    Write_Disable_CMD = 0x04
    Erase_4KBytes_Memory_CMD = 0x20  # Sector-Erase Address bits [AMS:A12]determine the sector address (SAX);
    Erase_64_32_8_KBytes_CMD = 0xd8  # Block-Erase Address bits AMS-A13 determine the block address
    Erase_Full_CMD = 0xc7  # The Chip-Erase instruction clears all bits
    Page_Program_CMD = 0x02  # The data for the selected page address must be in the erased state (FFH)
    SQI_Quad_Page_Program_CMD = 0x32
    Suspends_ProgramErase_CMD = 0xb0  # 在对某个sector写入和擦除的过程中想要对其他sector操作，就发此命令，但是对应挂起的sector还是不能读写的
    Resumes_ProgramErase_CMD = 0x30
    Read_Block_Protection_Register_CMD = 0x72
    Write_Block_Protection_Register_CMD = 0x42
    Lock_Down_Block_Protection_Register_CMD = 0x8d
    nonVolatile_Write_LockDown_Register_CMD = 0xe8
    Global_Block_Protection_Unlock_CMD = 0x98
    Read_Security_ID_CMD = 0x88
    Program_User_Security_ID_area_CMD = 0xa5
    Lockout_Security_ID_Programming_CMD = 0x85

    CMD_Type = [
        Reset_Enable_CMD,
        Reset_Memory_CMD,
        Enable_Quad_IO_CMD,
        Reset_Quad_IO_CMD,
        Read_Status_Register_CMD,
        Write_Status_Register_CMD,
        Read_Configuration_Register_CMD,
        Read_Memory_CMD,
        Read_Memory_at_Higher_Speed_CMD,
        SPI_Quad_Output_Read_CMD,
        SPI_Quad_IO_Read_CMD,
        SPI_Dual_Output_Read_CMD,
        SPI_Dual_IO_Read_CMD,
        Set_Burst_Length_CMD,
        SQI_Read_Burst_with_Wrap_CMD,
        SPI_Read_Burst_with_Wrap_CMD,
        JEDEC_ID_Read_CMD,
        Quad_IO_J_ID_Read_CMD,
        Serial_Flash_Discoverable_Parameters_CMD,
        Write_Enable_CMD,
        Write_Disable_CMD,
        Erase_4KBytes_Memory_CMD,
        Erase_64_32_8_KBytes_CMD,
        Erase_Full_CMD,
        Page_Program_CMD,
        SQI_Quad_Page_Program_CMD,
        Suspends_ProgramErase_CMD,
        Resumes_ProgramErase_CMD,
        Read_Block_Protection_Register_CMD,
        Write_Block_Protection_Register_CMD,
        Lock_Down_Block_Protection_Register_CMD,
        nonVolatile_Write_LockDown_Register_CMD,
        Global_Block_Protection_Unlock_CMD,
        Read_Security_ID_CMD,
        Program_User_Security_ID_area_CMD,
        Lockout_Security_ID_Programming_CMD
    ]

    DUMMY_BYTE = 0x00

    FLASH_WRITE_BUSY = 0x80

    FLASH_BUSY_RETRY_MAX = 100

    BlockAddr = [0x000000, 0x002000, 0x004000, 0x006000, 0x008000, 0x010000, 0x020000, 0x030000, 0x040000, 0x050000,
                 0x060000,
                 0x070000, 0x080000, 0x090000, 0x0A0000, 0x0B0000, 0x0C0000, 0x0D0000, 0x0E0000, 0x0F0000, 0x100000,
                 0x110000,
                 0x120000, 0x130000, 0x140000, 0x150000, 0x160000, 0x170000, 0x180000, 0x190000, 0x1A0000, 0x1B0000,
                 0x1C0000,
                 0x1D0000, 0x1E0000, 0x1F0000, 0x200000, 0x210000, 0x220000, 0x230000, 0x240000, 0x250000, 0x260000,
                 0x270000,
                 0x280000, 0x290000, 0x2A0000, 0x2B0000, 0x2C0000, 0x2D0000, 0x2E0000, 0x2F0000, 0x300000, 0x310000,
                 0x320000,
                 0x330000, 0x340000, 0x350000, 0x360000, 0x370000, 0x380000, 0x390000, 0x3A0000, 0x3B0000, 0x3C0000,
                 0x3D0000,
                 0x3E0000, 0x3F0000, 0x400000, 0x410000, 0x420000, 0x430000, 0x440000, 0x450000, 0x460000, 0x470000,
                 0x480000,
                 0x490000, 0x4A0000, 0x4B0000, 0x4C0000, 0x4D0000, 0x4E0000, 0x4F0000, 0x500000, 0x510000, 0x520000,
                 0x530000,
                 0x540000, 0x550000, 0x560000, 0x570000, 0x580000, 0x590000, 0x5A0000, 0x5B0000, 0x5C0000, 0x5D0000,
                 0x5E0000,
                 0x5F0000, 0x600000, 0x610000, 0x620000, 0x630000, 0x640000, 0x650000, 0x660000, 0x670000, 0x680000,
                 0x690000,
                 0x6A0000, 0x6B0000, 0x6C0000, 0x6D0000, 0x6E0000, 0x6F0000, 0x700000, 0x710000, 0x720000, 0x730000,
                 0x740000,
                 0x750000, 0x760000, 0x770000, 0x780000, 0x790000, 0x7A0000, 0x7B0000, 0x7C0000, 0x7D0000, 0x7E0000,
                 0x7F0000,
                 0x7F8000, 0x7FA000, 0x7FC000, 0x7FE000]

    STAND_ID = 0xBF2643


class SST26VF064B(object):
    
    rpc_public_api = ['read_id', 'page_program']
    
    def __init__(self, mix_ad5761_hyc=None):
        self.mix_ad5761_hyc = mix_ad5761_hyc
        buff = [SST26VF064BDef.Reset_Enable_CMD]
        self.write(buff)
        buff = [SST26VF064BDef.Reset_Memory_CMD]
        self.write(buff)
        self.write_enable()
        buff = [SST26VF064BDef.Write_Block_Protection_Register_CMD, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.write(buff)
        buff = [SST26VF064BDef.Write_Block_Protection_Register_CMD, SST26VF064BDef.Write_Status_Register_CMD,
                0x00, 0x02]
        self.write(buff)
        print 'flash id[', hex(self.read_id()), ']'

    def write(self, data):
        assert isinstance(data, list)
        self.mix_ad5761_hyc.chip_select(0x20, 6250000, 8)
        raw = []
        for each in data:
            raw.append(each << 16)
        self.mix_ad5761_hyc.write(raw)
        self.mix_ad5761_hyc.chip_select(0x00, 6250000, 8)

    def write_and_read(self, data, size):
        assert isinstance(data, list)
        assert isinstance(size, int) and size > 0
        self.mix_ad5761_hyc.chip_select(0x20, 6250000, 8)
        raw = []
        for each in data:
            raw.append(each << 16)
        rd = self.mix_ad5761_hyc.write_and_read(raw, size)
        rd_data = []
        for each in rd:
            rd_data.append(each >> 16)
        self.mix_ad5761_hyc.chip_select(0x00, 6250000, 8)
        return rd_data

    def read_status(self):
        buff = [SST26VF064BDef.Read_Status_Register_CMD]
        return self.write_and_read(buff, 1)[0]

    def wait_busy_reset(self):
        retry = 0
        while retry < SST26VF064BDef.FLASH_BUSY_RETRY_MAX:
            status = self.read_status()
            if not (status & SST26VF064BDef.FLASH_WRITE_BUSY):
                break
            retry += 1
        if retry >= SST26VF064BDef.FLASH_BUSY_RETRY_MAX:
            return -1
        return 0

    def reset(self):
        buff = [SST26VF064BDef.Reset_Enable_CMD]
        self.write(buff)
        buff = [SST26VF064BDef.Reset_Memory_CMD]
        self.write(buff)

    def read_flash(self, addr, num):
        assert isinstance(addr, int) and 0 <= addr <= 0xFFFFFF
        assert isinstance(num, int) and num > 0
        buff = [SST26VF064BDef.Read_Memory_CMD, ((addr & 0xFF0000) >> 16) & 0xFF,
                ((addr & 0x00FF00) >> 8) & 0xFF, (addr & 0x0000FF)]
        return self.write_and_read(buff, num)

    def write_enable(self):
        buff = [SST26VF064BDef.Write_Enable_CMD]
        self.write(buff)

    def erase_sector(self, sector):
        assert isinstance(sector, int) and 0 <= sector <= 2047
        head = 4096 * sector
        self.write_enable()
        buff = [SST26VF064BDef.Erase_4KBytes_Memory_CMD, ((head & 0xFF0000) >> 16) & 0xFF,
                ((head & 0x00FF00) >> 8) & 0xFF, (head & 0x0000FF)]
        self.write(buff)
        return self.wait_busy_reset()

    def erase_block(self, block):
        assert isinstance(block, int) and 0 <= block <= len(SST26VF064BDef.BlockAddr)
        self.write_enable()
        addr = SST26VF064BDef.BlockAddr[block]
        buff = [SST26VF064BDef.Erase_64_32_8_KBytes_CMD, ((addr & 0xFF0000) >> 16) & 0xFF,
                ((addr & 0x00FF00) >> 8) & 0xFF, (addr & 0x0000FF)]
        self.write(buff)
        return self.wait_busy_reset()

    def erase_chip(self):
        self.write_enable()
        self.write([SST26VF064BDef.Erase_Full_CMD])
        return self.wait_busy_reset()

    def read_id(self):
        rd = self.write_and_read([SST26VF064BDef.JEDEC_ID_Read_CMD], 3)
        return (rd[0] << 16) | (rd[1] << 8) | rd[2]

    def page_program(self, page, offset, data):
        assert isinstance(page, int)
        assert isinstance(offset, int)
        assert isinstance(data, list)
        addr = page * 256 + offset
        self.write_enable()
        buff = [SST26VF064BDef.Page_Program_CMD, ((addr & 0xFF0000) >> 16) & 0xFF,
                ((addr & 0x00FF00) >> 8) & 0xFF, (addr & 0x0000FF)]
        buff.extend(data)
        self.write(buff)
        return self.wait_busy_reset()

