import time
import pyautogui
import pygetwindow as gw
import win32gui
import logging
from datetime import datetime

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

logger = logging.getLogger(__name__)


class ImageObject:

    def __init__(self, hwnd_app_win_active, title_app_active, delay_check_active_win, delay_save_screen):
        self.hwnd_app_win_active = hwnd_app_win_active
        self.title_app_active = title_app_active
        self.delay_check_active_win = delay_check_active_win
        self.delay_save_screen = delay_save_screen
        self.first_check_active_window = False
        self.start_search_win_time = None
        self.start_time_save_screen = None
        self.confirm_screenshot_active = False
        self.type_of_confirmation = None
        self.path_confirm = None

    def screenshot_save_window_class(self, path_tag_screenshot):
        if self.start_search_win_time is None:
            self.start_search_win_time = time.time()
        required_window = [win32gui.GetWindowText(self.hwnd_app_win_active), self.hwnd_app_win_active]
        system_active_window = gw.getActiveWindow()
        delay_time_search_win = time.time() - self.start_search_win_time
        full_path = str(path_tag_screenshot) + '.png'
        if system_active_window is not None and win32gui.GetForegroundWindow() == self.hwnd_app_win_active and self.title_app_active in win32gui.GetWindowText(self.hwnd_app_win_active):
            delay_time_s = time.time() - self.start_time_save_screen
            self.first_check_active_window = True
            if self.start_time_save_screen in None:
                self.start_time_save_screen = time.time()
            left, top, width, height = system_active_window.left, system_active_window.top, system_active_window.width, system_active_window.height
            screen_active_win = pyautogui.screenshot(region=(left, top, width, height))

            if delay_time_s >= self.delay_save_screen:
                logger.info(f"Nie odnaleziono pliku screenshot!: {full_path}! "
                             f"\nMożliwość pojawienia sie błędu podczas wprowadzania w GTS informacji dla okna [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {self.title_app_active}]"
                             f"\nAktywne okno [{system_active_window}]")
                error_time = datetime.now()
                error_time_form = error_time.strftime("%Y-%m-%d_%H-%M-%S")
                error_screen_name = 'process_errors_screens/error_process_active_win.png'+str(error_time_form)+'.png'
                screen_active_win.save(error_screen_name)
                screen_active_win.save('error_process_active_win.png')
                logger.info(f"Screen aktywnego okna podczas wystąpienia błędu -> ścieżka: {error_screen_name}")
            else:
                screen_active_win.save(str(path_tag_screenshot)+'.png')

            logger.info(f"\nAktualane oczekiwanie na zapis -> [delay_time_s: {delay_time_s}]")
            time.sleep(0.1)
        elif delay_time_search_win >= self.delay_check_active_win and not self.first_check_active_window:
            logger.info("Przekroczono dopuszczalny limit poszukiwania aktywności dla okna! Możliwe że włąsciwe okno programu nie może sie wczytać!"
                         f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {self.title_app_active}]"
                         f"\nAktywne okno [{system_active_window}]")

        elif self.first_check_active_window:
            logger.info("Nieoczekiwana zmiana aktywnego okna w trakcie próby zapisu screena aktywnego okna!"
                         f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {self.title_app_active}]"
                         f"\nAktywne okno [{system_active_window}]")
        else:
            time.sleep(0.1)

    def image_detect_class(self):
        pass
