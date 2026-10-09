import sys
import pythoncom
pythoncom.CoInitialize()

from logger_config import setup_logging
from main_GUI import Window
# ZMIANA: Zmieniono PyQt5 na PyQt6
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    setup_logging(window.signal_handler)
    window.show()
    # ZMIANA: W PyQt6 używa się czystego app.exec() zamiast app.exec_()
    sys.exit(app.exec())
