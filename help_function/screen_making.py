import time
import os
import logging
from datetime import datetime

import pyautogui
import pygetwindow as gw
import win32gui

from help_function.image_detect import image_detect, image_detect_scale
from help_function.win32_library import list_all_windows


# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )
logger = logging.getLogger(__name__)

def screenshot_active_window(path_tag_screenshot, path_screen_verite=None, hwnd=None, window_label=None, delay_active_win=5, delay_save=5):
    # list_all_windows()
    first_check_active_window = False # zmienia swoja wartośc na True w moemencie wejscia w ifa po stwierdzeniu że okno jest prawidłowe,
                                      # a jezeli coś sie zmieni w trakcie zapisu zdjęcia to od razu wywali że nastąpiła ingerencja w działanie programu
    current_time_win = time.time()
    current_time_save = time.time()
    required_window = [win32gui.GetWindowText(hwnd), hwnd]
    active_window = gw.getActiveWindow()
    screen_verite_confirm = []

    while True and 'Terminal' in active_window.title:
        if path_screen_verite is None:
            path_screen_verite = []
        delay_time_win = time.time() - current_time_win
        active_window = gw.getActiveWindow()
        logger.info(f"Wymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                     f"\nAktywne okno [{active_window}] | win32gui.GetForegroundWindow(): {win32gui.GetForegroundWindow()}")

        if active_window is not None and win32gui.GetForegroundWindow() == hwnd and window_label in win32gui.GetWindowText(hwnd):
            if not first_check_active_window:
                current_time_save = time.time()
            first_check_active_window = True
            # print("teraz zmieni okno")
            # time.sleep(3)
            left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
            screen_active_win = pyautogui.screenshot(region=(left, top, width, height))
            screen_active_win.save(str(path_tag_screenshot)+'.png')
            full_path = str(path_tag_screenshot)+'.png'

            delay_time_s = time.time() - current_time_save
            logger.info(f"\nAktualane oczekiwanie na zapis -> [delay_time_s: {delay_time_s}]")
            #if os.path.isfile(full_path) and image_detect(full_path, path_screen_verite, 0.8):
            #if win32gui.GetForegroundWindow() == hwnd and window_label in win32gui.GetWindowText(hwnd) and os.path.isfile(full_path) and image_detect(full_path, path_screen_verite, 0.8):
            if win32gui.GetForegroundWindow() == hwnd and window_label in win32gui.GetWindowText(hwnd) and os.path.isfile(full_path):
                for path_screen_v in path_screen_verite:
                    if image_detect(full_path, path_screen_v, 0.8):
                        logger.info(f"Poszukiwany screenshot istnieje: {full_path}"
                                     f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                                     f"\nAktywne okno [{active_window}]")
                        path_screen_c = [path_screen_v, True]
                        screen_verite_confirm.append(path_screen_c)
                        return True, 1, path_screen_v
                    else:
                        logger.info(f"Poszukiwany screenshot nieistnieje: {full_path}"
                                     f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                                     f"\nAktywne okno [{active_window}]")
                        path_screen_c = [path_screen_v, False]
                        screen_verite_confirm.append(path_screen_c)
                        # first_check_active_window = False # TODO: zmienione ale będzie wadziło z wcześniejszą czescia kodu gdzie przy wejsciu w pierwszego ifa mamy ustawianą wartosc True
            if delay_time_s >= delay_save:
                # TODO: można dodać funkcję która będzie weryfikowac czy dany błąd istnieje już w bazie błedów na którymś ze zdjęć
                logger.info(f"Nie odnaleziono pliku screenshot!: {full_path}! "
                             f"\nMożliwość pojawienia sie błędu podczas wprowadzania w GTS informacji dla okna [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                             f"\nAktywne okno [{active_window}]")
                left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
                screen_active_win = pyautogui.screenshot(region=(left, top, width, height))
                error_time = datetime.now()
                error_time_form = error_time.strftime("%Y-%m-%d_%H-%M-%S")
                error_screen_name = 'process_errors_screens/error_process_active_win.png'+str(error_time_form)+'.png'
                screen_active_win.save(error_screen_name)
                screen_active_win.save('error_process_active_win.png')
                logger.info(f"Screen aktywnego okna podczas wystąpienia błędu -> ścieżka: {error_screen_name}")
                return False, 1, None
            time.sleep(0.1)
        elif delay_time_win >= delay_active_win and not first_check_active_window:
            logger.info("Przekroczono dopuszczalny limit poszukiwania aktywności dla okna! Możliwe że włąsciwe okno programu nie może sie wczytać!"
                         f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                         f"\nAktywne okno [{active_window}]")
            return False, 2, None
        elif first_check_active_window:
            logger.info("Nieoczekiwana zmiana aktywnego okna w trakcie próby zapisu screena aktywnego okna!"
                         f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                         f"\nAktywne okno [{active_window}]")
            return False, 2, None
        else:
            logger.info(f"\nAktualne oczekiwanie na okno -> [delay_time_win: {delay_time_win}]")
            time.sleep(0.1)
    else:
        logger.info("Nieoczekiwana zmiana aktywnego okna tuż przed próbą zapisu screena aktywnego okna! Natychmiastowe zakończenie - bez oczekiwania na okno!"
                     f"\nWymagane okno [Label_system: {required_window[0]} | HWND_system: {required_window[1]} | Label_user: {window_label}]"
                     f"\nAktywne okno [{active_window}]")
        return False, 2, None


# def screenshot_active_window(path_tag_screenshot, path_screen_verite, hwnd=None, delay_active_win=5, delay_save=5):
#     current_time = time.time()
#     required_window = [win32gui.GetWindowText(hwnd), hwnd]
#     #list_all_windows()
#     while True:
#         delay_time_w = time.time() - current_time
#         active_window = gw.getActiveWindow()
#
#         print(f"Wymagane okno [Label: {required_window[0]} | HWND: {required_window[1]}")
#         print(f"Aktywne okno [{active_window}] | win32gui.GetForegroundWindow(): {win32gui.GetForegroundWindow()}")
#
#         if active_window is not None and win32gui.GetForegroundWindow() == hwnd:
#             current_time = time.time()
#             while True:
#                 left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
#                 screen_active_win = pyautogui.screenshot(region=(left, top, width, height))
#                 screen_active_win.save(str(path_tag_screenshot)+'.png')
#                 full_path = str(path_tag_screenshot)+'.png'
#
#
#                 delay_time_s = time.time() - current_time
#                 print(f"delay_time_s: {delay_time_s}")
#                 #if os.path.isfile(full_path) and image_detect(full_path, path_screen_verite, 0.8):
#                 if os.path.isfile(full_path) and image_detect(full_path, path_screen_verite, 0.8):
#                     print(f"Poszukiwany screenshot istnieje: {full_path}")
#                     return True
#                 elif delay_time_s >= delay_save:
#                     print(f"Nie odnaleziono pliku screenshot!: {full_path}! "
#                           f"Możliwość pojawienia sie błędu podczas wprowadzania w GTS informacji dla okna [Label: {required_window[0]} | HWND: {required_window[1]}"
#                           f"Aktywne okno [{active_window}]")
#                     left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
#                     screen_active_win = pyautogui.screenshot(region=(left, top, width, height))
#                     error_time = datetime.now()
#                     error_time_form = error_time.strftime("%Y-%m-%d_%H-%M-%S")
#                     error_screen_name = 'process_errors_screens/error_process_active_win.png'+str(error_time_form)+'.png'
#                     screen_active_win.save(error_screen_name)
#                     screen_active_win.save('error_process_active_win.png')
#                     print(f"Screen aktywnego okna podczas wystąpienia błędu -> ścieżka: {error_screen_name}")
#                     return False
#                 time.sleep(0.1)
#         elif delay_time_w >= delay_active_win:
#             print("Przekroczono dopuszczalny limit poszukiwania aktywności dla okna!")
#             return False
#         else:
#             time.sleep(0.1)
#         return False