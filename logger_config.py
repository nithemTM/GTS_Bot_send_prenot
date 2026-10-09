import logging
from PyQt5.QtCore import QObject, pyqtSignal


class QtSignalHandler(QObject):
    log_signal = pyqtSignal(str)


class QTextEditLogger(logging.Handler):
    def __init__(self, qt_signal_handler):
        super().__init__()
        self.qt_signal_handler = qt_signal_handler

    def emit(self, record):
        msg = self.format(record)
        self.qt_signal_handler.log_signal.emit(msg)


def setup_logging(qt_signal_handler):
    logger = logging.getLogger()  # root logger
    logger.setLevel(logging.DEBUG)  # lub INFO w produkcji

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    gui_handler = QTextEditLogger(qt_signal_handler)
    gui_handler.setFormatter(formatter)
    logger.addHandler(gui_handler)
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)
