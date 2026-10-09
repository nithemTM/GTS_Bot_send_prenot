import win32con
import win32gui
import time
import win32api
import pyautogui
from help_function.raise_exception_object import ExceptionObject


def find_window_by_partial_title(partial_title):
    def enum_windows_callback(h, _):
        print(f"Tytuł okna: {win32gui.GetWindowText(h)}, hwnd: {h}, len: {len(win32gui.GetWindowText(h))}")
        return True
    hwnd = None  # Zainicjuj hwnd jako None, aby wiedzieć, że na początku nic nie znaleziono
    confirm = False
    window_name = None
    win32gui.EnumWindows(enum_windows_callback, None)
    print(f"confirm:{confirm}")
    print(f"to jest hwnd: {hwnd}")
    return hwnd, window_name, confirm


def bring_window_to_front(hwnd, window_title, delay=5):

    if hwnd:

        # [MOVING OKNA - SPOSOB 1] ustawianie rozmiaru okna i jego pozycji
        # win32gui.MoveWindow(hwnd, 10, 10, 1236, 723, True)
        # rec = win32gui.GetWindowRect(hwnd)
        # x = rec[0]
        # y = rec[1]
        # [MOVING OKNA - SPOSOB 2]
        #win32gui.SetWindowPos(hwnd,win32con.HWND_TOP, x, y, 1300, 800, win32con.SWP_NOZORDER | win32con.SWP_NOMOVE)

        # [FLAGOWANIE] ustawianie flagi na maxymalizacje po zminimalizowaniiu okna ale flaga musi być ustawiona przed jego zminimalizowaniem
        # placement_win = win32gui.GetWindowPlacement(hwnd)
        # if placement_win[1] == win32con.SW_SHOWMINIMIZED:
        #     win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        #     print("1 jestem ifie po maximalizacji ")
        #     placement_win = win32gui.GetWindowPlacement(hwnd)
        #
        # time.sleep(1)
        # placement_win = list(placement_win)
        # placement_win[0] |= win32con.WPF_RESTORETOMAXIMIZED
        # win32gui.SetWindowPlacement(hwnd, placement_win)
        # print(f"stan-1:{win32gui.GetWindowPlacement(hwnd)}")
        #
        # win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        # print("2 jestem ifie po minimalizacji ")
        # print(f"stan0:{win32gui.GetWindowPlacement(hwnd)}")
        #
        # win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        #
        # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        #                       win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        # print("3 jestem ifie po maximalizacji ")
        # print(f"stan1:{win32gui.GetWindowPlacement(hwnd)}")

        #win32gui.SetFocus(hwnd)



        #win32gui.BringWindowToTop(hwnd)
        current_time = time.time()
        while True:
            win32gui.SetForegroundWindow(hwnd)
            delay_time = time.time() - current_time
            print(f"hwnd: {hwnd}, sys: {win32gui.GetForegroundWindow()}, titl: {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
            if win32gui.GetForegroundWindow() == hwnd:
                placement_win = win32gui.GetWindowPlacement(hwnd)
                app_window_size = win32gui.GetWindowRect(hwnd)
                screen_window_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
                app_window_width = app_window_size[2]-app_window_size[0]
                print(f"width_screen_window:{screen_window_width} | size_app_window: {app_window_size} | "
                      f"height_app: {app_window_size[3]-app_window_size[1]} | width_app: {app_window_width} | "
                      f"stan_before_win_app:{win32gui.GetWindowPlacement(hwnd)}")

                if app_window_width == screen_window_width:
                    time.sleep(0.5)
                    print(f"Ustawiono jako aktywne okno: {win32gui.GetWindowText(hwnd)}!")
                    print(f"Stan_equal_win_app:{win32gui.GetWindowPlacement(hwnd)}")
                    return True
                else:
                    print(f"Maxymalizacja znalezionego okna: {win32gui.GetWindowText(hwnd)}, hwnd: {hwnd} | "
                          f"stan_during_win_app:{win32gui.GetWindowPlacement(hwnd)}")
                    # ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                    #
                    # if bool(ex_style & win32con.WS_EX_TOPMOST):
                    #     win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    #     win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                    #                           win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                    #     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    partial_title_win_app = 'GTS.AppStarter_DC78 - Global Terminal System'
                    print(f"stan1:{win32gui.GetWindowPlacement(hwnd)}")
                    if placement_win[1] == win32con.SW_SHOWMINIMIZED:
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                        if partial_title_win_app not in win32gui.GetWindowText(hwnd):
                            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

                        elif partial_title_win_app in win32gui.GetWindowText(hwnd):
                            return True
                    else:
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                        if partial_title_win_app not in win32gui.GetWindowText(hwnd):
                            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

                        elif partial_title_win_app in win32gui.GetWindowText(hwnd):
                            return True

            if delay_time >= delay:
                print(f"Przekroczono czas ustawiania okna jako aktywnego [window_title: {window_title}]")
                return False
            print(f"time1 {delay_time}")

            time.sleep(0.1)
    else:
        #raise Exception("Nie znaleziono okna do ustawienia na pierwszy plan")
        print(f"Nie znaleziono okna [window_title: {window_title}] do ustawienia na pierwszy plan!")
        return False


def find_windows_callback(hwnd, search_data_window):
    # print(h)
    window_title = win32gui.GetWindowText(hwnd)
    partial_title, partial_title_alt, data_window_result, data_window_result_alt = search_data_window
    # sprawdzamy czy nie ma więcej niz jednego okna
    if data_window_result is None:
        data_window_result = []
    if data_window_result_alt is None:
        data_window_result_alt = []
    if partial_title in window_title:
        print(f"Dodano poszukiwane okno do listy [window_title: {window_title} (hwnd: {hwnd})]")
        data_window_result.append((hwnd, window_title))
    elif partial_title not in window_title and partial_title_alt is not None:
        for partial_title_a in partial_title_alt:
            if partial_title_a in window_title:
                print(f"Dodano okno alternatywne do listy [window_title: {window_title} (hwnd: {hwnd})]")
                data_window_result_alt.append((hwnd, window_title))
    return True


def app_window_qty_callback(hwnd, search_data_window):
    window_title = win32gui.GetWindowText(hwnd)
    partial_title, data_result = search_data_window
    if data_result is None:
        data_result = []
    if partial_title in window_title:
        data_result.append((hwnd, window_title))
        rect = win32gui.GetWindowRect(hwnd)

        # Współrzędne przycisku "X" (w prawym górnym rogu okna)
        x_close = rect[2] - 10  # 10 pikseli od prawej krawędzi
        y_close = rect[1] + 10  # 10 pikseli od górnej krawędzi

        # Przenieś kursor na przycisk "X" i kliknij
        pyautogui.moveTo(x_close, y_close)
        pyautogui.click()
        #win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        print(f"Dodano okno zawierające w tytule frazę {partial_title} z listy [window_title: {window_title} (hwnd: {hwnd})]")
    return True


def find_window_stos_callback(hwnd, data_window_to_search):
    window_text = win32gui.GetWindowText(hwnd)

    if data_window_to_search[0].lower() in window_text.lower():
        print(f"Apkikacja GTS aktywna")
        data_window_to_search[1] = 'AKTYWNA'
    return True


def search_app_by_partial_title(partial_title, delay_time, partial_title_alt_tab=None):

    print(partial_title)
    current_time = time.time()
    hwnd = None
    window_title = None
    hwnd_alt = None
    window_title_alt = None
    confirm_alt = False

    while hwnd is None:
        data_window = []
        data_window_alt = []
        actual_delay = time.time() - current_time
        # szukanie głównego okna

        win32gui.EnumWindows(find_windows_callback, (partial_title, partial_title_alt_tab, data_window, data_window_alt))
        print(len(data_window))
        print(data_window)
        print(len(data_window_alt))
        print(data_window_alt)
        # szukanie okna alternatywnego
        # if len(data_window) == 0 and partial_title_alt_tab is not None:
        #     for partial_title_alt in partial_title_alt_tab:
        #         print(f"Próba odszukania alternatywnego okno dla [partial_title_alt: {partial_title_alt}]")
        #         win32gui.EnumWindows(find_windows_callback, (partial_title_alt, data_window_alt))

        print(f"actual_delay: {actual_delay}")
        if len(data_window) > 1 or len(data_window_alt) > 1 or (len(data_window) > 0 and len(data_window_alt) > 0):
            print(f"Uwaga za duża ilość otwartych okien aplikacji, Może być aktywne tylko jedno! Wystartuj program na nowo!")
            data_window_sum = data_window + data_window_alt
            return False, None, False, data_window_sum
        elif len(data_window) == 0 and actual_delay < delay_time:
            print(f"Nie znaleziono okna dla [partial_title: {partial_title}], ponowna próba za 1 sekundę...")
            time.sleep(1)
        elif len(data_window) == 1 and len(data_window_alt) == 0:
            hwnd, window_title = data_window[0]
            print(f"Znaleziono okno o hwnd: {hwnd}")
            print(f"Ustawianie okna [window_title: {window_title}, hwnd: {hwnd}] na pierwszy plan...")
            confirm_focus_win = bring_window_to_front(hwnd, window_title)
            confirm_alt = False
            return confirm_focus_win, hwnd, confirm_alt, data_window[0]
        elif actual_delay >= delay_time and len(data_window) == 0:
            if len(data_window_alt) == 0:
                confirm_alt = False
                return False, hwnd, confirm_alt, data_window_alt
            elif len(data_window_alt) == 1:
                hwnd_alt, window_title_alt = data_window_alt[0]
                print(f"Znaleziono okno alternatywne o hwnd: {hwnd_alt}")
                print(f"Ustawianie okna alternatywne [window_title: {window_title_alt}, hwnd: {hwnd_alt}] na pierwszy plan...")
                confirm_alt_focus_win = bring_window_to_front(hwnd_alt, window_title_alt)
                confirm = False
                return confirm, hwnd_alt, confirm_alt_focus_win, data_window_alt[0]


def list_all_windows():
    def enum_windows_callback(h, _):
        print(f"Tytuł okna: {win32gui.GetWindowText(h)}, hwnd: {h}, len: {len(win32gui.GetWindowText(h))}")
        return True

    win32gui.EnumWindows(enum_windows_callback, None)


# TODO: Dodać obsługę wyskakujących okien z błędami - 1 - trzeba je wykryc zrobic screena z zapisem w błedach - 2 - zamknąć to okno [focus na nie i można Alt+F4]
#  i wznowić działanie programu dla nastepnych recordów
# LISTA NAZW OKIEN:
# GlobalTerminalSystem - Error in Application - \\Remote



def close_window_button(hwnd):
    rect = win32gui.GetWindowRect(hwnd)

    # Współrzędne przycisku "X" (w prawym górnym rogu okna)
    x_close = rect[2] - 10  # 10 pikseli od prawej krawędzi
    y_close = rect[1] + 10  # 10 pikseli od górnej krawędzi

    # Przenieś kursor na przycisk "X" i kliknij
    pyautogui.moveTo(x_close, y_close)
    pyautogui.click()


def close_window_callback(hwnd, search_data_window=None):
    window_title = win32gui.GetWindowText(hwnd)
    partial_title_to_close, data_result_close = search_data_window

    if data_result_close is None:
        data_result_close = []

    if partial_title_to_close in window_title:
        data_result_close.append((hwnd, window_title))
        print(f"Zamknięto okno z wymagana frazą {partial_title_to_close} do listy [window_title: {window_title} (hwnd: {hwnd})]")
    return True









# THREADING
# def search_app_by_partial_title(partial_title, delay_time, partial_title_alt_tab=None, control_auto=None):
#
#     print(partial_title)
#     current_time = time.time()
#     hwnd = None
#     window_title = None
#     hwnd_alt = None
#     window_title_alt = None
#     confirm_alt = False
#
#
#     while hwnd is None:
#         if control_auto.run_flag:
#             data_window = []
#             data_window_alt = []
#             actual_delay = time.time() - current_time
#             # szukanie głównego okna
#
#             win32gui.EnumWindows(find_windows_callback, (partial_title, partial_title_alt_tab, data_window, data_window_alt))
#             print(len(data_window))
#             print(data_window)
#             print(len(data_window_alt))
#             print(data_window_alt)
#             # szukanie okna alternatywnego
#             # if len(data_window) == 0 and partial_title_alt_tab is not None:
#             #     for partial_title_alt in partial_title_alt_tab:
#             #         print(f"Próba odszukania alternatywnego okno dla [partial_title_alt: {partial_title_alt}]")
#             #         win32gui.EnumWindows(find_windows_callback, (partial_title_alt, data_window_alt))
#
#             print(f"actual_delay: {actual_delay}")
#             if len(data_window) > 1 or len(data_window_alt) > 1 or (len(data_window) > 0 and len(data_window_alt) > 0):
#                 print(f"Uwaga za duża ilość otwartych okien aplikacji, Może być aktywne tylko jedno! Wystartuj program na nowo!")
#                 data_window_sum = data_window + data_window_alt
#                 return False, None, False, data_window_sum
#             elif len(data_window) == 0 and actual_delay < delay_time:
#                 print(f"Nie znaleziono okna dla [partial_title: {partial_title}], ponowna próba za 1 sekundę...")
#                 time.sleep(1)
#             elif len(data_window) == 1 and len(data_window_alt) == 0:
#                 hwnd, window_title = data_window[0]
#                 print(f"Znaleziono okno o hwnd: {hwnd}")
#                 print(f"Ustawianie okna [window_title: {window_title}, hwnd: {hwnd}] na pierwszy plan...")
#                 confirm_focus_win = bring_window_to_front(hwnd, window_title)
#                 confirm_alt = False
#                 return confirm_focus_win, hwnd, confirm_alt, data_window[0]
#             elif actual_delay >= delay_time and len(data_window) == 0:
#                 if len(data_window_alt) == 0:
#                     confirm_alt = False
#                     return False, hwnd, confirm_alt, data_window_alt
#                 elif len(data_window_alt) == 1:
#                     hwnd_alt, window_title_alt = data_window_alt[0]
#                     print(f"Znaleziono okno alternatywne o hwnd: {hwnd_alt}")
#                     print(f"Ustawianie okna alternatywne [window_title: {window_title_alt}, hwnd: {hwnd_alt}] na pierwszy plan...")
#                     confirm_alt_focus_win = bring_window_to_front(hwnd_alt, window_title_alt)
#                     confirm = False
#                     return confirm, hwnd_alt, confirm_alt_focus_win, data_window_alt[0]
#         else:
#             print("Przerwano ponieważ wykryto ruch myszy")
#             raise ExceptionObject("Wykryto ruch myszy")







# def find_windows_callback(hwnd, search_data_window):
#     # print(h)
#     window_title = win32gui.GetWindowText(hwnd)
#     partial_title, data_window_result = search_data_window
#     if partial_title in window_title:
#         print(f"Znaleziono poszukiwane okno [window_title: {window_title} (hwnd: {hwnd})]")
#         data_window_result.append((hwnd, window_title))
#
#     return True


# def search_app_by_partial_title(partial_title, delay_time, partial_title_alt_tab=None):
#
#     print(partial_title)
#     current_time = time.time()
#     hwnd = None
#     window_title = None
#     hwnd_alt = None
#     window_title_alt = None
#     confirm_alt = False
#
#
#     while hwnd is None:
#         data_window = []
#         data_window_alt = []
#         actual_delay = time.time() - current_time
#         # szukanie głównego okna
#         win32gui.EnumWindows(find_windows_callback, (partial_title, data_window))
#         print(len(data_window))
#         # szukanie okna alternatywnego
#         if len(data_window) == 0 and partial_title_alt_tab is not None:
#             for partial_title_alt in partial_title_alt_tab:
#                 print(f"Próba odszukania alternatywnego okno dla [partial_title_alt: {partial_title_alt}]")
#                 win32gui.EnumWindows(find_windows_callback, (partial_title_alt, data_window_alt))
#
#         print(f"actual_delay: {actual_delay}")
#
#         if len(data_window) == 0 and actual_delay < delay_time:
#             print(f"Nie znaleziono okna dla [partial_title: {partial_title}], ponowna próba za 1 sekundę...")
#             time.sleep(1)
#         elif len(data_window) > 0:
#             hwnd, window_title = data_window[0]
#             print(f"Znaleziono okno o hwnd: {hwnd}")
#             print(f"Ustawianie okna [window_title: {window_title}, hwnd: {hwnd}] na pierwszy plan...")
#             confirm_focus_win = bring_window_to_front(hwnd, window_title)
#             confirm_alt = False
#             return confirm_focus_win, hwnd, confirm_alt, data_window[0]
#         elif actual_delay >= delay_time and len(data_window) == 0:
#             if len(data_window_alt) == 0:
#                 confirm_alt = False
#                 return False, hwnd, confirm_alt, [None, None]
#             elif len(data_window_alt) > 0:
#                 hwnd_alt, window_title_alt = data_window_alt[0]
#                 print(f"Znaleziono okno alternatywne o hwnd: {hwnd_alt}")
#                 print(f"Ustawianie okna alternatywne [window_title: {window_title_alt}, hwnd: {hwnd_alt}] na pierwszy plan...")
#                 confirm_alt_focus_win = bring_window_to_front(hwnd_alt, window_title_alt)
#                 confirm = False
#                 return confirm, hwnd_alt, confirm_alt_focus_win, data_window_alt[0]
#         #return False, hwnd, False






















def print_class_name_on_hover():
    try:
        while True:
            # Pobierz aktualną pozycję kursora
            x, y = win32api.GetCursorPos()

            # Uzyskaj uchwyt okna (lub kontrolki) pod kursorem
            hwnd = win32gui.WindowFromPoint((x, y))
            if hwnd:
                class_name = win32gui.GetClassName(hwnd)
                print(f'Class name: {class_name}')

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Monitoring zakończony.")


def is_button(hwnd):
    class_name = win32gui.GetClassName(hwnd)
    return class_name == "Button"


# Funkcja do uzyskiwania uchwytu i tekstu przycisku pod kursorem
def get_button_info_on_hover():
    previous_hwnd = None
    try:
        while True:
            # Pobierz aktualną pozycję kursora
            x, y = win32api.GetCursorPos()

            # Uzyskaj uchwyt okna (lub kontrolki) pod kursorem
            hwnd = win32gui.WindowFromPoint((x, y))

            # Funkcja do wywołania dla każdej kontrolki
            def callback(child_hwnd, lParam):
                if is_button(child_hwnd):
                    button_text = win32gui.GetWindowText(child_hwnd)
                    print(f'Uchwyt: {child_hwnd}, Tekst przycisku: "{button_text}"')
                return True  # Kontynuuj przeglądanie

            # Jeśli uchwyt się zmienił, przeszukaj dzieci kontrolki
            if hwnd != previous_hwnd:
                previous_hwnd = hwnd
                win32gui.EnumChildWindows(hwnd, callback, None)

            time.sleep(0.1)  # Małe opóźnienie, aby uniknąć nadmiernego obciążenia CPU

    except KeyboardInterrupt:
        print("Monitoring zakończony.")


def location():
    try:
        while True:
            x, y = win32api.GetCursorPos()
            print(f'Współrzędne: x={x}, y={y}')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program zatrzymany przez użytkownika.")


def pobierz(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(1)
    hwnd = win32gui.WindowFromPoint((x, y))
    button_text = win32gui.GetWindowText(hwnd)
    print(f'Uchwyt: {hwnd}, Tekst przycisku: "{button_text}"')


def get_button_info_on_hover1():
    previous_hwnd = None
    try:
        while True:
            # Pobierz aktualną pozycję kursora
            x, y = win32api.GetCursorPos()

            # Uzyskaj uchwyt okna na podstawie pozycji kursora
            hwnd = win32gui.WindowFromPoint((x, y))

            if hwnd != previous_hwnd:
                # Jeśli uchwyt się zmienił, uzyskaj nowy tekst przycisku
                previous_hwnd = hwnd
                button_text = win32gui.GetWindowText(hwnd)
                print(f'Uchwyt: {hwnd}, Tekst przycisku: "{button_text}"')

            time.sleep(0.1)  # Małe opóźnienie, aby uniknąć nadmiernego obciążenia CPU

    except KeyboardInterrupt:
        print("Monitoring zakończony.")


def enum_child_windows(window_handle):
    child_handles = []
    print("teraz listuj")
    def callback(hwnd, l_param):
        text = win32gui.GetWindowText(hwnd)
        child_handles.append((hwnd, text))
        print(f"button: {text} : {hwnd}")
    win32gui.EnumChildWindows(window_handle, callback, None)
    return child_handles


def find_window(title):
    print(title)
    hwnd = win32gui.FindWindow(None, title)  # Szuka okna po pełnym tytule
    if hwnd == 0:  # Jeśli nie znalazło okna
        print("Okno nie zostało znalezione.")
        return None
    else:
        print(f"Znaleziono okno o hwnd 1: {hwnd}")
        return hwnd

##########################################################


