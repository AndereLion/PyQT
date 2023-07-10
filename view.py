from PyQt5 import QtWidgets, QtCore

from model import SerialThread


class Ui_MainWindow(object):
    def __init__(self):
        self.serialThread = None

    def send_command_to_terminal(self):
        command = self.lineEdit.text()
        self.serialThread.set_command(command)
        self.lineEdit.clear()

    def connect_hub(self):
        port = self.comboBox.currentText().split(":")[1]
        baudrate = self.comboBox2.currentText().split(":")[1]

        if port:
            if self.serialThread and self.serialThread.isRunning():
                self.serialThread.terminate()
                self.serialThread.wait()

            self.serialThread = SerialThread(port, baudrate)
            self.serialThread.dataReceived.connect(self.write_data_to_terminal)
            self.serialThread.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: darkgray;")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)

        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setObjectName("comboBox")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")
        self.gridLayout.addWidget(self.comboBox2, 10, 0, 1, 1)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Enter your command here...")
        self.gridLayout.addWidget(self.lineEdit, 3, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minicom PRO"))

        self.comboBox.setItemText(1, _translate("MainWindow", "Port:/dev/ttyS0"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Port:/dev/ttyUSB0"))

        self.comboBox2.setItemText(1, _translate("MainWindow", "Baudrate:57600"))
        self.comboBox2.setItemText(0, _translate("MainWindow", "Baudrate:115200"))

        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.pushButton.clicked.connect(self.connect_hub)

        self.lineEdit.returnPressed.connect(self.send_command_to_terminal)

    def write_data_to_terminal(self, log_data):
        self.textBrowser.append(log_data)
