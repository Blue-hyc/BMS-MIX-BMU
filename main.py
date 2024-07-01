import time
from mix.lynx.launcher.launcher import *
from mix.addon.driver.module.dvm_board import *
from mix.addon.driver.module.psu1_board import *
from mix.driver.core.bus.axi4_lite_bus import *
from mix.driver.hyc.common.ipcore.mix_ad5761_hyc import *
from mix.driver.hyc.common.ipcore.mix_ads8900_hyc import *
from mix.addon.driver.ic.pca9506 import *

from mix.addon.driver.module.calibration import *
import socket

MIX_AD5761_HYC_CH1 = 0x43C00000
MIX_ADS8900_HYC_CH1 = 0x43C10000
MIX_AD5761_HYC_CH2 = 0x43C60000
MIX_ADS8900_HYC_CH2 = 0x43C50000
MIX_GPIO_HYC_0 = 0x43C40000
MIX_I2C_HYC_EXP = 0x43C20000
axi_i2c_0 = 0x41600000

PC_TO_BOARD_FRAME_HEAD = 0xFA
BOARD_TO_PC_FRAME_HEAD = 0xFB
PC_TO_BOARD_FRAME_END = 0xFE
BOARD_TO_PC_FRAME_END = 0xFD

BOARD_TRANS_I2C_DATA = 23
BOARD_RECV_I2C_DATA = 24
BOARD_ID_REQ = 30
BOARD_ID_SET = 31
BOARD_FW_VERSION_REQ = 32
BOARD_HW_VERSION_REQ = 33
BOARD_TEMP_GET = 51
BMU_TEMP_GET = 62
RESET_ALL = 74
RESET_PS = 75
MEASURE_FV_SET = 90
MEASURE_FI_SET = 91
MEASURE_MV_GET = 92
MEASURE_MI_GET = 93
CTRL_SWITCH_SET = 94
CTRL_SWITCH_GET = 95
BOARD_MODE_SET = 100
BOARD_MODE_GET = 101
CAL_DATA_SET = 104
CAL_DATA_GET = 105
PLC_STATE_GET = 134
ACIR_GET = 145
CARRIER_ID_SET = 0xEF
CARRIER_ID_REQ = 0xF0

MESSAGE_CMD = (
    BOARD_TRANS_I2C_DATA,
    BOARD_RECV_I2C_DATA,
    MEASURE_FV_SET,
    MEASURE_FI_SET,
    MEASURE_MV_GET,
    MEASURE_MI_GET,
    BOARD_MODE_SET,
    BOARD_MODE_GET,
    CAL_DATA_SET,
    CAL_DATA_GET
)

BOARD_TRANS_I2C_DATA_REPLY = 12
BOARD_RECV_I2C_DATA_REPLY = 13
BOARD_ID_REQ_REPLY = 20
BOARD_ID_SET_REPLY = 21
BOARD_FW_REQ_REPLY = 22
BOARD_HW_REQ_REPLY = 23
BOARD_TEMP_GET_REPLY = 41
BMU_TEMP_GET_REPLY = 52
RESET_ALL_REPLY = 64
RESET_PS_REPLY = 65
MEASURE_FV_SET_REPLY = 90
MEASURE_FI_SET_REPLY = 91
MEASURE_MV_GET_REPLY = 92
MEASURE_MI_GET_REPLY = 93
CTRL_SWITCH_SET_REPLY = 94
CTRL_SWITCH_GET_REPLY = 95
BOARD_MODE_SET_REPLY = 100
BOARD_MODE_GET_REPLY = 101
CAL_DATA_SET_REPLY = 104
CAL_DATA_GET_REPLY = 105
PLC_STATE_GET_REPLY = 134
ACIR_GET_REPLY = 145
CARRIER_ID_SET_REPLY = 0xEF
CARRIER_ID_REQ_REPLY = 0xF0

MESSAGE_CMD_REPLY = (
    BOARD_TRANS_I2C_DATA_REPLY,
    BOARD_RECV_I2C_DATA_REPLY,
    MEASURE_FV_SET_REPLY,
    MEASURE_FI_SET_REPLY,
    MEASURE_MV_GET_REPLY,
    MEASURE_MI_GET_REPLY,
    BOARD_MODE_SET_REPLY,
    BOARD_MODE_GET_REPLY,
    CAL_DATA_SET_REPLY,
    CAL_DATA_GET_REPLY,
)

SYS_MODE_NORMAL = 1
SYS_MODE_CAL = 2
SYS_MODE_CAL_CHECK = 3



class MrsM(object):
    def __init__(self):
        # pass
        io_gpio = GPIO(MIX_GPIO_HYC_0)
        self._io_gpio = io_gpio
        exp_reset = Pin(io_gpio, 0)
        exp_reset.set_level(1)
        io_exp = PCA9506(0x20, IIC(MIX_I2C_HYC_EXP))
        psu_0 = PSU1Board(None, Pin(io_exp, 27, 'output'), None, Pin(io_gpio, 3), Pin(io_exp, 4, 'output'),
                          Pin(io_exp, 3, 'output'), MIXAD5761HYC(MIX_AD5761_HYC_CH1))
        # psu_1 = PSU1Board(None, Pin(io_exp, 28, 'output'), None, Pin(io_gpio, 4), Pin(io_exp, 6, 'output'),
        #                   Pin(io_exp, 5, 'output'), MIXAD5761HYC(MIX_AD5761_HYC_CH2))
        dmm_0 = DVMBoard(None, io_exp, Pin(io_gpio, 1), MIXADS8900HYC(MIX_ADS8900_HYC_CH1))
        dmm_1 = DVMBoard(None, io_exp, Pin(io_gpio, 2), MIXADS8900HYC(MIX_ADS8900_HYC_CH2))
        self._psu = {0: psu_0}
        try:
            self._psu[0].analog_current(0.05)
        except Exception as e:
            print 'psu_0 analog current fail.'
        try:
            self._psu[1].analog_current(0.05)
        except Exception as e:
            print 'psu_1 analog current fail.'
        self._dvm = {0: dmm_0, 1: dmm_1}

    def message(self, msg):
        print time.ctime(), 'recv from client:', msg
        out = [0xFB]
        length = msg[2] | (msg[3] << 8)
        if PC_TO_BOARD_FRAME_HEAD != msg[0] or \
                PC_TO_BOARD_FRAME_END != msg[length + 5]:
            out.extend([0, 0, 0])
        else:
            cmd = msg[1]
            if cmd == BOARD_TRANS_I2C_DATA:
                pass

            elif cmd == BOARD_RECV_I2C_DATA:
                pass

            elif cmd == MEASURE_FV_SET:
                pass

            elif cmd == MEASURE_FI_SET:
                pass

            elif cmd == MEASURE_MV_GET:
                channel = msg[4]
                out.extend([MEASURE_MV_GET_REPLY, 5, 0])
                try:
                    self._dvm[channel].set_input(channel, DVMBoardDef.PSU1_HC_1)
                    self._dvm[channel].set_gain(DVMBoardDef.DVM_GAIN_6_P_4)
                    real, imag = self._dvm[channel].read_fft(500000, 1024 * 2, 3)
                    current = math.sqrt(pow(real / 1.0, 2) + pow(imag / 1.0, 2))
                    if 0.045 < current < 0.055:
                        self._dvm[channel].set_input(channel, DVMBoardDef.MV_S)
                        self._dvm[channel].set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
                        dc = self._dvm[channel].measure_voltage(500000, 0.001) - 0.0012
                        print 'dc: [', dc, ']'
                        out.append(1)
                        out.extend(float2hex(dc))
                    else:
                        out.append(2)
                except Exception as e:
                    out.append(2)

            elif cmd == MEASURE_MI_GET:
                pass

            elif cmd == RESET_PS:
                pass

            elif cmd == BOARD_TEMP_GET:
                pass

            elif cmd == CTRL_SWITCH_SET:
                pass

            elif cmd == CTRL_SWITCH_GET:
                pass

            elif cmd == BOARD_MODE_SET:
                pass

            elif cmd == BOARD_ID_REQ:
                out.extend([BOARD_ID_REQ_REPLY, 10, 0])
                id_str = 'V000001'
                try:
                    id_list = []
                    for character in id_str:
                        id_list.append(ord(character))
                except Exception as e:
                    out.append(2)
                else:
                    out.append(1)
                    out.extend(id_list)
                    remain = 9 - len(id_list)
                    for i in range(remain):
                        out.append(0)

            elif cmd == BOARD_ID_SET:
                pass

            elif cmd == BOARD_FW_VERSION_REQ:
                out.extend([BOARD_FW_REQ_REPLY, 5, 0, 1])
                out.extend([9, 0, 0, 1])

            elif cmd == BOARD_HW_VERSION_REQ:
                out.extend([BOARD_HW_REQ_REPLY, 5, 0, 1])
                out.extend([1, 0, 0, 0])

            elif cmd == CAL_DATA_SET:
                pass

            elif cmd == CAL_DATA_GET:
                pass

            elif cmd == CARRIER_ID_SET:
                pass

            elif cmd == CARRIER_ID_REQ:
                channel = msg[4]
                out.extend([CARRIER_ID_REQ_REPLY, 12, 0])
                carrier_str = ['HYCCARRIER1', 'HYCCARRIER2']
                try:
                    carrier_id = []
                    for character in carrier_str[channel]:
                        carrier_id.append(ord(character))
                except Exception as e:
                    out.append(2)
                else:
                    out.append(1)
                    out.extend(carrier_id)

            elif cmd == ACIR_GET:
                out.extend([ACIR_GET_REPLY, 5, 0])
                channel = msg[4]
                voltages = 0.0
                currents = 0.0
                try:
                    if channel == 0:
                        self._dvm[0].set_input(0, DVMBoardDef.MV_S)
                        self._dvm[0].set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
                        self._dvm[1].set_input(1, DVMBoardDef.PSU1_HC_1)
                        self._dvm[1].set_gain(DVMBoardDef.DVM_GAIN_6_P_4)
                        for i in range(20):
                            real, imag = self._dvm[0].read_fft(500000, 1024 * 2, 3)
                            voltage = math.sqrt(pow(real / 1.0, 2) + pow(imag / 1.0, 2))
                            voltages += voltage
                            real, imag = self._dvm[1].read_fft(500000, 1024 * 2, 3)
                            current = math.sqrt(pow(real / 1.0, 2) + pow(imag / 1.0, 2))
                            currents += current
                    else:
                        self._dvm[1].set_input(1, DVMBoardDef.MV_S)
                        self._dvm[1].set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
                        self._dvm[0].set_input(0, DVMBoardDef.PSU1_HC_1)
                        self._dvm[0].set_gain(DVMBoardDef.DVM_GAIN_6_P_4)
                        for i in range(20):
                            real, imag = self._dvm[1].read_fft(500000, 1024 * 2, 3)
                            voltage = math.sqrt(pow(real / 1.0, 2) + pow(imag / 1.0, 2))
                            voltages += voltage
                            real, imag = self._dvm[0].read_fft(500000, 1024 * 2, 3)
                            current = math.sqrt(pow(real / 1.0, 2) + pow(imag / 1.0, 2))
                            currents += current
                except Exception as e:
                    out.append(2)
                else:
                    out.append(1)
                    out.extend(float2hex(((voltages / 10) / (currents / 10) * 1000) - 1.9))

            elif cmd == PLC_STATE_GET:
                out.extend([PLC_STATE_GET_REPLY, 2, 0])
                rd = self._io_gpio.get_plc()
                out.extend([rd>>2, rd&0x03])

            elif cmd == BMU_TEMP_GET:
                channel = msg[4]
                out.extend([BMU_TEMP_GET_REPLY, 5, 0])
                try:
                    temp = 25.8
                except Exception as e:
                    out.append(2)
                else:
                    out.append(1)
                    out.extend(float2hex(temp))

            else:
                out.extend([0, 0, 0])
        # add crc & tail here.
        out.extend([0, 0xFD])
        print time.ctime(), 'send to client:', out
        return out


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((Xavier().get_ip(), 8816))
    sock.listen(3)
    sock.setblocking(False)
    sock.settimeout(0.0)
    conn_list = []
    mrs = MrsM()
    while True:
        try:
            client_sock, client_addr = sock.accept()
        except Exception as e:
            pass
        else:
            client_sock.setblocking(False)
            conn_list.append(client_sock)
        for conn in conn_list:
            try:
                msg = conn.recv(1024)
            except Exception as e:
                pass
            else:
                if not msg:
                    conn.close()
                    conn_list.remove(conn)
                    continue
                # str to byte list
                tmp = list(msg)
                msg = list(struct.unpack('%dB' % len(tmp), msg))
                ret = mrs.message(msg)
                # list data to str
                b = []
                for i in ret:
                    b.append(chr(i))
                ret = ''.join(b)
                conn.sendall(ret)


    #FV
    # psu_0.fv(1.2, 0.01, PSU1BoardDef.CURRENT_RANGE_25mA)
    #FI
    # psu_0.fi(-0.05, -1.0, PSU1BoardDef.CURRENT_RANGE_100mA)
    # psu_0.output(True)
    #ANOLOG CURRENT
    # psu_0.analog_current(0.05)

    # dmm_0 = DVMBoard(None, io_exp, spi_s0_dmm1, mix_ads8900_hyc_0)
    # dmm_0.set_input(0, DVMBoardDef.MV_S)
    # dmm_0.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
    #
    # dc = dmm_0.measure_voltage(500000, 0.001)
    # print 'dc: [', dc-0.0012, ']'

    # dmm_0.set_input(0, DVMBoardDef.PSU1_HC_1)
    # dmm_0.set_gain(DVMBoardDef.DVM_GAIN_6_P_4)




    # rd = dmm_0.measure_voltage(10, 1.0, True)
    # print rd/1

    # dmm_1 = DVMBoard(None, io_exp, spi_s0_dmm2, mix_ads8900_hyc_1)
    # dmm_1.set_input(1, DVMBoardDef.PSU1_HC_1)
    # dmm_1.set_gain(DVMBoardDef.DVM_GAIN_6_P_4)

    # voltages= 0.0
    # currents=0.0
    # for i in range(20):
    #     real, imag = dmm_0.read_fft(500000, 1024 * 2, 3)
    #
    #     voltage = math.sqrt(pow(real / 0.8 / 1.0, 2) + pow(imag / 0.8 / 1.0, 2))
    #     voltages += voltage
    #     print 'voltage: [', voltage, ']'
    #
    #     real, imag = dmm_1.read_fft(500000, 1024*2, 3)
    #
    #     current = math.sqrt(pow(real/6.4/1.0, 2) + pow(imag/6.4/1.0, 2))
    #     currents += current
    #     print 'current: [', current, ']'
    #
    # print 'acir: [', ((voltages/10) / (currents/10) * 1000) - 1.9, ']'


