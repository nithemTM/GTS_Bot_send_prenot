from PyQt5.QtCore import QObject, pyqtSignal
from bot_main import run_bot1
import logging
import time


class BotWorker(QObject):
    finished = pyqtSignal()
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        logger = logging.getLogger(__name__)
        run_bot1()
        self.finished.emit()

    def stop(self):
        self._running = False
