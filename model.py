import serial
from PyQt5 import QtCore


class SerialThread(QtCore.QThread):
    dataReceived = QtCore.pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.command = ""

    def set_command(self, command):
        self.command = command

    def run(self):
        ser = serial.Serial(port=self.port, baudrate=self.baudrate)
        value = ser.readline()
        while value:
            if self.command:
                ser.write(self.command.encode() + b"\r\n")
                self.command = ""

            value = ser.readline()
            try:
                value_in_string = value.decode().replace("\n", "")

            except UnicodeDecodeError:
                self.dataReceived.emit("Please use valid baud rate!!!")
                break
            self.dataReceived.emit(value_in_string)
