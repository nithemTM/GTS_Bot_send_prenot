# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\SendPrenotGUI.ui'
# Adapted for PyQt6

# ZMIANA: Import z PyQt6 zamiast PyQt5
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 850)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 850))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.ApplicationName = QtWidgets.QLabel(self.centralwidget)
        self.ApplicationName.setObjectName("ApplicationName")
        self.gridLayout.addWidget(self.ApplicationName, 0, 0, 1, 1)
        self.ImportFromExcel = QtWidgets.QPushButton(self.centralwidget)
        self.ImportFromExcel.setObjectName("ImportFromExcel")
        self.gridLayout.addWidget(self.ImportFromExcel, 1, 0, 2, 1)
        self.labelAppInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelAppInfo.setStyleSheet("font: 10pt \"Consolas\";")
        self.labelAppInfo.setObjectName("labelAppInfo")
        self.gridLayout.addWidget(self.labelAppInfo, 1, 1, 1, 1)
        self.InfoSpace = QtWidgets.QLabel(self.centralwidget)

        # ZMIANA: W PyQt6 stałe menu kontekstowego wymagają pełnej ścieżki Enumu -> Qt.ContextMenuPolicy.DefaultContextMenu
        self.InfoSpace.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)

        self.InfoSpace.setStyleSheet("font: 12pt \"Constantia\";")
        self.InfoSpace.setWordWrap(False)
        self.InfoSpace.setObjectName("InfoSpace")
        self.gridLayout.addWidget(self.InfoSpace, 2, 1, 2, 1)
        self.StartContinuePrenot = QtWidgets.QPushButton(self.centralwidget)
        self.StartContinuePrenot.setObjectName("StartContinuePrenot")
        self.gridLayout.addWidget(self.StartContinuePrenot, 3, 0, 1, 1)
        self.StopProgram = QtWidgets.QPushButton(self.centralwidget)
        self.StopProgram.setObjectName("StopProgram")
        self.gridLayout.addWidget(self.StopProgram, 4, 0, 1, 1)
        self.labelProgressData = QtWidgets.QLabel(self.centralwidget)
        self.labelProgressData.setStyleSheet("font: 10pt \"Consolas\";")
        self.labelProgressData.setObjectName("labelProgressData")
        self.gridLayout.addWidget(self.labelProgressData, 5, 0, 1, 1)
        self.ProgressInfo = QtWidgets.QLabel(self.centralwidget)

        # ZMIANA: W PyQt6 styl cienia ramki wyciąga się przez QtWidgets.QFrame.Shadow.Plain
        self.ProgressInfo.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)

        self.ProgressInfo.setLineWidth(1)
        self.ProgressInfo.setObjectName("ProgressInfo")
        self.gridLayout.addWidget(self.ProgressInfo, 6, 0, 1, 2)
        self.labelLogInformation = QtWidgets.QLabel(self.centralwidget)
        self.labelLogInformation.setStyleSheet("font: 10pt \"Consolas\";")
        self.labelLogInformation.setObjectName("labelLogInformation")
        self.gridLayout.addWidget(self.labelLogInformation, 7, 0, 1, 1)
        self.logOutput = QtWidgets.QPlainTextEdit(self.centralwidget)

        # ZMIANA: W PyQt6 zawijanie linii w QPlainTextEdit wymaga pełnego Enumu -> QPlainTextEdit.LineWrapMode.NoWrap
        self.logOutput.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

        self.logOutput.setReadOnly(True)
        self.logOutput.setObjectName("logOutput")
        self.gridLayout.addWidget(self.logOutput, 8, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ApplicationName.setText(_translate("MainWindow", "Send Prenot Application"))
        self.ImportFromExcel.setText(_translate("MainWindow", "Import from Excel"))
        self.labelAppInfo.setText(_translate("MainWindow", "Information App"))
        self.InfoSpace.setText(_translate("MainWindow", "Info Space"))
        self.StartContinuePrenot.setText(_translate("MainWindow", "Start / Continue Prenot"))
        self.StopProgram.setText(_translate("MainWindow", "Stop Program"))
        self.labelProgressData.setText(_translate("MainWindow", "Progress data"))
        self.ProgressInfo.setText(_translate("MainWindow", "Progress Info"))
        self.labelLogInformation.setText(_translate("MainWindow", "Log Information"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # ZMIANA: Czyste exec() zamiast exec_()
    sys.exit(app.exec())
