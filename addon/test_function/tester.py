import time
import json
import logging
import csv
import codecs
from ..driver.module.dvm_board import *
from ..driver.module.psu1_board import *
from ..driver.module.psu2_board import *
from mix.addon.driver.module.transition_board import TransitionBoardDef
from mix.lynx.launcher.xavier import Xavier

DEFAULT_CONFIG_PROFILE_DIR = '/mix/addon/config/HYC_BMS.json'

I2C_PULL_UP_1_2 = 1.2
I2C_PULL_UP_1_8 = 1.8

I2C_PULL_UP = TransitionBoardDef.PULL_UP_VOLTAGE_CONFIG


def cal_pec(data, seed):
    pec = seed
    for i in range(len(data)):
        pec ^= data[i]
        for j in range(8):
            if pec & 0x80 == 0x80:
                pec = ((pec << 1) ^ 0x07) & 0xFF
            else:
                pec <<= 1
    return pec


def package(cmd, raw):
    out = [cmd]
    length = len(raw)
    if length > 255:
        out.append(length & 0xFF)
        out.append((length & 0xFF00) >> 8)
    else:
        out.append(length)
    out.extend(raw)
    pec = cal_pec(out, 0x62)
    out.append(pec)
    # return out[1:len(out)]
    return out


class Tester(object):
    rpc_public_api = ['carrierID', 'testerID', 'HW', 'FW', 'temp', 'reset', 'I2C', 'matingcheck', 'ptc23_check']

    def __init__(self, xobjects):
        self._psu1 = xobjects['psu1']
        self._psu2 = xobjects['psu2']
        self._dvm = xobjects['dvm']
        self._led_fan = xobjects['led_fan']
        self._transition = xobjects['transition']
        self._calibration = xobjects['calibration']
        self._carrier = xobjects['carrier']
        self._init_temperature = 0.0
        self._predefine = xobjects['predefine']
        self._i2c_bus = xobjects['i2c_dut']
        self.today = ''
        self.count = 0
        self._address = Xavier().get_ip()
        self.i = 0
        board_id = self._calibration.read_board_id()
        self.board_id = board_id
        try:
            file_dir = '/mix/MIX_config.csv'
            csv = open(file_dir, 'r')
            # for i in range(3):
            t = csv.readline().split(',')
            t = csv.readline().split(',')
            self.ptc23_offset = t[0:2]
            print 'self.ptc23_offset', csv, self.ptc23_offset[0], self.ptc23_offset[1]
            t = csv.readline().split(',')
            self.carrier_id = t[0]
            csv.close()
        except Exception as e:
            print 'Fail to read MIX_config.csv'
        logging.basicConfig(filename='//mix//matingcheck.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def carrierID(self):
        carrier_id = 'HYCCARRIER1'
        try:
            # carrier_id = self._carrier.read_carrier()
            id_list = []
            rd = [72, 73, 74]
            # carrier_id = self._calibration.read_board_id()
            for i in range(len(rd)):
                id_list.extend(chr(rd[i]))
            carrier_id = ''.join(id_list)
            print 'carrier:', rd, id_list, carrier_id
            return [0, carrier_id]
        except Exception as e:
            return [-1]

    def testerID(self):
        try:
            board_id = self._calibration.read_board_id()
            self.board_id = board_id
            return [0, board_id]
        except Exception as e:
            return [-1]

    def create_csv(self):
        date = time.strftime("%Y%m%d", time.localtime(time.time()))
        if date != self.today or self.count == 0:
            self.count += 1
            self.today = date
            self.file_dir = '//root//' + self.today + '-' + self.board_id + '.csv'
            with open(self.file_dir, 'a') as log_file:
                writer = csv.writer(log_file)
                header = ['date', 'time', 'testerID', 'test result', 'IP', 'Cn2Pn_v', 'ptc1_v', '<ptc1_res>', 'SN',
                          'neg_v', 'neg_i', 'neg_impedance', 'pos_v', 'pos_i', 'pos_impedance', '<impedance>',
                          'sda_v', 'scl_v', 'sda_v_load', 'sda_i', 'scl_v_load', 'scl_i', '<sda_res>', '<scl_res>']
                writer.writerow(header)

    def matingcheck(self):
        self._transition.ptc2_raw = []
        self._transition.ptc3_raw = []
        self._transition.ptc2_flag = 'normal'
        self._transition.ptc3_flag = 'normal'

        try:
            self.reset()
            self._psu1.fv(3.8, 0.1, 5)
            self._dvm.set_input_fast(0)
            self._dvm.set_gain_fast(3)
            vol = self._dvm.measure_voltage(1000, 0.05)
            if 3.6 < vol < 4.0:
                self._psu1.post_power_on_init()
            self._psu1.restore()

            self._psu2.fv(1, 0.1, 5)
            self._dvm.set_input_fast(4)
            self._dvm.set_gain_fast(3)
            vol = self._dvm.measure_voltage(1000, 0.05)
            if 0.8 < vol < 1.2:
                self._psu2.post_power_on_init()
            self._psu2.restore()
        except Exception as e:
            pass

        self.create_csv()
        self.new_row = []
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        second = time.strftime("%H:%M:%S", time.localtime(time.time()))
        self.new_row.append(date)
        self.new_row.append(second)
        self.new_row.append(self.board_id)
        self.new_row.append('pass')
        self.new_row.append(self._address)
        # Check bmu exists
        self._transition.set_switch(TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG, 1)
        self._psu2.fi(0.001, 1, 4)
        self._psu2.output(True)
        self._dvm.set_input_fast(DVMBoardDef.PSU2_SENSE)
        self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
        vol = self._dvm.measure_voltage(2000, 0.05)
        self._transition.set_switch(TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG, 0)
        self._psu2.restore()
        self.new_row.append(vol)
        if vol > 0.8:
            print 'no bmu', vol
            self.new_row[3] = 'No BMU'
            logging.error('No bmu was detected')
            return [-1]

        # PTC1 test
        self._transition.set_switch(TransitionBoardDef.SWITCH_PTC1, 1)
        self._psu2.fi(0.001, 1, 4)
        self._psu2.output(True)
        vol = self._dvm.measure_voltage(2000, 0.05)
        self._transition.set_switch(TransitionBoardDef.SWITCH_PTC1, 0)
        self._psu2.restore()
        self.new_row.append(vol)
        ptc1_res = vol / 0.001
        self.new_row.append(ptc1_res)

        if vol > 0.5:
            print 'ptc1 ng', vol
            self.new_row[3] = 'PTC1'
            logging.error('PTC1 test FAIL')
            logging.error('PS3_clamp_voltage[' + str(vol) + ']')
            return [-1]

        # Wake up BMU
        self._transition.set_switch(TransitionBoardDef.SWITCH_PS1_CELL_POS_CELL_NEG, 1)
        self._psu1.fv(3.8, 0.1, PSU1BoardDef.CURRENT_RANGE_100mA)
        time.sleep(0.1)
        self._transition.set_switch(TransitionBoardDef.SWITCH_CELL_POS_TP3_SHORT, 1)
        time.sleep(1.1)
        self._transition.set_switch(TransitionBoardDef.SWITCH_CELL_POS_TP3_SHORT, 0)
        time.sleep(1)

        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # self.new_row.append('NA')
        # bmu_type = 1
        # read bmu from 0x90
        # addr = 0x0B
        # buff = [0x90]
        # size = 18 + 2 + 1
        # try:
        #     recv_buff = self._i2c_bus.write_and_read(addr, buff, size)
        #     print recv_buff
        #     if len(recv_buff) == size:
        #         final = recv_buff[0:(size - 1)]
        #         if final[1] == 0xFF and final[5] == 0xFF and final[9] == 0xFF:
        #             bmu_type = 1
        #             self.new_row.append('flow1')
        #         else:
        #             # flow4
        #             result = []
        #             for buff in recv_buff:
        #                 result.append(chr(buff))
        #             sn = ''.join(result[1:18])
        #             print sn
        #             self.new_row.append(sn)
        #             bmu_type = 0
        # except Exception as e:
        #     print 'read SN fail'
        #     self.new_row[3] = 'Read SN Fail'
        #     logging.error('read SN FAIL')
        #     self.reset()
        #     return [-1]

        init_gg = [0x40000024, 0x1ACCE551,
                   0x400C0028, 0x1ACCE551,
                   0x4009002C, 0x1ACCE551,
                   0x400C0004, 0x00000001,
                   0x40090000, 0x00000000,
                   0x40090004, 0xFFFFFFFF,
                   0x40090008, 0x0000FF00,
                   0x40090014, 0x00000F01,
                   0x40090018, 0x00000005,
                   0x40080010, 0x00000001,
                   0x40080014, 0x00000002,
                   0x40000008, 0xABCD0007,
                   0x40080000, 0x00000007,
                   0x4008048C, 0x000300B8,
                   0x40080490, 0x00001044,
                   0x40080494, 0x20444411,
                   0x40080498, 0x10A00000,
                   0x4008049C, 0x30A0000A,
                   0x40080474, 0x00000144,
                   0x40080478, 0x000F1100,
                   0x40080470, 0x00030800,
                   0x4008000C, 0x000449B4,
                   0x40000014, 0xABCD0000,
                   0x40020000, 0x00000000,
                   0xE000ED10, 0x00000004,
                   0x40000030, 0xAB1FF935,
                   0x40080008, 0x00004000
                   ]

        # addr = [0x18, 0x00, 0x09, 0x40]
        # open_fet = [0x05, 0x00, 0x00, 0x00]
        # shut_fet = [0x00, 0x00, 0x00, 0x00]

        # if bmu_type == 1:
        #     # init gg
        #     try:
        #         for i in range(len(init_gg)):
        #             data = []
        #             for j in range(4):
        #                 data.append((init_gg[i] >> (j * 8)) & 0xff)
        #
        #             if i % 2 != 0:
        #                 buff = package(0xC1, data)
        #                 self._i2c_bus.write(0x0B, buff)
        #             else:
        #                 buff = package(0xC0, data)
        #                 self._i2c_bus.write(0x0B, buff)
        #     except Exception as e:
        #         pass
        #
        #     # open fet
        #     try:
        #         buff = package(0xC0, addr)
        #         self._i2c_bus.write(0x0B, buff)
        #         buff = package(0xC1, open_fet)
        #         self._i2c_bus.write(0x0B, buff)
        #     except Exception as e:
        #         pass

        # try:
        #     neg_resistance test
        #     self._transition.set_switch(TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG, 1)
        #     self._psu2.fi(0.5, 0.5, PSU2BoardDef.CURRENT_RANGE_1A)
        #     self._psu2.output(True)
        #     self._dvm.set_input_fast(DVMBoardDef.PSU2_HC_1)
        #     self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
        #     volt = self._dvm.measure_voltage(1000, 0.1)
        #     self._dvm.set_input_fast(DVMBoardDef.PSU2_SENSE)
        #     self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
        #     r_sense = PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_1A]
        #     psu_gain = PSU2BoardDef.GAIN_TYPE[PSU2BoardDef.CURRENT_RANGE_1A]
        #     voltage_neg = self._dvm.measure_voltage(1000, 0.1)
        #     current_neg = volt / r_sense / psu_gain
        #     res_neg = voltage_neg / current_neg
        #     self.new_row.append(voltage_neg)
        #     self.new_row.append(current_neg)
        #     self.new_row.append(res_neg)
        #     print 'neg_volt[', voltage_neg, '] neg_current[', current_neg, ']'
        #     print 'res_neg[', res_neg, ']'
        #     self._transition.set_switch(TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG, 0)
        #     self._psu2.restore()

        self.new_row.append('NA')
        self.new_row.append('NA')
        self.new_row.append('NA')
        self.new_row.append('NA')
        self.new_row.append('NA')
        self.new_row.append('NA')
        self.new_row.append('NA')
        self.new_row.append('NA')
        #     #discharge cap
        #     self._transition.set_pin(0, 12, 1)
        #     time.sleep(0.1)
        #     self._transition.set_pin(0, 12, 0)
        #     time.sleep(0.05)
        #     print 'discharge cap'
        #     # pos_resistance test
        #     self._transition.set_switch(TransitionBoardDef.SWITCH_PS3_CELL_POS_PACK_POS, 1)
        #     # self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_POS_TP3_SHORT, 1)
        #     self._psu2.fi(0.5, 0.5, PSU2BoardDef.CURRENT_RANGE_1A)
        #     self._psu2.output(True)
        #     self._dvm.set_input_fast(DVMBoardDef.PSU2_HC_1)
        #     self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
        #     volt = self._dvm.measure_voltage(1000, 0.1)
        #     self._dvm.set_input_fast(DVMBoardDef.PSU2_SENSE)
        #     self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
        #     r_sense = PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_1A]
        #     psu_gain = PSU2BoardDef.GAIN_TYPE[PSU2BoardDef.CURRENT_RANGE_1A]
        #     voltage_pos = self._dvm.measure_voltage(1000, 0.1)
        #     current_pos = volt / r_sense / psu_gain
        #     res_pos = voltage_pos / current_pos
        #     self.new_row.append(voltage_pos)
        #     self.new_row.append(current_pos)
        #     self.new_row.append(res_pos)
        #     print 'pos_volt[', voltage_pos, '] pos_current[', current_pos, ']'
        #     print 'res_pos[', res_pos, ']'
        #     total = res_pos
        #     self.new_row.append(total * 1000)
        #     self._transition.set_switch(TransitionBoardDef.SWITCH_PS3_CELL_POS_PACK_POS, 0)
        #     self._transition.set_pin(1, 5, 0)
        #     self._transition.set_pin(1, 8, 0)
        #     self._psu2.restore()

        #     try:
        #         if bmu_type == 1:
        #             # close fet
        #             print 'fresh bmu need close fet'
        #             buff = package(0xC0, addr)
        #             self._i2c_bus.write(0x0B, buff)
        #             buff = package(0xC1, shut_fet)
        #             self._i2c_bus.write(0x0B, buff)
        #             print 'res total [', res_pos, ']'
        #     except Exception as e:
        #         pass
        #     if total > 0.048 or total < 0.036:
        #         self.new_row[3] = 'Impedance Fail'
        #         # logging.error('Impedance test FAIL, pos_res[' + str(res_pos) + '], neg_res[' + str(res_neg) + ']')
        #         # logging.error('pos_voltage[' + str(voltage_pos) + '], pos_current[' + str(current_pos))
        #         # logging.error('neg_voltage[' + str(voltage_neg) + '], neg_current[' + str(current_neg))
        #         self.reset()
        #         return [-1]
        # except Exception as e:
        #     return [-1]

        try:
            # ptc2&3
            self._psu1.fv(3.8, 0.022, PSU1BoardDef.CURRENT_RANGE_25mA)
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SDA, 1)
            self._dvm.set_input_fast(DVMBoardDef.I2C_SDA)
            self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
            sda_volt = self._dvm.measure_voltage(2000, 0.05)
            sda_volt = self._calibration.cal_mv(0, PSU1BoardDef.CURRENT_RANGE_100mA, sda_volt)
            self.new_row.append(sda_volt)
            print 'ptc2&3 check', 'sda volt', sda_volt
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SDA, 0)
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SCL, 1)
            self._dvm.set_input_fast(DVMBoardDef.I2C_SCL)
            self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
            scl_volt = self._dvm.measure_voltage(2000, 0.05)
            scl_volt = self._calibration.cal_mv(0, PSU1BoardDef.CURRENT_RANGE_100mA, scl_volt)
            self.new_row.append(scl_volt)
            print 'ptc2&3 check', 'scl_volt', scl_volt
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SCL, 0)

            # time.sleep(0.01)
            self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SDA, 1)
            cal_current = self._calibration.cal_fi(1, 3, 0.00025)
            self._psu2.fi(cal_current, 0.5, PSU2BoardDef.CURRENT_RANGE_2_5mA)
            self._psu2.output(True)
            time.sleep(0.2)
            self._dvm.set_input_fast(DVMBoardDef.PSU2_SENSE)
            self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
            sda_volt_load = self._dvm.measure_voltage(1000, 0.15)
            sda_volt_load = fabs(self._calibration.cal_mv(0, PSU1BoardDef.CURRENT_RANGE_100mA, sda_volt_load))
            self.new_row.append(sda_volt_load)
            print 'ptc2&3 check', 'sda_volt_load', sda_volt_load
            self._dvm.set_input_fast(DVMBoardDef.PSU2_MEASOUT)
            self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
            sda_i = self._dvm.measure_voltage(1000, 0.1) / 200.0 / 10.0
            sda_i = self._calibration.cal_mi(1, PSU2BoardDef.CURRENT_RANGE_2_5mA, sda_i)
            print 'ptc2&3 check', 'sda_i', sda_i
            self.new_row.append(sda_i)
            self._psu2.output(False)
            self._psu2.restore()
            self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SDA, 0)

            self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SCL, 1)
            self._psu2.fi(cal_current, 0.5, PSU2BoardDef.CURRENT_RANGE_2_5mA)
            self._psu2.output(True)
            time.sleep(0.2)
            self._dvm.set_input_fast(DVMBoardDef.PSU2_SENSE)
            self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
            scl_volt_load = self._dvm.measure_voltage(1000, 0.15)
            print 'ptc2&3 check', 'scl_volt_load', scl_volt_load
            scl_volt_load = fabs(self._calibration.cal_mv(0, PSU1BoardDef.CURRENT_RANGE_100mA, scl_volt_load))
            self.new_row.append(scl_volt_load)
            print 'ptc2&3 check', 'scl_volt_load', scl_volt_load
            self._dvm.set_input_fast(DVMBoardDef.PSU2_MEASOUT)
            self._dvm.set_gain_fast(DVMBoardDef.DVM_GAIN_0_P_8)
            scl_i = self._dvm.measure_voltage(1000, 0.1) / 200.0 / 10.0
            scl_i = self._calibration.cal_mi(1, PSU2BoardDef.CURRENT_RANGE_2_5mA, scl_i)
            print 'ptc2&3 check', 'scl_i', scl_i
            self.new_row.append(scl_i)

            # self._psu2.output(False)
            # self._psu2.restore()
            # self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SCL, 0)

            ptc2 = ((sda_volt - sda_volt_load) / sda_i) + float(self.ptc23_offset[0])
            ptc3 = ((scl_volt - scl_volt_load) / scl_i) + float(self.ptc23_offset[1])
            self.new_row.append(ptc2)
            self.new_row.append(ptc3)
            print ptc2, ptc3
            print 'int(self.ptc23_offset)', float(self.ptc23_offset[0])
            print 'int(self.ptc23_offset)', float(self.ptc23_offset[1])
            ptc2_usl = 1736.0 - 1.5
            ptc2_lsl = 1594.0 + 1.5
            ptc3_usl = 2342.0 - 1.5
            ptc3_lsl = 2188.0 + 1.5
            print 'ptc2 usl lsl', ptc2_usl, ptc2_lsl
            if ptc2 < ptc2_lsl or ptc2 > ptc2_usl:
                self.new_row[3] = 'PTC2 Fail'
                if ptc2_usl < ptc2 < ptc2_usl + 20:
                    sda_volt_load = sda_volt - ((ptc2 - 22) * sda_i)
                    self._transition.ptc2_raw = [sda_volt, sda_volt_load, sda_i]
                    self._transition.ptc2_flag = 'ptc2 fail'
                    self.new_row[3] = 'PTC2 Fail, but return pass'
                else:
                    self._transition.ptc2_raw = []
                    self._transition.ptc2_flag = 'normal'
                    return [-1]
            elif ptc3 < ptc3_lsl or ptc3 > ptc3_usl:
                self.new_row[3] = 'PTC3 Fail'
                if ptc3_usl < ptc3 < ptc3_usl + 20:
                    scl_volt_load = scl_volt - ((ptc3 - 22) * scl_i)
                    self._transition.ptc3_raw = [scl_volt, scl_volt_load, scl_i]
                    self._transition.ptc3_flag = 'ptc3 fail'
                    self.new_row[3] = 'PTC3 Fail, but return pass'
                else:
                    self._transition.ptc3_raw = []
                    self._transition.ptc3_flag = 'normal'
                    return [-1]
            return [0]
        except Exception as e:
            return [-1]
        finally:
            self.reset()

    def HW(self):
        return [0, '1000']

    def FW(self):
        try:
            board_id = self._calibration.read_board_id()
            carrier_id = self._carrier.read_carrier()[-6:]
            print board_id, carrier_id
            if board_id != carrier_id:
                self._led_fan.set_led_color('yellow')
                return [-1]
                # pass
            print 'lets mating check'
            # logging.info('mating check start')
            # self.reset()
            self._led_fan.set_led_color('blue')
            self._led_fan.set_fan_type('fast')
            # self._transition.set_pin(1, 11, 1)
            # self._psu2.restore()
            self._init_temperature = self._carrier.read_temperature()
            self.I2C(1.2, 'OFF')
            mating_check = self.matingcheck()
            with open(self.file_dir, 'a') as log_file:
                writer = csv.writer(log_file)
                if len(self.new_row) != 0:
                    writer.writerow(self.new_row)
                self.new_row = []
            # logging.info('mating check end')
            # print 'type:', mating_check
            if mating_check[0] == -1:
                print 'error'
                return [-1, self._predefine.FW()]
            return [0, self._predefine.FW()]
        except Exception as e:
            return [-1]

    def temp(self):
        # temperature = 25.0
        try:
            temperature = self._carrier.read_temperature()
            return [0, temperature + 273.15]
        except Exception as e:
            try:
                temperature = self._carrier.read_temperature()
                return [0, temperature + 273.15]
            except Exception as e:
                return [0, self._init_temperature + 273.15]

    def reset(self):
        try:
            self._transition.reset_all_switch()
            self._psu1.restore()
            self._psu2.restore()
            self._transition.set_dut_pull_up('pull_up_cutoff')
            # time.sleep(1.0)
            return [0]
        except Exception as e:
            return [-1]

    def I2C(self, volt, pull_up):
        try:
            volt = round(volt * 10)
            volt /= 10.0
            self._transition.set_dut_pull_up_voltage(volt)
            resistance = TransitionBoardDef.I2C_PULL_UP_2_2K if pull_up == 'ON' else TransitionBoardDef.I2C_PULL_UP_NONE
            self._transition.set_dut_pull_up(resistance)
            print 'I2C set:', volt, pull_up
            return [0]
        except Exception as e:
            return [-1]

    def ptc23_check(self, delay, duration):
        try:

            self._transition.set_switch(TransitionBoardDef.SWITCH_PS1_CELL_POS_CELL_NEG, 1)
            self._psu1.fv(3.8, 0.1, PSU1BoardDef.CURRENT_RANGE_100mA)
            time.sleep(0.1)
            self._transition.set_switch(TransitionBoardDef.SWITCH_CELL_POS_TP3, 1)
            time.sleep(0.1)
            self._transition.set_switch(TransitionBoardDef.SWITCH_CELL_POS_TP3, 0)
            time.sleep(2)

            # neg_resistance test
            # self._transition.set_switch(TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG, 1)
            # self._psu2.fi(0.5, 0.5, PSU2BoardDef.CURRENT_RANGE_1A)
            # self._psu2.output(True)
            # self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            # self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            # voltage_neg = self._dvm.measure_voltage(1000, 0.1)
            # self._dvm.set_input(DVMBoardDef.PSU2_HC_1)
            # self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            # r_sense = PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_1A]
            # psu_gain = PSU2BoardDef.GAIN_TYPE[PSU2BoardDef.CURRENT_RANGE_1A]
            # volt = self._dvm.measure_voltage(1000, 0.1)
            # current_neg = volt / r_sense / psu_gain
            # res_neg = voltage_neg / current_neg
            # print 'neg_volt[', voltage_neg, '] neg_current[', current_neg, ']'
            # print 'res_neg[', res_neg, ']'
            # # self._transition.set_switch(TransitionBoardDef.SWITCH_PS2_CELL_NEG_PACK_NEG, 0)
            # self._transition.set_pin(1, 5, 0)
            # self._transition.set_pin(1, 8, 0)
            # self._psu2.restore()

            # pos_resistance test
            # self._transition.set_switch(TransitionBoardDef.SWITCH_PS3_CELL_POS_PACK_POS, 1)
            # # self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_POS_TP3_SHORT, 1)
            # self._psu2.fi(0.5, 0.5, PSU2BoardDef.CURRENT_RANGE_1A)
            # self._psu2.output(True)
            # self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            # self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            # voltage_pos = self._dvm.measure_voltage(1000, 0.1)
            # self._dvm.set_input(DVMBoardDef.PSU2_HC_1)
            # self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            # r_sense = PSU2BoardDef.R_SENSE[PSU2BoardDef.CURRENT_RANGE_1A]
            # psu_gain = PSU2BoardDef.GAIN_TYPE[PSU2BoardDef.CURRENT_RANGE_1A]
            # volt = self._dvm.measure_voltage(1000, 0.1)
            # current_pos = volt / r_sense / psu_gain
            # res_pos = voltage_pos / current_pos
            # print 'pos_volt[', voltage_pos, '] pos_current[', current_pos, ']'
            # print 'res_pos[', res_pos, ']'
            # self._transition.set_switch(TransitionBoardDef.SWITCH_PS3_CELL_POS_PACK_POS, 0)
            # self._psu2.output(False)
            # self._psu2.restore()
            time.sleep(delay)

            # ptc2&3
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SDA, 1)
            self._dvm.set_input(DVMBoardDef.I2C_SDA)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            sda_volt = self._dvm.measure_voltage(2000, 0.05)
            sda_volt = self._calibration.cal_mv(0, PSU1BoardDef.CURRENT_RANGE_100mA, sda_volt)
            print 'ptc2&3 check', 'sda volt', sda_volt
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SDA, 0)
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SCL, 1)
            self._dvm.set_input(DVMBoardDef.I2C_SCL)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            scl_volt = self._dvm.measure_voltage(2000, 0.05)
            scl_volt = self._calibration.cal_mv(0, PSU1BoardDef.CURRENT_RANGE_100mA, scl_volt)
            print 'ptc2&3 check', 'scl_volt', scl_volt
            self._transition.set_switch(TransitionBoardDef.SWITCH_EXT_MV_SCL, 0)

            # time.sleep(0.01)
            self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SDA, 1)
            cal_current = self._calibration.cal_fi(1, 3, 0.00025)
            self._psu2.fi(cal_current, 0.5, PSU2BoardDef.CURRENT_RANGE_2_5mA)
            self._psu2.output(True)
            time.sleep(delay)
            self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            # time.sleep(delay)
            # self._psu2.output(False)
            #
            # self._psu2.output(True)

            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            sda_volt_load = self._dvm.measure_voltage(1000, duration)
            print 'ptc2&3 check', 'sda_volt_load', sda_volt_load
            sda_volt_load = fabs(self._calibration.cal_mv(1, 5, sda_volt_load))
            print 'ptc2&3 check', 'cal_sda_volt_load', sda_volt_load
            self._dvm.set_input(DVMBoardDef.PSU2_MEASOUT)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            sda_i = self._dvm.measure_voltage(1000, duration) / 200.0 / 10.0
            print 'ptc2&3 check', 'sda_i', sda_i
            sda_i = self._calibration.cal_mi(1, PSU2BoardDef.CURRENT_RANGE_2_5mA, sda_i)
            print 'ptc2&3 check', 'cal_sda_i', sda_i
            self._psu2.output(False)
            self._psu2.restore()
            self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SDA, 0)

            self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SCL, 1)
            self._psu2.fi(cal_current, 0.5, PSU2BoardDef.CURRENT_RANGE_2_5mA)
            self._psu2.output(True)
            time.sleep(delay)
            self._dvm.set_input(DVMBoardDef.PSU2_SENSE)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            scl_volt_load = self._dvm.measure_voltage(1000, duration)
            print 'ptc2&3 check', 'scl_volt_load', scl_volt_load
            scl_volt_load = fabs(self._calibration.cal_mv(1, 5, scl_volt_load))
            print 'ptc2&3 check', 'cal_scl_volt_load', scl_volt_load
            self._dvm.set_input(DVMBoardDef.PSU2_MEASOUT)
            self._dvm.set_gain(DVMBoardDef.DVM_GAIN_0_P_8)
            scl_i = self._dvm.measure_voltage(1000, duration) / 200.0 / 10.0
            print 'ptc2&3 check', 'sda_i', sda_i
            scl_i = self._calibration.cal_mi(1, PSU2BoardDef.CURRENT_RANGE_2_5mA, scl_i)
            print 'ptc2&3 check', 'cal_scl_i', scl_i

            # self._psu2.output(False)
            # self._psu2.restore()
            # self._transition.set_switch(TransitionBoardDef.SWITCH_PACK_NEG_SCL, 0)

            ptc2 = ((sda_volt - sda_volt_load) / sda_i) + int(self.ptc23_offset[0])
            ptc3 = ((scl_volt - scl_volt_load) / scl_i) + int(self.ptc23_offset[1])
            print ptc2, ptc3
            return [0, ptc2, ptc3]
            # print 'int(self.ptc23_offset)', int(self.ptc23_offset[0])
            # print 'int(self.ptc23_offset)', int(self.ptc23_offset[1])
            # ptc2_usl = 1731 - 1
            # ptc2_lsl = 1594 + 1
            # ptc3_usl = 2337 - 1
            # ptc3_lsl = 2190 + 1
            # if ptc2 < ptc2_lsl or ptc2 > ptc2_usl:
            #     logging.error('PTC2 test FAIL, sda_res[' + str(ptc2) + ']')
            #     logging.error('sda_v1[' + str(sda_volt) + '], sda_v2[' + str(sda_volt_load) + '], sda_i[' + str(sda_i))
            #     return [-1]
            # elif ptc3 < ptc3_lsl or ptc3 > ptc3_usl:
            #     logging.error('PTC3 test FAIL, sda_res[' + str(ptc3) + ']')
            #     logging.error('scl_v1[' + str(scl_volt) + '], scl_v2[' + str(scl_volt_load) + '], scl_i[' + str(scl_i))
            #     return [-1]
            # return [0]
        except Exception as e:
            return [-1]
        finally:
            self.reset()
