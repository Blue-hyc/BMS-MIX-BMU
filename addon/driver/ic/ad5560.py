# -*- coding: utf-8 -*-
import time
from mix.driver.hyc.common.ipcore.mix_ad5761_hyc import *
from mix.driver.hyc.common.ipcore.mix_ad5761_hyc_emulator import MIXAD5761HYCEmulator

__author__ = "wanghong@hyc.cn"
__version__ = "0.1"


class AD5560Def:
    AD5560_REG_NOP = 0x00
    AD5560_REG_SYS_CTRL = 0x01
    AD5560_REG_DPS_1 = 0x02
    AD5560_REG_DPS_2 = 0x03
    AD5560_REG_COMP_1 = 0x04
    AD5560_REG_COMP_2 = 0x05
    AD5560_REG_ALM_SETUP = 0x06
    AD5560_REG_DIAG = 0x07
    AD5560_REG_FIN_DAC_x1 = 0x08
    AD5560_REG_FIN_DAC_m = 0x09
    AD5560_REG_FIN_DAC_c = 0x0A
    AD5560_REG_OFFSET_DAC_x = 0x0B
    AD5560_REG_OSD_DAC_x = 0x0C
    AD5560_REG_CLL_DAC_x1 = 0x0D
    AD5560_REG_CLL_DAC_m = 0x0E
    AD5560_REG_CLL_DAC_c = 0x0F
    AD5560_REG_CLH_DAC_x1 = 0x10
    AD5560_REG_CLH_DAC_m = 0x11
    AD5560_REG_CLH_DAC_c = 0x12
    AD5560_REG_CPL_DAC_x1_5uA = 0x13
    AD5560_REG_CPL_DAC_m_5uA = 0x14
    AD5560_REG_CPL_DAC_c_5uA = 0x15
    AD5560_REG_CPL_DAC_x1_25uA = 0x16
    AD5560_REG_CPL_DAC_m_25uA = 0x17
    AD5560_REG_CPL_DAC_c_25uA = 0x18
    AD5560_REG_CPL_DAC_x1_250uA = 0x19
    AD5560_REG_CPL_DAC_m_250uA = 0x1A
    AD5560_REG_CPL_DAC_c_250uA = 0x1B
    AD5560_REG_CPL_DAC_x1_2_5mA = 0x1C
    AD5560_REG_CPL_DAC_m_2_5mA = 0x1D
    AD5560_REG_CPL_DAC_c_2_5mA = 0x1E
    AD5560_REG_CPL_DAC_x1_25mA = 0x1F
    AD5560_REG_CPL_DAC_m_25mA = 0x20
    AD5560_REG_CPL_DAC_c_25mA = 0x21
    AD5560_REG_CPL_DAC_x1_EXT2_500mA = 0x22
    AD5560_REG_CPL_DAC_m_EXT2_500mA = 0x23
    AD5560_REG_CPL_DAC_c_EXT2_500mA = 0x24
    AD5560_REG_CPL_DAC_x1_EXT1_1_2A = 0x25
    AD5560_REG_CPL_DAC_m_EXT1_1_2A = 0x26
    AD5560_REG_CPL_DAC_c_EXT1_1_2A = 0x27
    AD5560_REG_CPH_DAC_x1_5uA = 0x28
    AD5560_REG_CPH_DAC_m_5uA = 0x29
    AD5560_REG_CPH_DAC_c_5uA = 0x2A
    AD5560_REG_CPH_DAC_x1_25uA = 0x2B
    AD5560_REG_CPH_DAC_m_25uA = 0x2C
    AD5560_REG_CPH_DAC_c_25uA = 0x2D
    AD5560_REG_CPH_DAC_x1_250uA = 0x2E
    AD5560_REG_CPH_DAC_m_250uA = 0x2F
    AD5560_REG_CPH_DAC_c_250uA = 0x30
    AD5560_REG_CPH_DAC_x1_2_5mA = 0x31
    AD5560_REG_CPH_DAC_m_2_5mA = 0x32
    AD5560_REG_CPH_DAC_c_2_5mA = 0x33
    AD5560_REG_CPH_DAC_x1_25mA = 0x34
    AD5560_REG_CPH_DAC_m_25mA = 0x35
    AD5560_REG_CPH_DAC_c_25mA = 0x36
    AD5560_REG_CPH_DAC_x1_EXT2_500mA = 0x37
    AD5560_REG_CPH_DAC_m_EXT2_500mA = 0x38
    AD5560_REG_CPH_DAC_c_EXT2_500mA = 0x39
    AD5560_REG_CPH_DAC_x1_EXT1_1_2A = 0x3A
    AD5560_REG_CPH_DAC_m_EXT1_1_2A = 0x3B
    AD5560_REG_CPH_DAC_c_EXT1_1_2A = 0x3C
    AD5560_REG_DGS_DAC = 0x3D
    AD5560_REG_RAMP_END_CODE = 0x3E
    AD5560_REG_RAMP_SETP_SIZE = 0x3F
    AD5560_REG_RCLK_DIVIDER = 0x40
    AD5560_REG_ENABLE_RAMP = 0x41
    AD5560_REG_INT_RAMP = 0x42
    AD5560_REG_ALARM_STATUS = 0x43
    AD5560_REG_ALARM_STATUS_CLR_ALARM = 0x44

    REGISTERS = [
        AD5560_REG_NOP,
        AD5560_REG_SYS_CTRL,
        AD5560_REG_DPS_1,
        AD5560_REG_DPS_2,
        AD5560_REG_COMP_1,
        AD5560_REG_COMP_2,
        AD5560_REG_ALM_SETUP,
        AD5560_REG_DIAG,
        AD5560_REG_FIN_DAC_x1,
        AD5560_REG_FIN_DAC_m,
        AD5560_REG_FIN_DAC_c,
        AD5560_REG_OFFSET_DAC_x,
        AD5560_REG_OSD_DAC_x,
        AD5560_REG_CLL_DAC_x1,
        AD5560_REG_CLL_DAC_m,
        AD5560_REG_CLL_DAC_c,
        AD5560_REG_CLH_DAC_x1,
        AD5560_REG_CLH_DAC_m,
        AD5560_REG_CLH_DAC_c,
        AD5560_REG_CPL_DAC_x1_5uA,
        AD5560_REG_CPL_DAC_m_5uA,
        AD5560_REG_CPL_DAC_c_5uA,
        AD5560_REG_CPL_DAC_x1_25uA,
        AD5560_REG_CPL_DAC_m_25uA,
        AD5560_REG_CPL_DAC_c_25uA,
        AD5560_REG_CPL_DAC_x1_250uA,
        AD5560_REG_CPL_DAC_m_250uA,
        AD5560_REG_CPL_DAC_c_250uA,
        AD5560_REG_CPL_DAC_x1_2_5mA,
        AD5560_REG_CPL_DAC_m_2_5mA,
        AD5560_REG_CPL_DAC_c_2_5mA,
        AD5560_REG_CPL_DAC_x1_25mA,
        AD5560_REG_CPL_DAC_m_25mA,
        AD5560_REG_CPL_DAC_c_25mA,
        AD5560_REG_CPL_DAC_x1_EXT2_500mA,
        AD5560_REG_CPL_DAC_m_EXT2_500mA,
        AD5560_REG_CPL_DAC_c_EXT2_500mA,
        AD5560_REG_CPL_DAC_x1_EXT1_1_2A,
        AD5560_REG_CPL_DAC_m_EXT1_1_2A,
        AD5560_REG_CPL_DAC_c_EXT1_1_2A,
        AD5560_REG_CPH_DAC_x1_5uA,
        AD5560_REG_CPH_DAC_m_5uA,
        AD5560_REG_CPH_DAC_c_5uA,
        AD5560_REG_CPH_DAC_x1_25uA,
        AD5560_REG_CPH_DAC_m_25uA,
        AD5560_REG_CPH_DAC_c_25uA,
        AD5560_REG_CPH_DAC_x1_250uA,
        AD5560_REG_CPH_DAC_m_250uA,
        AD5560_REG_CPH_DAC_c_250uA,
        AD5560_REG_CPH_DAC_x1_2_5mA,
        AD5560_REG_CPH_DAC_m_2_5mA,
        AD5560_REG_CPH_DAC_c_2_5mA,
        AD5560_REG_CPH_DAC_x1_25mA,
        AD5560_REG_CPH_DAC_m_25mA,
        AD5560_REG_CPH_DAC_c_25mA,
        AD5560_REG_CPH_DAC_x1_EXT2_500mA,
        AD5560_REG_CPH_DAC_m_EXT2_500mA,
        AD5560_REG_CPH_DAC_c_EXT2_500mA,
        AD5560_REG_CPH_DAC_x1_EXT1_1_2A,
        AD5560_REG_CPH_DAC_m_EXT1_1_2A,
        AD5560_REG_CPH_DAC_c_EXT1_1_2A,
        AD5560_REG_DGS_DAC,
        AD5560_REG_RAMP_END_CODE,
        AD5560_REG_RAMP_SETP_SIZE,
        AD5560_REG_RCLK_DIVIDER,
        AD5560_REG_ENABLE_RAMP,
        AD5560_REG_INT_RAMP,
        AD5560_REG_ALARM_STATUS,
        AD5560_REG_ALARM_STATUS_CLR_ALARM,
    ]

    COMMUNICATION_WRITE = 0x000000
    COMMUNICATION_READ = 0x800000

    COMMUNICATION = [
        COMMUNICATION_WRITE,
        COMMUNICATION_READ
    ]

    AD5560_CLEN_ENABLE_OFFSET = 4
    AD5560_CLEN_ENABLE_MASK = 1 << AD5560_CLEN_ENABLE_OFFSET

    AD5560_SW_INH_OFFSET = 15
    AD5560_SW_INH_MASK = 1 << AD5560_SW_INH_OFFSET

    AD5560_ME_ENABLE_MASK = 0x0100
    AD5560_ME_ENABLE_OFFSET = 8

    AD5560_CMP_TYPE_OFFSET = 9
    AD5560_CMP_TYPE_MASK = 3 << AD5560_CMP_TYPE_OFFSET

    AD5560_CMP_TYPE_NONE = 1 << AD5560_CMP_TYPE_OFFSET
    AD5560_CMP_TYPE_CURRENT = 2 << AD5560_CMP_TYPE_OFFSET
    AD5560_CMP_TYPE_VOLT = 3 << AD5560_CMP_TYPE_OFFSET

    CMP_Type = [
        AD5560_CMP_TYPE_NONE,
        AD5560_CMP_TYPE_CURRENT,
        AD5560_CMP_TYPE_VOLT
    ]

    AD5560_CURRENT_RANGE_OFFSET = 11
    AD5560_CURRENT_RANGE_MASK = 7 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_5uA = 0 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_25uA = 1 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_250uA = 2 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_2_5mA = 3 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_25mA = 4 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_EXT2 = 5 << AD5560_CURRENT_RANGE_OFFSET
    AD5560_CURRENT_RANGE_EXT1 = 6 << AD5560_CURRENT_RANGE_OFFSET

    CURRENT_Range = [
        AD5560_CURRENT_RANGE_5uA,
        AD5560_CURRENT_RANGE_25uA,
        AD5560_CURRENT_RANGE_250uA,
        AD5560_CURRENT_RANGE_2_5mA,
        AD5560_CURRENT_RANGE_25mA,
        AD5560_CURRENT_RANGE_EXT2,
        AD5560_CURRENT_RANGE_EXT1
    ]

    CPH_Reg = {
        AD5560_CURRENT_RANGE_5uA: AD5560_REG_CPH_DAC_x1_5uA,
        AD5560_CURRENT_RANGE_25uA: AD5560_REG_CPH_DAC_x1_25uA,
        AD5560_CURRENT_RANGE_250uA: AD5560_REG_CPH_DAC_x1_250uA,
        AD5560_CURRENT_RANGE_2_5mA: AD5560_REG_CPH_DAC_x1_2_5mA,
        AD5560_CURRENT_RANGE_25mA: AD5560_REG_CPH_DAC_x1_25mA,
        AD5560_CURRENT_RANGE_EXT2: AD5560_REG_CPH_DAC_x1_EXT2_500mA,
        AD5560_CURRENT_RANGE_EXT1: AD5560_REG_CPH_DAC_x1_EXT1_1_2A
    }

    CPL_Reg = {
        AD5560_CURRENT_RANGE_5uA: AD5560_REG_CPL_DAC_x1_5uA,
        AD5560_CURRENT_RANGE_25uA: AD5560_REG_CPL_DAC_x1_25uA,
        AD5560_CURRENT_RANGE_250uA: AD5560_REG_CPL_DAC_x1_250uA,
        AD5560_CURRENT_RANGE_2_5mA: AD5560_REG_CPL_DAC_x1_2_5mA,
        AD5560_CURRENT_RANGE_25mA: AD5560_REG_CPL_DAC_x1_25mA,
        AD5560_CURRENT_RANGE_EXT2: AD5560_REG_CPL_DAC_x1_EXT2_500mA,
        AD5560_CURRENT_RANGE_EXT1: AD5560_REG_CPL_DAC_x1_EXT1_1_2A
    }

    AD5560_MEASOUT_OFFSET = 5
    AD5560_MEASOUT_MASK = 0x00E0

    AD5560_MEASOUT_HIGH_Z = 0 << AD5560_MEASOUT_OFFSET
    AD5560_MEASOUT_I_SENSE = 1 << AD5560_MEASOUT_OFFSET
    AD5560_MEASOUT_V_SENSE = 2 << AD5560_MEASOUT_OFFSET
    AD5560_MEASOUT_K_SENSE = 3 << AD5560_MEASOUT_OFFSET
    AD5560_MEASOUT_T_SENSE = 4 << AD5560_MEASOUT_OFFSET

    ME_Type = [
        AD5560_MEASOUT_HIGH_Z,
        AD5560_MEASOUT_I_SENSE,
        AD5560_MEASOUT_V_SENSE,
        AD5560_MEASOUT_K_SENSE,
        AD5560_MEASOUT_T_SENSE
    ]

    AD5560_MODE_OFFSET = 9
    AD5560_MODE_MASK = 3 << AD5560_MODE_OFFSET
    AD5560_MODE_MASTER_OUT_INTERNAL = 0 << AD5560_MODE_OFFSET
    AD5560_MODE_MASTER_MI = 1 << AD5560_MODE_OFFSET
    AD5560_MODE_SLAVE_FV = 2 << AD5560_MODE_OFFSET
    AD5560_MODE_SLAVE_FI = 3 << AD5560_MODE_OFFSET

    MODE_Type = [
        AD5560_MODE_MASTER_OUT_INTERNAL,
        AD5560_MODE_MASTER_MI,
        AD5560_MODE_SLAVE_FV,
        AD5560_MODE_SLAVE_FI
    ]

    AD5560_SR_OFFSET = 12
    AD5560_SR_MASK = 7 << AD5560_SR_OFFSET

    AD5560_INT10K_OFFSET = 8
    AD5560_INT10K_MASK = 1 << AD5560_INT10K_OFFSET

    AD5560_GUARD_HIGHZ_OFFSET = 7
    AD5560_GUARD_HIGHZ_MASK = 1 << AD5560_GUARD_HIGHZ_OFFSET

    AD5560_CPO_OFFSET = 10
    AD5560_CPO_MASK = 1 << AD5560_CPO_OFFSET

    AD5560_PD_OFFSET = 9
    AD5560_PD_MASK = 1 << AD5560_PD_OFFSET

    AD5560_GAIN_OFFSET = 12
    AD5560_GAIN_MASK = 3 << AD5560_GAIN_OFFSET

    AD5560_GAIN_0 = 0 << AD5560_GAIN_OFFSET
    AD5560_GAIN_1 = 1 << AD5560_GAIN_OFFSET
    AD5560_GAIN_2 = 2 << AD5560_GAIN_OFFSET
    AD5560_GAIN_3 = 3 << AD5560_GAIN_OFFSET

    AD5560_MEASOUT_GAIN = 0
    AD5560_MI_GAIN = 1

    GAIN_Type = {
        AD5560_GAIN_0: {AD5560_MEASOUT_GAIN: 1.0, AD5560_MI_GAIN: 20.0},
        AD5560_GAIN_1: {AD5560_MEASOUT_GAIN: 1.0, AD5560_MI_GAIN: 10.0},
        AD5560_GAIN_2: {AD5560_MEASOUT_GAIN: 0.2, AD5560_MI_GAIN: 20.0},
        AD5560_GAIN_3: {AD5560_MEASOUT_GAIN: 0.2, AD5560_MI_GAIN: 10.0},
    }

    AD5560_Rz_OFFSET = 12
    AD5560_Rz_MASK = 7 << AD5560_Rz_OFFSET
    AD5560_Rz_500Ohm = 0 << AD5560_Rz_OFFSET
    AD5560_Rz_1_6kOhm = 1 << AD5560_Rz_OFFSET
    AD5560_Rz_5kOhm = 2 << AD5560_Rz_OFFSET
    AD5560_Rz_16kOhm = 3 << AD5560_Rz_OFFSET
    AD5560_Rz_50kOhm = 4 << AD5560_Rz_OFFSET
    AD5560_Rz_160kOhm = 5 << AD5560_Rz_OFFSET
    AD5560_Rz_500kOhm = 6 << AD5560_Rz_OFFSET
    AD5560_Rz_1_6MOhm = 7 << AD5560_Rz_OFFSET

    Rz_Type = [
        AD5560_Rz_500Ohm,
        AD5560_Rz_1_6kOhm,
        AD5560_Rz_5kOhm,
        AD5560_Rz_16kOhm,
        AD5560_Rz_50kOhm,
        AD5560_Rz_160kOhm,
        AD5560_Rz_500kOhm,
        AD5560_Rz_1_6MOhm
    ]

    AD5560_Rp_OFFSET = 9
    AD5560_Rp_MASK = 7 << AD5560_Rp_OFFSET
    AD5560_Rp_200Ohm = 0 << AD5560_Rp_OFFSET
    AD5560_Rp_675kOhm = 1 << AD5560_Rp_OFFSET
    AD5560_Rp_2280Ohm = 2 << AD5560_Rp_OFFSET
    AD5560_Rp_7700Ohm = 3 << AD5560_Rp_OFFSET
    AD5560_Rp_26kOhm = 4 << AD5560_Rp_OFFSET
    AD5560_Rp_88kOhm = 5 << AD5560_Rp_OFFSET
    AD5560_Rp_296kOhm = 6 << AD5560_Rp_OFFSET
    AD5560_Rp_1MOhm = 7 << AD5560_Rp_OFFSET

    Rp_Type = [
        AD5560_Rp_200Ohm,
        AD5560_Rp_675kOhm,
        AD5560_Rp_2280Ohm,
        AD5560_Rp_7700Ohm,
        AD5560_Rp_26kOhm,
        AD5560_Rp_88kOhm,
        AD5560_Rp_296kOhm,
        AD5560_Rp_1MOhm,
    ]

    AD5560_Gm_OFFSET = 7
    AD5560_Gm_MASK = 3 << AD5560_Gm_OFFSET
    AD5560_Gm_40 = 0 << AD5560_Gm_OFFSET
    AD5560_Gm_80 = 1 << AD5560_Gm_OFFSET
    AD5560_Gm_300 = 2 << AD5560_Gm_OFFSET
    AD5560_Gm_900 = 3 << AD5560_Gm_OFFSET

    Gm_Type = [
        AD5560_Gm_40,
        AD5560_Gm_80,
        AD5560_Gm_300,
        AD5560_Gm_900
    ]

    AD5560_Cf_OFFSET = 4
    AD5560_Cf_MASK = 7 << AD5560_Cf_OFFSET
    AD5560_Cf_0 = 1 << AD5560_Cf_OFFSET
    AD5560_Cf_1 = 2 << AD5560_Cf_OFFSET
    AD5560_Cf_2 = 3 << AD5560_Cf_OFFSET
    AD5560_Cf_3 = 4 << AD5560_Cf_OFFSET
    AD5560_Cf_4 = 5 << AD5560_Cf_OFFSET

    Cf_Type = [
        AD5560_Cf_0,
        AD5560_Cf_1,
        AD5560_Cf_2,
        AD5560_Cf_3,
        AD5560_Cf_4,
    ]

    # Cc3 Cc2 Cc1
    AD5560_Cc_OFFSET = 1
    AD5560_Cc_MASK = 7 << AD5560_Cc_OFFSET
    AD5560_Cc_0001 = 0 << AD5560_Cc_OFFSET
    AD5560_Cc_0011 = 1 << AD5560_Cc_OFFSET
    AD5560_Cc_0101 = 2 << AD5560_Cc_OFFSET
    AD5560_Cc_0111 = 3 << AD5560_Cc_OFFSET
    AD5560_Cc_1001 = 4 << AD5560_Cc_OFFSET
    AD5560_Cc_1011 = 5 << AD5560_Cc_OFFSET
    AD5560_Cc_1101 = 6 << AD5560_Cc_OFFSET
    AD5560_Cc_1111 = 7 << AD5560_Cc_OFFSET

    Cc_Type = [
        AD5560_Cc_0001,
        AD5560_Cc_0011,
        AD5560_Cc_0101,
        AD5560_Cc_0111,
        AD5560_Cc_1001,
        AD5560_Cc_1011,
        AD5560_Cc_1101,
        AD5560_Cc_1111
    ]

    AD5560_ALARM_LTMPALM = 1 << 15
    AD5560_ALARM_TMPALM = 1 << 14
    AD5560_ALARM_LOSALM = 1 << 13
    AD5560_ALARM_OSALM = 1 << 12
    AD5560_ALARM_LDUTALM = 1 << 11
    AD5560_ALARM_DUTALM = 1 << 10
    AD5560_ALARM_LCLALM = 1 << 9
    AD5560_ALARM_CLALM = 1 << 8
    AD5560_ALARM_LGRDLAM = 1 << 7
    AD5560_ALARM_GRDALM = 1 << 6
    AD5560_ALARM_CPOL = 1 << 5
    AD5560_ALARM_CPOH = 1 << 4

    Alarm_Type = [
        AD5560_ALARM_LTMPALM,
        AD5560_ALARM_TMPALM,
        AD5560_ALARM_LOSALM,
        AD5560_ALARM_OSALM,
        AD5560_ALARM_LDUTALM,
        AD5560_ALARM_DUTALM,
        AD5560_ALARM_LCLALM,
        AD5560_ALARM_CLALM,
        AD5560_ALARM_LGRDLAM,
        AD5560_ALARM_GRDALM,
        AD5560_ALARM_CPOL,
        AD5560_ALARM_CPOH
    ]

    AD5560_DIS_DUT_ALARM_OFFSET = 10


class AD5560Exception(Exception):
    def __init__(self, err_str):
        self.err_reason = 'AD5560: %s.' % err_str

    def __str__(self):
        return self.err_reason


class AD5560(object):
    '''
    The AD5560 is a low power, low noise, completely integrated analog front end for high precision
    measurement applications.

    Examples:
        axi4_bus = AXI4LiteBus('/dev/quad_spi_0', 8192)
        spi_bus = PLSPIBus(axi4_bus)
        spi_bus.set_work_mode(PLSPIDef.SPI_MODE)
        spi_bus.set_mode("MODE3")
        spi_bus.set_speed(1000000)
        ad7124 = AD5560(spi_bus)
    '''
    rpc_public_api = ['write_register', 'read_register', 'set_dac', 'enable_sw_inh', 'reset',
                      'set_measout_type', 'set_clamp', 'set_mode', 'set_comparator', 'set_current_range', 'enable_pd',
                      'set_gain', 'set_manual_compensation', 'read_alarm']

    def __init__(self, reference, mix_ad5761_hyc=None):
        assert isinstance(reference, float)
        if mix_ad5761_hyc is None:
            self.mix_ad5761_hyc = MIXAD5761HYCEmulator('ad5560_emulator')
        else:
            self.mix_ad5761_hyc = mix_ad5761_hyc
        self._reference = reference

    def spi_switch(self):
        self.mix_ad5761_hyc.chip_select(0, 6250000, 24)

    def write_register(self, reg, content):
        '''
        AD5560 write specific register.

        Args:
            reg:   instance(int), [0~0xFF], .
            content:  instance(int).

        Examples:
            ad5560.write_register(AD5560Def.AD5560_REG_SYS_CTRL, 0x00)

        '''
        assert reg in AD5560Def.REGISTERS
        assert isinstance(content, int)
        raw = AD5560Def.COMMUNICATION_WRITE | (reg << 16) | (content & 0xFFFF)
        self.spi_switch()
        self.mix_ad5761_hyc.write([raw])

    def read_register(self, reg):
        '''
        AD5560 read specific register.

        Args:
            reg:   instance(int), [0~0xFF], .

        Returns:
            int.

        Examples:
            rd = ad5560.read_register(AD5560Def.AD5560_REG_SYS_CTRL)

        '''
        assert reg in AD5560Def.REGISTERS
        raw = AD5560Def.COMMUNICATION_READ | (reg << 16)
        self.spi_switch()
        return self.mix_ad5761_hyc.write_and_read([raw], 1)[0] & 0xFFFF

    def set_dac(self, volt):
        '''
        AD5560 set internal DAC.

        Args:
            volt:   instance(float).

        Examples:
            ad5560.set_dac(1.0)

        '''
        assert isinstance(volt, float) or isinstance(volt, int)
        if volt > 0:
            dac = int(volt * 1.0 * 65535 / (5.125 * self._reference) + 0.5 + 0x8000)
        else:
            dac = int(volt * 1.0 * 65535 / (5.125 * self._reference) - 0.5 + 0x8000)
        self.write_register(AD5560Def.AD5560_REG_FIN_DAC_x1, dac)

    def enable_sw_inh(self, enable=True):
        '''
        AD5560 enable software inhibit.

        Args:
            enable:   instance(bool).

        Examples:
            ad5560.enable_sw_inh(False)

        '''
        assert isinstance(enable, bool)
        self.set_dut_alarm(1)
        dsp_reg1bits = self.read_register(AD5560Def.AD5560_REG_DPS_1)
        if enable:
            dsp_reg1bits &= ~AD5560Def.AD5560_SW_INH_MASK
        else:
            dsp_reg1bits |= AD5560Def.AD5560_SW_INH_MASK
        self.write_register(AD5560Def.AD5560_REG_DPS_1, dsp_reg1bits)

    def set_dut_alarm(self, state):
        '''
        AD5560 set or reset dut alarm.

        Args:
            state:   instance(int), [0, 1].

        Examples:
            ad5560.set_dut_alarm(0)

        '''
        assert state in (0, 1)
        alarm_setup_reg1bits = self.read_register(AD5560Def.AD5560_REG_ALM_SETUP)
        alarm_setup_reg1bits |= state << AD5560Def.AD5560_DIS_DUT_ALARM_OFFSET
        self.write_register(AD5560Def.AD5560_REG_ALM_SETUP, alarm_setup_reg1bits)

    def set_measout_type(self, measout=AD5560Def.AD5560_MEASOUT_HIGH_Z):
        '''
        AD5560 set measure out type.

        Args:
            measout:   instance(int) and in AD5560Def.ME_Type.

        Examples:
            ad5560.set_measout_type(AD5560Def.AD5560_MEASOUT_I_SENSE)

        '''
        assert measout in AD5560Def.ME_Type
        dsp_reg1bits = self.read_register(AD5560Def.AD5560_REG_DPS_1)
        dsp_reg1bits &= ~AD5560Def.AD5560_ME_ENABLE_MASK
        dsp_reg1bits |= 1 << AD5560Def.AD5560_ME_ENABLE_OFFSET
        dsp_reg1bits &= ~AD5560Def.AD5560_MEASOUT_MASK
        dsp_reg1bits |= measout
        self.write_register(AD5560Def.AD5560_REG_DPS_1, dsp_reg1bits)

    def set_clamp(self, volt_pos, volt_neg):
        '''
        AD5560 set positive and negative clamp voltage.

        Args:
            volt_pos:   instance(float), must be positive.
            volt_neg:   instance(float), must be negative.

        Examples:
            ad5560.set_clamp(1.0, -0.1)

        '''
        assert isinstance(volt_pos, float) or isinstance(volt_pos, int)
        assert isinstance(volt_neg, float) or isinstance(volt_neg, int)
        dac_pos = (int(round(volt_pos * 1.0 * 65536 / (5.125 * self._reference))) + 0x8000) & 0xFFFF
        dac_neg = (int(round(volt_neg * 1.0 * 65536 / (5.125 * self._reference))) + 0x8000) & 0xFFFF
        self.write_register(AD5560Def.AD5560_REG_CLH_DAC_x1, dac_pos)
        self.write_register(AD5560Def.AD5560_REG_CLL_DAC_x1, dac_neg)
        dsp_reg1bits = self.read_register(AD5560Def.AD5560_REG_DPS_1)
        if ~(dsp_reg1bits & AD5560Def.AD5560_CLEN_ENABLE_MASK):
            dsp_reg1bits |= 1 << AD5560Def.AD5560_CLEN_ENABLE_OFFSET
        self.write_register(AD5560Def.AD5560_REG_DPS_1, dsp_reg1bits)

    def set_mode(self, mode):
        '''
        AD5560 set working mode.

        Args:
            mode:   instance(int), in list AD5560Def.MODE_Type.

        Examples:
            ad5560.set_mode(AD5560Def.AD5560_MODE_SLAVE_FI)

        '''
        assert mode in AD5560Def.MODE_Type
        dsp_reg2bits = self.read_register(AD5560Def.AD5560_REG_DPS_2)
        dsp_reg2bits &= ~AD5560Def.AD5560_MODE_MASK
        dsp_reg2bits |= mode
        dsp_reg2bits &= ~AD5560Def.AD5560_SR_MASK
        if mode == AD5560Def.AD5560_MODE_SLAVE_FI:
            dsp_reg2bits |= 7 << AD5560Def.AD5560_SR_OFFSET
        dsp_reg2bits &= ~AD5560Def.AD5560_INT10K_MASK
        dsp_reg2bits |= AD5560Def.AD5560_GUARD_HIGHZ_MASK
        self.write_register(AD5560Def.AD5560_REG_DPS_2, dsp_reg2bits)

    def set_comparator(self, cmp_type, current_range, cph, cpl):
        '''
        AD5560 set comparator.

        Args:
            cmp_type:   instance(int), in list AD5560Def.CMP_Type.
            current_range:  instance(int), in list AD5560Def.CURRENT_Range.
            cph:  instance(float), high voltage.
            cpl:  instance(float), low voltage.

        Examples:
            ad5560.set_comparator(AD5560Def.AD5560_CMP_TYPE_CURRENT, AD5560Def.AD5560_CURRENT_RANGE_25mA, 2.0, 0.8)

        '''
        assert cmp_type in AD5560Def.CMP_Type
        assert current_range in AD5560Def.CURRENT_Range
        assert isinstance(cph, float) or isinstance(cph, int)
        assert isinstance(cpl, float) or isinstance(cpl, int)
        # sys_regbits = self.read_register(AD5560Def.AD5560_REG_SYS_CTRL)
        # sys_regbits |= AD5560Def.AD5560_CPO_MASK
        # self.write_register(AD5560Def.AD5560_REG_SYS_CTRL, sys_regbits)
        dps_reg1bits = self.read_register(AD5560Def.AD5560_REG_DPS_1)
        dps_reg1bits &= ~AD5560Def.AD5560_CMP_TYPE_MASK
        dps_reg1bits |= cmp_type
        self.write_register(AD5560Def.AD5560_REG_DPS_1, dps_reg1bits)
        cph_dac = int(cph * 1.0 * 65536 / (5.125 * self._reference) + 0x8000) & 0xFFFF
        cpl_dac = int(cpl * 1.0 * 65536 / (5.125 * self._reference) + 0x8000) & 0xFFFF
        self.write_register(AD5560Def.CPH_Reg[current_range], cph_dac)
        self.write_register(AD5560Def.CPL_Reg[current_range], cpl_dac)

    def set_current_range(self, current_range):
        '''
        AD5560 set current range.

        Args:
            current_range:  instance(int), in list AD5560Def.CURRENT_Range.

        Examples:
            ad5560.set_current_range(AD5560Def.AD5560_CURRENT_RANGE_25mA)

        '''
        assert current_range in AD5560Def.CURRENT_Range
        dps_reg1bits = self.read_register(AD5560Def.AD5560_REG_DPS_1)
        if current_range != (dps_reg1bits & AD5560Def.AD5560_CURRENT_RANGE_MASK):
            self.enable_sw_inh(True)
            dps_reg1bits &= ~AD5560Def.AD5560_CURRENT_RANGE_MASK
            dps_reg1bits |= current_range
            self.write_register(AD5560Def.AD5560_REG_DPS_1, dps_reg1bits)

    def enable_pd(self, enable):
        '''
        AD5560 enable or disable power down.

        Args:
            enable:  instance(bool).

        Examples:
            ad5560.enable_pd(False)

        '''
        assert isinstance(enable, bool)
        sys_regbits = self.read_register(AD5560Def.AD5560_REG_SYS_CTRL)
        if enable:
            sys_regbits &= ~AD5560Def.AD5560_PD_MASK
        else:
            sys_regbits |= AD5560Def.AD5560_PD_MASK
        self.write_register(AD5560Def.AD5560_REG_SYS_CTRL, sys_regbits)

    def set_gain(self, gain):
        '''
        AD5560 set gain of measure out and MI.

        Args:
            gain:  instance(int), in list AD5560Def.GAIN_Type.

        Examples:
            ad5560.set_gain(AD5560Def.AD5560_GAIN_1)

        '''
        assert gain in AD5560Def.GAIN_Type
        sys_regbits = self.read_register(AD5560Def.AD5560_REG_SYS_CTRL)
        if gain != (sys_regbits & AD5560Def.AD5560_GAIN_MASK):
            sys_regbits &= ~AD5560Def.AD5560_GAIN_MASK
            sys_regbits |= gain
        self.write_register(AD5560Def.AD5560_REG_SYS_CTRL, sys_regbits)

    def set_manual_compensation(self, rz=AD5560Def.AD5560_Rz_500Ohm, rp=AD5560Def.AD5560_Rp_200Ohm,
                                gm=AD5560Def.AD5560_Gm_300, cf=AD5560Def.AD5560_Cf_1, cc=AD5560Def.AD5560_Cc_0101):
        '''
        AD5560 set manual compensation.

        Args:
            rz:  instance(int), in list AD5560Def.GAIN_Type.
            rp:
            gm:
            cf:
            cc:

        Examples:
            ad5560.set_manual_compensation(AD5560Def.AD5560_GAIN_1)

        '''
        assert isinstance(rz, int) and rz in AD5560Def.Rz_Type
        assert isinstance(rp, int) and rp in AD5560Def.Rp_Type
        assert isinstance(gm, int) and gm in AD5560Def.Gm_Type
        assert isinstance(cf, int) and cf in AD5560Def.Cf_Type
        assert isinstance(cc, int) and cc in AD5560Def.Cc_Type
        comp_reg2bit2 = 0x8000 | rz | rp | gm | cf | cc
        self.write_register(AD5560Def.AD5560_REG_COMP_2, comp_reg2bit2)

    def read_alarm(self, alarm, clear=False):
        '''
        AD5560 read and clear alarm.

        Args:
            alarm:  instance(int), in list AD5560Def.GAIN_Type.
            clear:  instance(bool).

        Examples:
            ad5560.read_alarm(AD5560Def.AD5560_GAIN_1)

        '''
        assert isinstance(alarm, int) and alarm in AD5560Def.Alarm_Type
        assert isinstance(clear, bool)
        reg = AD5560Def.AD5560_REG_ALARM_STATUS_CLR_ALARM if clear else AD5560Def.AD5560_REG_ALARM_STATUS
        status = self.read_register(reg)
        if status & alarm:
            return 1
        return 0
