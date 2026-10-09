import time
import win32con
import win32gui
import pygetwindow as gw
import win32process
from help_function.window_titles import enum_window_titles, search_app, path_get_target, run_app, enum_window_titles_1, wait_window, all_window
from help_function.win32_library import search_app_by_partial_title, list_all_windows, find_window, enum_child_windows, location, pobierz, get_button_info_on_hover1, get_button_info_on_hover, print_class_name_on_hover
from help_function.image_detect import image_detect
from help_function.screen_making import screenshot_active_window
from help_function.controller_automate import tab, down, up, enter, selected_key, put_text, backspace
from help_function.process_os import is_application_running, get_application_processes


# is_application_running('wfica32.exe')
#get_application_processes()
#time.sleep(30)
# _, found_pid = win32process.GetWindowThreadProcessId(search_win_hwnd)
# print("wypisz")
# print(found_pid)
# time.sleep(20)


path_app_shortcut = "C:\\Users\\matok4\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\GTSGUI_DC78^.lnk"
window_title = "Consafe Logistics - Astro WMS -  Jarosty DC CDC 310 004 Linux PROD  (M2_Jarosty-DSPL310-NB0066.awc)"
# enum_window_titles()
path_app = path_get_target(path_app_shortcut)

# print(enum_window_titles_1("GTS.AppStarter_DC78"))
#hwnd = find_window('GTS.AppStarter_DC78 - Global Terminal System  - \\\\Remote')
all_window()
# search_app(path_app, window_title)


# Przykładowe wywołanie funkcji

#enum_child_windows(hwnd)
# get_button_info_on_hover1()
list_all_windows()
app_starting = False
delay_time = 3
while True:
    partial_title_win_app = 'GTS.AppStarter_DC78 - Global Terminal System'
    partial_title_win_app_alt = 'GlobalTerminalSystem - '

    search_win_confirm, search_win_hwnd, search_win_alt_confirm = search_app_by_partial_title(partial_title_win_app, delay_time, partial_title_win_app_alt)
    #list_all_windows()
    # time.sleep(2)
    # screenshot_active_window('gts_window_screen', search_win_hwnd)
    screenshot_path = 'gts_window_screen.png'
    # item_check_path = 'image/gts_DT310_win_login.png'
    # while True:
    #     if image_detect(screenshot_path, item_check_path, 1):
    #         print("Gotowe do logowania")
    #         break

    if search_win_confirm:
        app_starting = False
        item_check_path = 'image/databaseDC310_alternative_screen.png'

        tab(2)
        up(29)
        down(22)
        #enter(1)
            

        print(f"wysłane okno: {win32gui.GetWindowText(search_win_hwnd)} | {search_win_hwnd}")
        active_window = gw.getActiveWindow()
        print(
            f"{active_window} | hwnd_: {search_win_hwnd} | przek_: {win32gui.GetWindowText(search_win_hwnd)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
        list_all_windows()
        screenshot_active_window('gts_window_screen', search_win_hwnd)
        time.sleep(1)

        if image_detect(screenshot_path, item_check_path, fit_level=0.8, input_delay=1):
            print("zrobione")
            tab(1)
            enter(1)
            search_win_confirm_1, search_win_hwnd_1, search_win_alt_confirm_1 = search_app_by_partial_title('GlobalTerminalSystem - Welcome', 5)
            if search_win_confirm_1:
                time.sleep(7)
                selected_key('-')
                put_text('RE2')
                enter(1, 0.5)
                search_win_confirm_2, search_win_hwnd_2, search_win_alt_confirm_2 = search_app_by_partial_title('GlobalTerminalSystem - RE2 - Change of notification/receipt', 5)
                if search_win_confirm_2:
                    # tab(7)
                    selected_key('-')
                    selected_key('-')
                    item_check_path = 'image/enter_receiptnumber.png'
                    screenshot_active_window('gts_window_screen', search_win_hwnd_2)
                    if image_detect(screenshot_path, item_check_path):
                        backspace(1, 1)

            else:
                print("Po próbie zalogowania nie możemy wykryć okna [GlobalTerminalSystem - Welcome]")

        else:
            print("Nie znaleziono okna, przerwano prace")
            break

    elif not search_win_confirm and not search_win_alt_confirm and not app_starting:
        print(f"odpalanie app dla {search_win_confirm} and {search_win_alt_confirm}")
        run_app(path_app)
        app_starting = True
        delay_time = 30
    elif search_win_alt_confirm:
        print(f"Znaleziono alternatywne okno: {search_win_hwnd}")
        time.sleep(15)


time.sleep(30)
partial_title_win_app = 'GlobalTerminalSystem - RE2 - Change of notification/receipt'
partial_title_win_app_alt = 'GlobalTerminalSystem - '
search_win_confirm, search_win_hwnd, search_win_alt_confirm = search_app_by_partial_title(partial_title_win_app, 3, partial_title_win_app_alt)
if search_win_confirm:
    print(f"Okno aplikacji zostało odnalezione i zmaxymalizowane dla [partial_title_win_app: {partial_title_win_app}]")
    item_check_path = 'image/enter_receiptnumber.png'
    screenshot_active_window('gts_window_screen', search_win_hwnd)
    if image_detect(screenshot_path, item_check_path):
        backspace(1, 1)
        print(f"Odnaleziono [item_check_path: {item_check_path}] w obrębie [screenshot_path: {screenshot_path}]")
        time.sleep(10)
    else:
        print(f"Nie odnaleziono [item_check_path: {item_check_path}] w obrębie [screenshot_path: {screenshot_path}]")
        time.sleep(10)
elif search_win_alt_confirm:
    print(f"Okno aplikacji NIE zostało odnalezione dla [partial_title_win_app: {partial_title_win_app}] "
          f"ale mamy alternatywne okno [partial_title_win_app_alt: {partial_title_win_app_alt}]")
    time.sleep(10)
else:
    print(f"Żadne pokrewne okno zalogowanej aplikacji NIE odnaleziono w tym [partial_title_win_app: {partial_title_win_app}, "
          f"partial_title_win_app_alt: {partial_title_win_app_alt}]"
          f"Teraz wyszukiwanie okna logowania")
    time.sleep(10)









#image_()
# print_class_name_on_hover()
# get_button_info_on_hover()
#pobierz(937, 708)
#location()


# from help_function.window_titles import enum_window_titles, search_app, path_get_target, run_app, find_window, enum_window_titles_1
#
# if __name__ == '__main__':
#     path_app_shortcut = "C:\\Users\\matok4\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\GTSGUI_DC78^.lnk"
#     # enum_window_titles()
#     path_app = path_get_target(path_app_shortcut)
#     run_app(path_app)
#     print(enum_window_titles_1("GTS.AppStarter_DC78"))
#     # find_window("GTS.AppStarter_DC78 - Global Terminal System  - \\Remote")
#     #search_app(path_app)

