import sys
import logging
# ZMIANA: Zmieniono wszystkie PyQt5 na PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QLineEdit, QMenu
from widgets.SendPrenotGUI import Ui_MainWindow
from logger_config import QtSignalHandler
from bot_worker import BotWorker

# NOWA KOMENDA DLA PYQT6 (jeśli będziesz edytować okno w Qt Designerze):
# pyuic6 -x "C:\Users\matok4\PycharmProjects\Send_Prenot_Bot_GTS - GUI II\widgets\SendPrenotGUI.ui" -o "C:\Users\matok4\PycharmProjects\Send_Prenot_Bot_GTS - GUI II\widgets\SendPrenotGUI.py"


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signal_handler = QtSignalHandler()
        self.signal_handler.log_signal.connect(self.append_log)
        self.thread = None     # <- dodajemy atrybuty tu
        self.worker = None

        self.ui.StartContinuePrenot.clicked.connect(self.start_bot)
        self.ui.StopProgram.clicked.connect(self.stop_bot)

        #QTimer.singleShot(100, self.start_bot)

    def append_log(self, msg: str):
        self.ui.logOutput.appendPlainText(msg)

    def copy_all_logs(self):
        text = self.ui.logOutput.toPlainText()
        # ZMIANA: W PyQt6 do schowka dobieramy się przez QApplication.instance().clipboard()
        app_instance = QtWidgets.QApplication.instance()
        if app_instance:
            app_instance.clipboard().setText(text)

    def start_bot(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = QThread()
            self.worker = BotWorker()

            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.log_signal.connect(self.append_log)

            self.thread.start()

    def stop_bot(self):
        if self.worker:
            self.worker.stop()

# def create_gui_app():
#     app = QtWidgets.QApplication(sys.argv)
#     window_main = Window()
#     window_main.show()
#     sys.exit(app.exec()) # ZMIANA: exec() zamiast exec_()
#
#
# create_gui_app()
