import socket
from mix.driver.core.bus.i2c import I2C
import struct
import ctypes
from threading import Thread
import thread
from mix.addon.driver.module.calibration import Calibration
from mix.addon.driver.module.transition_board import *
from mix.addon.driver.module.dvm_board import *
from mix.addon.driver.module.calibration import *
from mix.addon.driver.module.psu2_board import *
from mix.addon.driver.module.psu1_board import *
from ..driver.module.base_board import BaseBoard
import json
from mix.lynx.launcher.xavier import Xavier

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
CARRIER_ID_SET = 0xEF
TEST_RESULT_GET = 136
CARRIER_ID_REQ = 0xF0


BOARD_TRANS_I2C_DATA_REPLY = 12
BOARD_RECV_I2C_DATA_REPLY = 13
BOARD_ID_REQ_REPLY = 20
BOARD_ID_SET_REPLY = 21
BOARD_FW_REQ_REPLY = 22
BOARD_HW_REQ_REPLY = 23
BOARD_TEMP_GET_REPLY = 41
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
TEST_RESULT_GET_REPLY = 136
CARRIER_ID_SET_REPLY = 0xEF
CARRIER_ID_REQ_REPLY = 0xF0


SYS_MODE_NORMAL = 1
SYS_MODE_CAL = 2
SYS_MODE_CAL_CHECK = 3


DVM_INPUT_VOLTAGE = {0: DVMBoardDef.PSU1_SENSE, 1: DVMBoardDef.PSU2_SENSE}


CURRENT_LOC = {
    0: {
        PSU1BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.PSU1_MV_1nA,
        PSU1BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.PSU1_MEASOUT,
        PSU1BoardDef.CURRENT_RANGE_100mA: DVMBoardDef.PSU1_HC_1,
    },
    1: {
        PSU2BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.PSU2_MEASOUT,
        PSU2BoardDef.CURRENT_RANGE_1A:    DVMBoardDef.PSU2_HC_2,
        PSU2BoardDef.CURRENT_RANGE_4A:    DVMBoardDef.PSU2_HC_2,
        PSU2BoardDef.CURRENT_RANGE_10A:   DVMBoardDef.PSU2_HC_2,
    }
}


GAIN_TYPE = {
    0: {
        PSU1BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.DVM_GAIN_51_P_2,
        PSU1BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU1BoardDef.CURRENT_RANGE_100mA: DVMBoardDef.DVM_GAIN_51_P_2,
    },
    1: {
        PSU2BoardDef.CURRENT_RANGE_5uA:   DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_25uA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_250uA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_2_5mA: DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_25mA:  DVMBoardDef.DVM_GAIN_0_P_8,
        PSU2BoardDef.CURRENT_RANGE_1A:    DVMBoardDef.DVM_GAIN_3_P_2,
        PSU2BoardDef.CURRENT_RANGE_4A:    DVMBoardDef.DVM_GAIN_3_P_2,
        PSU2BoardDef.CURRENT_RANGE_10A:   DVMBoardDef.DVM_GAIN_3_P_2,
    }
}


R_SENSE = {
    0: PSU1BoardDef.R_SENSE,
    1: PSU2BoardDef.R_SENSE
}


PSU_GAIN = {
    0: PSU1BoardDef.GAIN_TYPE,
    1: PSU2BoardDef.GAIN_TYPE
}


class I2CServer(Thread):

    def __init__(self, xobjects):
        super(I2CServer, self).__init__()
        self._psu = {0: xobjects['psu1'], 1: xobjects['psu2']}
        self._dvm = xobjects['dvm']
        self._led_fan = xobjects['led_fan']
        self._transition = xobjects['transition']
        self._cal_switch = {0: [TransitionBoardDef.SWITCH_CAL_PS1, TransitionBoardDef.SWITCH_CAL_PS1_I,
                                TransitionBoardDef.SWITCH_CAL_PS1_nA, TransitionBoardDef.SWITCH_CAL_PS1_uA],
                            1: [TransitionBoardDef.SWITCH_CAL_PS3, TransitionBoardDef.SWITCH_CAL_PS3_I,
                                TransitionBoardDef.SWITCH_CAL_PS3_uA, TransitionBoardDef.SWITCH_None]}
        self._i2c_bus = xobjects['i2c_dut']
        self._address = Xavier().get_ip()
        self._calibration = xobjects['calibration']
        self._carrier = xobjects['carrier']
        self._base = xobjects['base']
        self._sys_mode = SYS_MODE_NORMAL
        self._predefine = xobjects['predefine']
        self.start()

    def message(self, msg):
        out = [0xFB]
        length = msg[2] | (msg[3] << 8)
        if PC_TO_BOARD_FRAME_HEAD != msg[0] or \
                PC_TO_BOARD_FRAME_END != msg[length + 5]:
            out.extend([0, 0, 0])
        else:
            cmd = msg[1]
            if cmd == BOARD_TRANS_I2C_DATA:
                out.extend([BOARD_TRANS_I2C_DATA_REPLY, 1, 0])
                addr = 0x0B
                buff = msg[5:(5+length-1)]
                try:
                    self._i2c_bus.write(addr, buff)
                    out.append(1)
                except Exception as e:
                    out.append(2)

            elif cmd == BOARD_RECV_I2C_DATA:
                out.extend([BOARD_RECV_I2C_DATA_REPLY, msg[6], msg[7]])
                addr = 0x0B
                buff = msg[5:6]
                size = (msg[6] | (msg[7] << 8)) + 1
                try:
                    recv_buff = self._i2c_bus.write_and_read(addr, buff, size)
                    if len(recv_buff) == size:
                        out.extend(recv_buff[0:(size - 1)])
                except Exception as e:
                    out[2] = 0

            elif cmd == TEST_RESULT_GET:
                state = msg[4]
                if state == 1:
                    self._led_fan.set_led_color('green')
                    self._led_fan.set_fan_type('slow')
                if state == 2:
                    self._led_fan.set_led_color('red')
                    self._led_fan.set_fan_type('slow')
                out.extend([TEST_RESULT_GET_REPLY, 1, 0, 1])

            elif cmd == MEASURE_FV_SET:
                out.extend([MEASURE_FV_SET_REPLY, 1, 0, 1])
                psu = msg[4]
                ad5560ch = msg[5]
                raw = msg[6] | (msg[7] << 8) | (msg[8] << 16) | (msg[9] << 24)
                volt = hex2float(raw)
                raw = msg[10] | (msg[11] << 8) | (msg[12] << 16) | (msg[13] << 24)
                i_limit = hex2float(raw)
                current_range = msg[14]
                try:
                    if ad5560ch == 0:
                        self._transition.set_switch(self._cal_switch[psu][0], TransitionBoardDef.SWITCH_STATE_ON)
                        if self._sys_mode != SYS_MODE_CAL:
                            volt = self._calibration.cal_fv(psu, current_range, volt)
                    # cal FVMI, ONLY USED BY PSU1
                    elif ad5560ch == 1 and psu == 0:
                        if current_range == PSU1BoardDef.CURRENT_RANGE_5uA:
                            self._transition.set_switch(self._cal_switch[0][2], TransitionBoardDef.SWITCH_STATE_ON)
                        elif current_range == PSU1BoardDef.CURRENT_RANGE_25mA:
                            self._transition.set_switch(self._cal_switch[0][3], TransitionBoardDef.SWITCH_STATE_ON)
                        volt = self._calibration.cal_fv(0, current_range, volt)
                    else:
                        ex = 1/ 0
                    self._psu[psu].fv(volt, i_limit, current_range)
                except Exception as e:
                    print e.message
                    out[4] = 2

            elif cmd == MEASURE_FI_SET:
                out.extend([MEASURE_FI_SET_REPLY, 1, 0, 1])
                psu = msg[4]
                ad5560ch = msg[5]
                current = hex2float(msg[6] | (msg[7] << 8) | (msg[8] << 16) | (msg[9] << 24))
                v_limit = hex2float(msg[10] | (msg[11] << 8) | (msg[12] << 16) | (msg[13] << 24))
                current_range = msg[14]
                if current_range >= 1:
                    self._transition.set_switch(self._cal_switch[psu][1], TransitionBoardDef.SWITCH_STATE_ON)
                elif current_range == 0:
                    self._transition.set_switch(self._cal_switch[psu][2], TransitionBoardDef.SWITCH_STATE_ON)
                    # OFF PS2 cap
                cal_current = current
                if self._sys_mode == SYS_MODE_CAL_CHECK:
                    cal_current = self._calibration.cal_fi(psu, current_range, current)
                    # print 'raw current[', current, '] cal current[', cal_current, ']'
                self._psu[psu].fi(cal_current, v_limit, current_range)
                self._psu[psu].output(True)

            elif cmd == MEASURE_MV_GET:
                out.extend([MEASURE_MV_GET_REPLY, 4, 0])
                psu = msg[4]
                ad5560ch = msg[5]
                self._dvm.set_input(DVM_INPUT_VOLTAGE[psu])
                self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
                volt = self._dvm.measure_voltage(1000, 1.0)
                print 'MV:', volt
                if self._sys_mode == SYS_MODE_CAL_CHECK:
                    volt = self._calibration.cal_mv(psu, self._psu[psu].current_range, volt)
                print self._psu[psu].current_range
                raw = float2hex(volt)
                out.extend(raw)

            elif cmd == MEASURE_MI_GET:
                out.extend([MEASURE_MI_GET_REPLY, 4, 0])
                psu = msg[4]
                ad5560ch = msg[5]
                current_range = msg[6]
                self._dvm.set_input(CURRENT_LOC[psu][current_range])
                self._dvm.set_gain(GAIN_TYPE[psu][current_range])
                r_sense = R_SENSE[psu][current_range]
                psu_gain = PSU_GAIN[psu][current_range]
                avg_volt = self._dvm.measure_voltage(1000, 1.0)
                current = avg_volt / r_sense / psu_gain
                print 'current :', current
                if self._sys_mode == SYS_MODE_CAL_CHECK:
                    # if current_range == PSU1BoardDef.CURRENT_RANGE_5uA:
                    #     current *= 1000000
                    current = self._calibration.cal_mi(psu, self._psu[psu].current_range, current)
                    print 'current_range:', current_range
                    # if current_range == PSU1BoardDef.CURRENT_RANGE_5uA:
                    #     current /= 1000000
                raw = float2hex(current)
                out.extend(raw)

            elif cmd == RESET_PS:
                out.extend([RESET_PS_REPLY, 2, 0, 1])
                psu = msg[4]
                self._psu[psu].restore()

            elif cmd == BOARD_TEMP_GET:
                out.extend([BOARD_TEMP_GET_REPLY, 5, 0, 1])
                try:
                    tmp = self._base.read_temperature()
                    raw = float2hex(tmp)
                    out.extend(raw)
                except Exception as e:
                    out[4] = 2

            elif cmd == CTRL_SWITCH_SET:
                out.extend([CTRL_SWITCH_SET_REPLY, 1, 0, 1])
                try:
                    switch = msg[4]
                    state = msg[5]
                    self._transition.set_switch(switch, state)
                except Exception as e:
                    out[4] = 2

            elif cmd == CTRL_SWITCH_GET:
                out.extend([CTRL_SWITCH_GET_REPLY, 2, 0, 1])
                try:
                    switch = msg[4]
                    state = 1 if TransitionBoardDef.SWITCH_STATE_ON == self._transition.get_switch(switch) else 0
                    out.append(state)
                except Exception as e:
                    out[4] = 2

            elif cmd == BOARD_MODE_SET:
                out.extend([BOARD_MODE_SET_REPLY, 1, 0, 1])
                self._sys_mode = msg[4]
                self._transition.reset_all_switch()
                if self._sys_mode == SYS_MODE_NORMAL:
                    self._psu[0].restore()
                    self._psu[1].restore()

            elif cmd == BOARD_ID_REQ:
                out.extend([BOARD_ID_REQ_REPLY, 10, 0, 1])
                board_id = self._calibration.read_board_id(False)
                remain = 9 - len(board_id)
                if remain > 0:
                    for i in range(remain):
                        board_id.append(0)
                out.extend(board_id)

            elif cmd == BOARD_ID_SET:
                out.extend([BOARD_ID_SET_REPLY, 1, 0, 1])
                try:
                    if 0 != self._calibration.write_board_id(msg[4:4+6]):
                        out[4] = 2
                except Exception as e:
                    out[4] = 2

            elif cmd == BOARD_FW_VERSION_REQ:
                out.extend([BOARD_FW_REQ_REPLY, 5, 0, 1])
                string_fw = self._predefine.FW()
                list_fw = []
                for i in range(len(string_fw)):
                    list_fw.append(int(string_fw[i]))
                out.extend(list_fw)

            elif cmd == BOARD_HW_VERSION_REQ:
                out.extend([BOARD_HW_REQ_REPLY, 5, 0, 1])
                out.extend([1, 0, 0, 0])

            elif cmd == CAL_DATA_SET:
                out.extend([CAL_DATA_SET_REPLY, 1, 0, 1])
                try:
                    if 0 != self._calibration.write(msg[4:(4+length)]):
                        out[4] = 2
                except Exception as e:
                    out[4] = 2

            elif cmd == CAL_DATA_GET:
                out.extend([CAL_DATA_GET_REPLY, 1, 0, 2])
                try:
                    cal_data = self._calibration.read(msg[4:(4+length)])
                    out[2] = len(cal_data)+1
                    out[4] = 1
                    out.extend(cal_data)
                except Exception as e:
                    out[4] = 2

            elif cmd == CARRIER_ID_SET:
                out.extend([CARRIER_ID_SET_REPLY, 1, 0, 1])
                try:
                    self._carrier.write_carrier(msg[5:5+11])
                except Exception as e:
                    out[4] = 2

            elif cmd == CARRIER_ID_REQ:
                out.extend([CARRIER_ID_REQ_REPLY, 11+1, 0])
                try:
                    rd = self._carrier.read_carrier(False)
                    out.append(1)
                    out.extend(rd)
                except Exception as e:
                    out.append(2)

            else:
                out.extend([0, 0, 0])
        # add crc & tail here.
        out.extend([0, 0xFD])
        return out

    def func(self, client_sock):
        while True:
            msg = client_sock.recv(1024)
            if not msg:
                self._transition.reset_all_switch()
                self._psu[0].restore()
                self._psu[1].restore()
                break
            # str to byte list
            tmp = list(msg)
            msg = list(struct.unpack('%dB' % len(tmp), msg))
            ret = self.message(msg)
            # list data to str
            b = []
            for i in ret:
                b.append(chr(i))
            ret = ''.join(b)
            client_sock.sendall(ret)
        client_sock.close()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self._address, 8816))
        sock.listen(5)
        while True:
            client_sock, client_addr = sock.accept()
            print('GOT a connection:', client_addr)
            thread.start_new_thread(self.func, (client_sock,))
            # self.func(client_sock)



