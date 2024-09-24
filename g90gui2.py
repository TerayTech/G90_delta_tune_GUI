from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
import sys
import serial
import serial.tools.list_ports
import time


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(726, 392)

        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.ScanBox = QtWidgets.QComboBox(parent=Form)
        self.ScanBox.setGeometry(QtCore.QRect(150, 20, 131, 41))
        self.ScanBox.setObjectName("ScanBox")
        self.ConnectButton = QtWidgets.QPushButton(parent=Form)
        self.ConnectButton.setGeometry(QtCore.QRect(20, 70, 121, 41))
        self.ConnectButton.setObjectName("ConnectButton")
        self.message_box = QtWidgets.QTextBrowser(parent=Form)
        self.message_box.setGeometry(QtCore.QRect(450, 30, 256, 192))
        self.message_box.setObjectName("message_box")
        self.TuneButton = QtWidgets.QPushButton(parent=Form)
        self.TuneButton.setGeometry(QtCore.QRect(150, 170, 121, 41))
        self.TuneButton.setObjectName("TuneButton")
        self.preamp_ck = QtWidgets.QCheckBox(parent=Form)
        self.preamp_ck.setGeometry(QtCore.QRect(20, 140, 82, 20))
        self.preamp_ck.setObjectName("preamp_ck")
        self.att_ck = QtWidgets.QCheckBox(parent=Form)
        self.att_ck.setGeometry(QtCore.QRect(120, 140, 82, 20))
        self.att_ck.setObjectName("att_ck")
        self.tuner_ck = QtWidgets.QCheckBox(parent=Form)
        self.tuner_ck.setGeometry(QtCore.QRect(190, 140, 82, 20))
        self.tuner_ck.setObjectName("tuner_ck")
        self.plus3ktuneButton = QtWidgets.QPushButton(parent=Form)
        self.plus3ktuneButton.setGeometry(QtCore.QRect(150, 220, 121, 41))
        self.plus3ktuneButton.setObjectName("plus3ktuneButton")
        self.freq_disp = QtWidgets.QLCDNumber(parent=Form)
        self.freq_disp.setGeometry(QtCore.QRect(450, 330, 261, 51))
        self.freq_disp.setSmallDecimalPoint(True)
        self.freq_disp.setDigitCount(8)
        self.freq_disp.setObjectName("freq_disp")
        self.DisconnectButton = QtWidgets.QPushButton(parent=Form)
        self.DisconnectButton.setGeometry(QtCore.QRect(150, 70, 121, 41))
        self.DisconnectButton.setObjectName("DisconnectButton")
        self.GetFreqButton = QtWidgets.QPushButton(parent=Form)
        self.GetFreqButton.setGeometry(QtCore.QRect(20, 170, 121, 41))
        self.GetFreqButton.setObjectName("GetFreqButton")
        self.delta_freq = QtWidgets.QComboBox(parent=Form)
        self.delta_freq.setGeometry(QtCore.QRect(40, 220, 101, 41))
        self.delta_freq.setEditable(True)
        self.delta_freq.setPlaceholderText("")
        self.delta_freq.setObjectName("delta_freq")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(23, 230, 41, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(460, 310, 111, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(460, 10, 161, 20))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Connect the buttons to their respective functions
        self.pushButton.clicked.connect(self.scan_ports)
        self.ConnectButton.clicked.connect(self.connect_serial)
        self.DisconnectButton.clicked.connect(self.disconnect_serial)
        self.GetFreqButton.clicked.connect(self.get_frequency)

        self.preamp_ck.stateChanged.connect(self.preamp_control)
        self.att_ck.stateChanged.connect(self.att_control)
        self.tuner_ck.stateChanged.connect(self.tuner_control)
        self.TuneButton.clicked.connect(self.tune)

        self.plus3ktuneButton.clicked.connect(self.get_current_freq_and_set_delta_freq_and_tune)

        # Variable to hold the serial connection
        self.serial_connection = None

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "G90 Control"))

        self.pushButton.setText(_translate("Form", "Scan"))
        self.ConnectButton.setText(_translate("Form", "Connect"))
        self.TuneButton.setText(_translate("Form", "Tune"))
        self.preamp_ck.setText(_translate("Form", "PRE AMP"))
        self.att_ck.setText(_translate("Form", "ATT"))
        self.tuner_ck.setText(_translate("Form", "Tuner"))
        self.plus3ktuneButton.setText(_translate("Form", "Δ Tune"))
        self.DisconnectButton.setText(_translate("Form", "Disconnect"))
        self.GetFreqButton.setText(_translate("Form", "Get Frequency"))
        self.delta_freq.setCurrentText(_translate("Form", "3000"))
        self.label.setText(_translate("Form", "Δ"))
        self.label_2.setText(_translate("Form", "Current Frequency"))
        self.label_3.setText(_translate("Form", "Debug Imformation"))

    # Function to scan available serial ports and add them to the ScanBox
    def scan_ports(self):
        ports = serial.tools.list_ports.comports()
        self.ScanBox.clear()  # Clear previous entries
        for port in ports:
            self.ScanBox.addItem(port.device)
        if len(ports) == 0:
            self.message_box.append("No serial ports found.")
        else:
            self.message_box.append("Ports scanned successfully.")

    # Function to connect to the selected serial port
    def connect_serial(self):
        selected_port = self.ScanBox.currentText()
        if selected_port:
            try:
                self.serial_connection = serial.Serial(selected_port, baudrate=19200,
                                                       timeout=1)  # Set baudrate to 19200
                self.message_box.append(f"Connected to {selected_port}")
                self.serial_connection.reset_input_buffer()
                self.serial_connection.reset_output_buffer()
                # 释放PTT
                self.serial_connection.rts = False  # Set RTS low

            except Exception as e:
                self.message_box.append(f"Failed to connect: {str(e)}")
        else:
            self.message_box.append("No port selected.")

    # Function to disconnect the current serial connection
    def disconnect_serial(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
                self.message_box.append("Serial port disconnected.")
                self.serial_connection = None  # Reset the connection variable
            except Exception as e:
                self.message_box.append(f"Failed to disconnect: {str(e)}")
        else:
            self.message_box.append("No active serial connection to disconnect.")

    # Function to handle Preamp control (send command based on checkbox state)
    def preamp_control(self, state):
        if not self.serial_connection or not self.serial_connection.is_open:
            self.message_box.append("No active serial connection.")
            return

        # If ATT is checked, ignore Preamp
        # if self.att_ck.isChecked():
        #     return

        # Send different commands based on checkbox state
        if state == Qt.CheckState.Checked.value:
            self.att_ck.setChecked(False)  # Uncheck ATT
            command = bytes.fromhex('FE FE 70 E0 16 02 01 FD')  # Preamp ON
        else:
            command = bytes.fromhex('FE FE 70 E0 16 02 00 FD')  # Preamp OFF

        # Send the command
        self.serial_connection.write(command)
        self.message_box.append("指令已发送 (Preamp)")

    # Function to handle ATT control and lock Preamp
    def att_control(self, state):
        if not self.serial_connection or not self.serial_connection.is_open:
            self.message_box.append("No active serial connection.")
            return

        # Lock Preamp when ATT is checked
        if state == Qt.CheckState.Checked.value:
            self.preamp_ck.setChecked(False)  # Uncheck Preamp
            command = bytes.fromhex('FE FE 70 E0 16 02 02 FD')  # ATT ON
        else:
            command = bytes.fromhex('FE FE 70 E0 16 02 00 FD')  # ATT OFF

        # Send the command
        self.serial_connection.write(command)
        self.message_box.append("指令已发送 (ATT)")

    # Function to handle ATU control (send command based on checkbox state)
    def tuner_control(self, state):
        if not self.serial_connection or not self.serial_connection.is_open:
            self.message_box.append("No active serial connection.")
            return

        # Send different commands based on checkbox state
        if state == Qt.CheckState.Checked.value:
            command = bytes.fromhex('FE FE 70 E0 1C 01 01 FD')  # ATU ON
        else:
            command = bytes.fromhex('FE FE 70 E0 1C 01 00 FD')  # ATU OFF

        # Send the command
        self.serial_connection.write(command)
        self.message_box.append("指令已发送 (ATU)")

    # Function to handle the Tune button click (send tune command)
    def tune(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            self.message_box.append("No active serial connection.")
            return

        command = bytes.fromhex('FE FE 70 E0 1C 01 02 FD')  # Send Tune command
        self.serial_connection.write(command)
        self.message_box.append("指令已发送 (Tune)")


    # Function to send command to get frequency
    def get_frequency(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            self.message_box.append("No active serial connection.")
            return

        self.serial_connection.flushInput()
        self.serial_connection.flushOutput()


        # Send the command to get frequency
        command = bytes.fromhex('FE FE 70 E0 03 FD')
        self.serial_connection.write(command)
        self.message_box.append("指令已发送: 获取频率")

        # Read the response
        try:
            response = self.serial_connection.read(17)  # Expected response length
            self.message_box.append(f"Response: {response.hex()}")

            # 修改 get_frequency 函数中解析的部分

            # 读取频率部分时从正确的字节位置开始解析 (response[8:13])
            if response[0:4] == b'\xFE\xFE\x70\xE0':
                frequency = self.parse_frequency(response[12:16])  # 8到12字节是频率数据
                self.freq_disp.display(frequency)
                self.message_box.append(f"Frequency: {frequency} Hz")
                return frequency
            else:
                self.message_box.append("Invalid response.")
        except Exception as e:
            self.message_box.append(f"Error reading response: {str(e)}")

    # Function to parse BCD frequency bytes
    def parse_frequency(self, bcd_bytes):
        byte0 = 0
        byte1 = bcd_bytes[0]
        byte2 = bcd_bytes[1]
        byte3 = bcd_bytes[2]
        byte4 = bcd_bytes[3]

        # Parse each nibble according to the BCD encoding
        freq_hz = (byte4 >> 4) * 1000000000 + (byte4 & 0x0F) * 100000000  # 1GHz, 100MHz
        freq_hz += (byte3 >> 4) * 10000000 + (byte3 & 0x0F) * 1000000  # 10MHz, 1MHz
        freq_hz += (byte2 >> 4) * 100000 + (byte2 & 0x0F) * 10000  # 100kHz, 10kHz
        freq_hz += (byte1 >> 4) * 1000 + (byte1 & 0x0F) * 100  # 1kHz, 100Hz
        freq_hz += (byte0 >> 4) * 10 + (byte0 & 0x0F) * 1  # 10Hz, 1Hz

        return freq_hz

    # 反向生成频率控制字
    # def send_frequency_command(self, frequency):
    #     if not self.serial_connection or not self.serial_connection.is_open:
    #         self.message_box.append("No active serial connection.")
    #         return
    #
    #     # 将频率转换为BCD编码字节
    #     bcd_bytes = self.frequency_to_bcd(frequency)
    #
    #     # 构造完整的指令流，填充 Byte0 到 Byte4 的位置
    #     command = bytes([
    #         0xFE, 0xFE, 0xE0, 0x70, 0x03,  # 固定头部
    #         bcd_bytes[0],
    #         bcd_bytes[1],  # Byte1
    #         bcd_bytes[2],  # Byte2
    #         bcd_bytes[3],  # Byte3
    #         bcd_bytes[4],  # Byte4
    #
    #         0xFD  # 尾部
    #     ])
    #
    #     # 发送构造的指令流
    #     self.serial_connection.write(command)
    #     self.message_box.append(f"Frequency command sent: {command.hex().upper()}")

    def send_frequency_command(self, frequency):
        if not self.serial_connection or not self.serial_connection.is_open:
            self.message_box.append("No active serial connection.")
            return

        # 将频率转换为BCD编码字节
        bcd_bytes = self.frequency_to_bcd(frequency)

        # 确保 bcd_bytes 中的各个字节按照正确的顺序填充
        command = bytes([
            0xFE, 0xFE, 0xE0, 0x70, 0x00,  # 固定头部 最后一位0x00 代表写入
            bcd_bytes[0],  # Byte0 (10Hz 和 1Hz)
            bcd_bytes[1],  # Byte1 (1kHz 和 100Hz)
            bcd_bytes[2],  # Byte2 (100kHz 和 10kHz)
            bcd_bytes[3],  # Byte3 (10MHz 和 1MHz)
            bcd_bytes[4],  # Byte4 (1GHz 和 100MHz)
            0xFD  # 尾部
        ])

        # 发送构造的指令流
        self.serial_connection.write(command)
        self.message_box.append(f"Frequency command sent: {command.hex().upper()}")

    # Function to convert frequency to BCD, based on the previous function I provided
    def frequency_to_bcd(self, frequency):
        # 确保频率是整数（Hz）
        frequency = int(frequency)

        # 提取每个频率段的值，支持到1GHz
        ghz = (frequency // 1000000000) % 10  # 1GHz
        sub_ghz = (frequency // 100000000) % 10  # 100MHz
        mhz_high = (frequency // 10000000) % 10  # 10MHz
        mhz_low = (frequency // 1000000) % 10  # 1MHz
        khz_high = (frequency // 100000) % 10  # 100kHz
        khz_low = (frequency // 10000) % 10  # 10kHz
        hz_high = (frequency // 1000) % 10  # 1kHz
        hz_low = (frequency // 100) % 10  # 100Hz
        tens_hz = (frequency // 10) % 10  # 10Hz
        ones_hz = frequency % 10  # 1Hz

        # 构造 BCD 编码字节，符合表格中所示的各个位数
        byte4 = (ghz << 4) | sub_ghz  # 1GHz 和 100MHz
        byte3 = (mhz_high << 4) | mhz_low  # 10MHz 和 1MHz
        byte2 = (khz_high << 4) | khz_low  # 100kHz 和 10kHz
        byte1 = (hz_high << 4) | hz_low  # 1kHz 和 100Hz
        byte0 = (tens_hz << 4) | ones_hz  # 10Hz 和 1Hz (这里1Hz位为0)

        return [byte0, byte1, byte2, byte3, byte4]

    def get_current_freq_and_set_delta_freq_and_tune(self):
        # 获取当前频率
        current_freq = self.get_frequency()
        if current_freq is None:
            self.message_box.append("无法获取当前频率。")
            return

        try:
            # 获取 delta 频率值，并确保是整数
            delta_freqency = int(self.delta_freq.currentText())
        except ValueError:
            self.message_box.append("无效的Δ频率输入，请输入有效的数字。")
            return

        # 计算目标频率
        target_freq = current_freq + delta_freqency
        self.message_box.append(f"Writing Target Frequency: {target_freq} Hz")

        # 发送目标频率命令
        self.send_frequency_command(target_freq)
        time.sleep(0.1)

        # 校验新频率
        new_freq = int(self.get_frequency())
        if new_freq is None:
            self.message_box.append("无法读取新频率。")
            return

        # 比较目标频率和读取的新频率
        if new_freq == target_freq:
            self.message_box.append("成功写入Δ频率")
        else:
            self.message_box.append(f"错误：Δ频率不符，读取到的频率为 {new_freq} Hz")

        self.tune()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec())
