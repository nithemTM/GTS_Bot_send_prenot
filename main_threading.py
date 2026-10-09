import time
import win32con
import win32gui
import pygetwindow as gw
import win32process

from help_function.menu_function import main_menu
from help_function.window_titles import enum_window_titles, search_app, path_get_target, run_app, enum_window_titles_1, wait_window, all_window
from help_function.win32_library import search_app_by_partial_title, list_all_windows, close_window_callback, app_window_qty_callback, find_window, enum_child_windows, location, pobierz, get_button_info_on_hover1, get_button_info_on_hover, print_class_name_on_hover
from help_function.image_detect import image_detect
from help_function.screen_making import screenshot_active_window
from help_function.controller_automate import tab, down, up, enter, selected_key, put_text, backspace, f10, ctrl_q, copy, home, escape, on_move
from help_function.process_os import is_application_running, get_application_processes
from help_function.controller_auto_object import AutoControlObject

import threading

# is_application_running('wfica32.exe')
#get_application_processes()
#time.sleep(30)
# _, found_pid = win32process.GetWindowThreadProcessId(search_win_hwnd)
# print("wypisz")
# print(found_pid)
# time.sleep(20)


def run_bot(control_interrupt):

    path_app_shortcut = "C:\\Users\\matok4\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\GTSGUI_DC78^.lnk"
    window_title = "Consafe Logistics - Astro WMS -  Jarosty DC CDC 310 004 Linux PROD  (M2_Jarosty-DSPL310-NB0066.awc)"
    # enum_window_titles()
    path_app = path_get_target(path_app_shortcut)

    # print(enum_window_titles_1("GTS.AppStarter_DC78"))
    #hwnd = find_window('GTS.AppStarter_DC78 - Global Terminal System  - \\\\Remote')
    #all_window()
    #list_all_windows()
    # data_window = []
    # win32gui.EnumWindows(app_window_qty_callback, ('Global', data_window))
    # print(data_window)
    # print(len(data_window))
    # if len(data_window) > 1:
    #     win32gui.EnumWindows(close_window_callback, ('GlobalTerminalSystem - \\\\Remote', None))
    # search_app(path_app, window_title)


    # Przykładowe wywołanie funkcji

    #enum_child_windows(hwnd)
    # get_button_info_on_hover1()
    #list_all_windows()
    app_started = False
    delay_time = 3
    description = None
    menu_confirm = True
    #index_loop = 10
    several_window = 0
    csm_prenot = ['409090073', '406170022', '409110187', '409090105', '408280072']
    index_loop = len(csm_prenot)-1

    while True:
        try:
            if not app_started or several_window >= 2:
                a = main_menu(description)
                if not a:
                    break

            control_interrupt.run_flag = True
            control_interrupt.listener_run = True
            partial_title_win_app = 'GlobalTerminalSystem - RT2 - Registration of OPDC/transitrecei'
            # partial_title_win_app_alt = 'GlobalTerminalSystem - '
            partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'GTS.AppStarter_DC78 - Global Terminal System']

            search_win_confirm, search_win_hwnd, search_win_alt_confirm, window_data = search_app_by_partial_title(partial_title_win_app,
                                                                                                      delay_time,
                                                                                                      partial_title_win_app_alt, control_interrupt)


            # list_all_windows()
            # time.sleep(2)
            # screenshot_active_window('gts_window_screen', search_win_hwnd)
            screenshot_path = 'gts_window_screen.png'
            screenshot_path_error = 'error_process_active_win.png'
            # item_check_path = 'image/gts_DT310_win_login.png'
            # while True:
            #     if image_detect(screenshot_path, item_check_path, 1):
            #         print("Gotowe do logowania")
            #         break
            #text_valid = input(">> ")
            if search_win_confirm:
                app_started = True
                description = "Aplikacja GTS została wykryta!"

                while index_loop >= 0 and window_data[0] == win32gui.GetForegroundWindow() and window_data[1] == win32gui.GetWindowText(window_data[0]):
                    print("######################")
                    print(f"window_data_info->{window_data[0]} : {win32gui.GetForegroundWindow()} | {window_data[1]} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                    print("######################")

                    f10(1, 0.1)
                    ctrl_q(2, 0.1)

                    confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'], window_data[0], window_data[1])
                    if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path, 'image/win_RT2_verify.png', fit_level=0.8, input_delay=1):
                        backspace(1, 0.1)
                        # TODO: jakikolwiek False zostanie wyrzucony mozna ten csm sprobowac jeszcze raz przepuscic,
                        #  jezeli za drugim razem nie zostanie poprawnie wprowadzony to znaczy ze w GTS pojawia sie problem z jego wrzuceniem
                        # TODO: tutaj bedzie potrzebny wrzucenie juz wspoldziałanie z plikiem excel

                        #text_valid = '409020095' # -> st 4
                        #text_valid = '312060170' # -> st 1
                        #text_valid = '310230090' # -> st 0
                        #text_valid = '404270004' # -> st 3
                        #text_valid = '309150051' # -> nietranzytowy
                        text_valid = csm_prenot[index_loop]
                        index_loop -= 1
                        put_text(text_valid)
                        clipboard_content, confirm_valid_clipboard = copy(1, text_valid)
                        if not confirm_valid_clipboard or clipboard_content is None:
                            index_loop += 1
                            print("Nie ma właściwej wartości w oknie")
                            print(clipboard_content)
                            # TODO: mozna tutaj dodac funkcje robiaca scrina aktywnego okna zeby sprawdzic co sie wydarzyło,
                            #  dodatkowo skopiowac to co było w schowku i razem z wartoscia ktora powinna sie tam znalezc umiescic w logach
                            #continue
                            break
                        home(1, 0.1)
                        confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_STATUS_1_verify.png', 'image/win_STATUS_0_verify.png', 'image/win_STATUS_3_verify.png', 'image/win_STATUS_4_verify.png'], window_data[0], window_data[1])
                        # if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path, 'image/win_TransitTransport_verify.png', fit_level=0.8, input_delay=1):
                        if confirm_screenshot_active and type_of_confirmation == 1 and 'STATUS_1' in path_confirm:

                            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_MenuChoice_registration_verify.png'], window_data[0], window_data[1])
                            if confirm_screenshot_active and type_of_confirmation == 1 and 'MenuChoice_registration' in path_confirm: #image_detect(screenshot_path, 'image/win_MenuChoice_registration_verify.png', fit_level=0.8, input_delay=1):
                                put_text('1', 0.1)
                                enter(1, 0.1)
                                confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_RT2_EnterSenddatePrenot_verify.png'], window_data[0], window_data[1])
                                if confirm_screenshot_active and type_of_confirmation == 1 and 'RT2_EnterSenddatePrenot' in path_confirm:
                                    confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_SendPrenotBtn_verify.png', 'image/win_DeletePrenotBtn_verify.png', 'image/win_LackPrenotBtn_verify.png'], window_data[0], window_data[1])
                                    #if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path, 'image/win_SendPrenotBtn_verify.png', fit_level=0.8, input_delay=1):
                                    if confirm_screenshot_active and type_of_confirmation == 1 and 'SendPrenotBtn_' in path_confirm:
                                        print('Możemy clikac "Send Prenot to WMS"\n\n')
                                        # TODO: tutaj będzie można dalej pociągnąć temat kliknięc SEND PRENOT + wszelkie BŁĘDY
                                    elif confirm_screenshot_active and type_of_confirmation == 1 and 'DeletePrenotBtn_' in path_confirm:
                                        # TODO: tutaj co w przypadku jeżeli otrzymamy DELET PRENOT
                                        print('Mamy "Delate Prenot to WMS"!\n\n')
                                    elif confirm_screenshot_active and type_of_confirmation == 1 and 'LackPrenotBtn_' in path_confirm:
                                        # TODO: tutaj co w przypadku jeżeli otrzymamy DELET PRENOT
                                        print('Brak przycisku do wysyłki zamówień tranzytowych! Prawdopodobnie nie jest to tranzyt! brak przycisku\n\n')
                                    else:
                                        print("Prawdopodobnie błąd który powinien sie pokazać w nastepnej linijce kodu!\n\n")
                        elif confirm_screenshot_active and type_of_confirmation == 1 and 'STATUS_0' in path_confirm:
                            print("STATUS 0 - > do odnotowania w pliku")
                        elif confirm_screenshot_active and type_of_confirmation == 1 and ('STATUS_4' in path_confirm or 'STATUS_3' in path_confirm):
                            print("STATUS 3 lub 4 tego transportu - > Został już wprowadzony")
                        # elif confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path, 'image/win_CommonTransport_verify.png', fit_level=0.8, input_delay=1):
                        #     print("Nie jest to tranzytowy Receipt!")
                        #     continue

                            # TODO: do oznakowania jako 'do sprawdzenia' w excel, później można dodać opcję sprawdzania błędów, tablice która przeleci po wszystkich scrinach z błędami i sprawdzi czy to błąd i wypisze go w logach
                            #  w osobnym folderze trzeba zrobić możliwosc zapisywania zrzutów aplikacji jeżeli wystąpi problem, wtedy poznamy wszystkie błędy jakie są dostepne
                            # TODO: Niezbedne bedzie tez wypisanie w logach dodatkowych informacji o tym co było szukane itd.
                    if not confirm_screenshot_active and type_of_confirmation == 1:
                        # TODO: jezeli bład powtórzy sie dwa razy z rzedu a nie jest on błędem z podwójnym oknem(trzeba to wykluczyć)
                        #  tylko błędem wartości bądz innym wyświetlanym tylko na dole okna wtedy pomijamy go, i zaznaczamy w pliku dla USERA
                        if image_detect(screenshot_path_error, 'error_image_patterns/win_RT2_QueryCausedNoRecords_error.png', fit_level=0.8, input_delay=2):
                            print("Znaleziony błąd: RT2_QueryCausedNoRecords")
                        else:
                            print("Nieznany błąd programu -> spróbuj odszukać PrintScreen dla tego błędu z podanej wcześniej ścieżki.")
                        index_loop += 1
                        #continue
                        break
                    if not confirm_screenshot_active and type_of_confirmation == 2:
                        index_loop += 1
                        print("Nieprawidłowe okno w programie -> Nastąpi wznowienie ostatniego procesu od początku aby odnaleźć prawidłowe okno!\n"
                              "Prawdopodobnie nie załadowało się okno w programie")
                        #continue
                        break
                    print(index_loop)
                    print("######################")
                    print(f"{window_data[0]} : {win32gui.GetForegroundWindow()} | {window_data[1]} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                    print("######################")
                else:
                    if window_data[0] != win32gui.GetForegroundWindow() or window_data[1] != win32gui.GetWindowText(window_data[0]):
                        index_loop += 1
                        print(
                            f"Wymagane okno [{window_data[0]} : {window_data[1]}] <-> Aktywne okno [{win32gui.GetForegroundWindow()} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}]")
                        print("Zakonczono dzialanie petli! Przyczyna -> nieprawidlowe okno -> Program wznowi pracę powtarzając cały ostatni proces!")

                    elif index_loop < 0:
                        print(
                            "Zakonczono dzialanie petli! Przyczyna -> zostało juz zakończone wrzucanie PRENOT")


                    # TODO: trzeba doprecyzowac jaka przyczyna wywalenia pętli tutaj bedzie można wkleić wartosc receiptno i dalsze kroki.

                input_menu = int(input(">> "))
                # os.system('cls')
                if input_menu == 1:
                    continue
                else:
                    break
            elif search_win_alt_confirm and 'GTS.AppStarter_DC78 - Global Terminal System' not in win32gui.GetWindowText(search_win_hwnd):
                app_started = True
                print(f"Znaleziono alternatywne okno: {search_win_hwnd} | {win32gui.GetWindowText(search_win_hwnd)}")
                f10(1, 0.1)
                ctrl_q(1, 0.1)
                put_text('RT2')
                enter(1, 0.1)

            elif search_win_alt_confirm and 'GTS.AppStarter_DC78 - Global Terminal System' in win32gui.GetWindowText(search_win_hwnd):
                app_started = True
                print(f"Znaleziono alternatywne okno logowania: {search_win_hwnd} | {win32gui.GetWindowText(search_win_hwnd)}")
                tab(2)
                up(29)
                down(22)
                active_window = gw.getActiveWindow()
                print(
                    f"{active_window} | hwnd_: {search_win_hwnd} | przek_: {win32gui.GetWindowText(search_win_hwnd)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
                # list_all_windows()
                # time.sleep(1)
                screenshot_active_window('gts_window_screen', ['image/win_LOG_verify.png'], window_data[0], window_data[1])
                if image_detect(screenshot_path, 'image/databaseDC310_alternative_screen.png', fit_level=0.8, input_delay=1):
                    print("zrobione")
                    tab(1)
                    enter(1, 0.1)
                else:
                    print("Nie znaleziono okna, przerwano prace")
                    break
            elif len(window_data) > 1:
                print(len(window_data))
                print(window_data)
                print(f"Aplikacja GTS nie została uruchomiona prawidłowo!")
                description = ("\t -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!")
            elif not search_win_confirm and not search_win_alt_confirm and not app_started:
                app_started = False
                print(f"Aplikacja GTS nie została uruchomiona!")
                description = ("\t -> Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!")
        except:
            description = ("\t -> Wykryto ingerencje urzytkownika w trakcie działania programu!")
            print("wykrytio ruch myszy")


if __name__ == '__main__':
    #run_bot()
    control_listener = AutoControlObject()
    listener_thread = threading.Thread(target=control_listener.start_mouse_listener)
    listener_thread1 = threading.Thread(target=run_bot, args=(control_listener,))
    listener_thread.start()
    listener_thread1.start()
    listener_thread.join()
    listener_thread1.join()


















































    #     app_started = True
    #     description = "Aplikacja GTS została wykryta!"
    #     item_check_path = 'image/databaseDC310_alternative_screen.png'
    #     tab(2)
    #     up(29)
    #     down(22)
    #     # enter(1)
    #
    #     print(f"wysłane okno: {win32gui.GetWindowText(search_win_hwnd)} | {search_win_hwnd}")
    #     active_window = gw.getActiveWindow()
    #     print(
    #         f"{active_window} | hwnd_: {search_win_hwnd} | przek_: {win32gui.GetWindowText(search_win_hwnd)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
    #     # list_all_windows()
    #     # time.sleep(1)
    #     screenshot_active_window('gts_window_screen', 'image/win_LOG_verify.png', search_win_hwnd)
    #
    #     if image_detect(screenshot_path, item_check_path, fit_level=0.8, input_delay=1):
    #         print("zrobione")
    #         tab(1)
    #         enter(1)
    #         search_win_confirm_1, search_win_hwnd_1, search_win_alt_confirm_1 = search_app_by_partial_title(
    #             'GlobalTerminalSystem - Welcome', 5)
    #         if search_win_confirm_1:
    #             time.sleep(7)
    #             selected_key('-')
    #             put_text('RE2')
    #             enter(1, 0.5)
    #             search_win_confirm_2, search_win_hwnd_2, search_win_alt_confirm_2 = search_app_by_partial_title(
    #                 'GlobalTerminalSystem - RE2 - Change of notification/receipt', 5)
    #             if search_win_confirm_2:
    #                 # tab(7)
    #                 minus(2)
    #                 item_check_path = 'image/enter_receiptnumber.png'
    #                 screenshot_active_window('gts_window_screen', 'image/win_RT2_verify.png', search_win_hwnd_2)
    #                 if image_detect(screenshot_path, item_check_path):
    #                     backspace(1, 1)
    #
    #         else:
    #             print("Po próbie zalogowania nie możemy wykryć okna [GlobalTerminalSystem - Welcome]")
    #
    #     else:
    #         print("Nie znaleziono okna, przerwano prace")
    #         break
    #
    # # elif not search_win_confirm and not search_win_alt_confirm and not app_starting:
    # #     print(f"odpalanie app dla {search_win_confirm} and {search_win_alt_confirm}")
    # #     run_app(path_app)
    # #     app_starting = True
    # #     delay_time = 30
    # elif search_win_alt_confirm:
    #     app_started = True
    #     print(f"Znaleziono alternatywne okno: {search_win_hwnd}")
    #
    #     time.sleep(15)
    # elif not search_win_confirm and not search_win_alt_confirm and not app_started:
    #     app_started = False
    #     print(f"Aplikacja GTS nie została uruchomiona")
    #     description = ("\t -> Aplikacja GTS nie została uruchomiona przy poprzedniej próbie!")




































# while True:
#     a = main_menu(description)
#     if not a:
#         exit()
#     partial_title_win_app = 'GTS.AppStarter_DC78 - Global Terminal System'
#     partial_title_win_app_alt = ['GlobalTerminalSystem - ']
#     #partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'GTS.AppStarter_DC78 - Global Terminal System']
#     search_win_confirm, search_win_hwnd, search_win_alt_confirm = search_app_by_partial_title(partial_title_win_app, delay_time, partial_title_win_app_alt)
#
#     #list_all_windows()
#     # time.sleep(2)
#     # screenshot_active_window('gts_window_screen', search_win_hwnd)
#     screenshot_path = 'gts_window_screen.png'
#     # item_check_path = 'image/gts_DT310_win_login.png'
#     # while True:
#     #     if image_detect(screenshot_path, item_check_path, 1):
#     #         print("Gotowe do logowania")
#     #         break
#
#     if search_win_confirm:
#         app_started = True
#         description = "Aplikacja GTS została wykryta!"
#         item_check_path = 'image/databaseDC310_alternative_screen.png'
#         tab(2)
#         up(29)
#         down(22)
#         #enter(1)
#
#         print(f"wysłane okno: {win32gui.GetWindowText(search_win_hwnd)} | {search_win_hwnd}")
#         active_window = gw.getActiveWindow()
#         print(
#             f"{active_window} | hwnd_: {search_win_hwnd} | przek_: {win32gui.GetWindowText(search_win_hwnd)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
#         #list_all_windows()
#         #time.sleep(1)
#         screenshot_active_window('gts_window_screen', 'image/win_LOG_verify.png', search_win_hwnd)
#
#         if image_detect(screenshot_path, item_check_path, fit_level=0.8, input_delay=1):
#             print("zrobione")
#             tab(1)
#             enter(1)
#             search_win_confirm_1, search_win_hwnd_1, search_win_alt_confirm_1 = search_app_by_partial_title('GlobalTerminalSystem - Welcome', 5)
#             if search_win_confirm_1:
#                 time.sleep(7)
#                 selected_key('-')
#                 put_text('RE2')
#                 enter(1, 0.5)
#                 search_win_confirm_2, search_win_hwnd_2, search_win_alt_confirm_2 = search_app_by_partial_title('GlobalTerminalSystem - RE2 - Change of notification/receipt', 5)
#                 if search_win_confirm_2:
#                     # tab(7)
#                     minus(2)
#                     item_check_path = 'image/enter_receiptnumber.png'
#                     screenshot_active_window('gts_window_screen', 'image/win_RT2_verify.png', search_win_hwnd_2)
#                     if image_detect(screenshot_path, item_check_path):
#                         backspace(1, 1)
#
#             else:
#                 print("Po próbie zalogowania nie możemy wykryć okna [GlobalTerminalSystem - Welcome]")
#
#         else:
#             print("Nie znaleziono okna, przerwano prace")
#             break
#
#     # elif not search_win_confirm and not search_win_alt_confirm and not app_starting:
#     #     print(f"odpalanie app dla {search_win_confirm} and {search_win_alt_confirm}")
#     #     run_app(path_app)
#     #     app_starting = True
#     #     delay_time = 30
#     elif search_win_alt_confirm:
#         app_started = True
#         print(f"Znaleziono alternatywne okno: {search_win_hwnd}")
#         time.sleep(15)
#     elif not search_win_confirm and not search_win_alt_confirm and not app_started:
#         app_started = False
#         print(f"Aplikacja GTS nie została uruchomiona")
#         description = ("\t -> Aplikacja GTS nie została uruchomiona przy poprzedniej próbie!")
#
#
#
# time.sleep(30)
# partial_title_win_app = 'GlobalTerminalSystem - RE2 - Change of notification/receipt'
# partial_title_win_app_alt = 'GlobalTerminalSystem - '
# search_win_confirm, search_win_hwnd, search_win_alt_confirm = search_app_by_partial_title(partial_title_win_app, 3, partial_title_win_app_alt)
# if search_win_confirm:
#     print(f"Okno aplikacji zostało odnalezione i zmaxymalizowane dla [partial_title_win_app: {partial_title_win_app}]")
#     item_check_path = 'image/enter_receiptnumber.png'
#     screenshot_active_window('gts_window_screen', search_win_hwnd)
#     if image_detect(screenshot_path, item_check_path):
#         backspace(1, 1)
#         print(f"Odnaleziono [item_check_path: {item_check_path}] w obrębie [screenshot_path: {screenshot_path}]")
#         time.sleep(10)
#     else:
#         print(f"Nie odnaleziono [item_check_path: {item_check_path}] w obrębie [screenshot_path: {screenshot_path}]")
#         time.sleep(10)
# elif search_win_alt_confirm:
#     print(f"Okno aplikacji NIE zostało odnalezione dla [partial_title_win_app: {partial_title_win_app}] "
#           f"ale mamy alternatywne okno [partial_title_win_app_alt: {partial_title_win_app_alt}]")
#     time.sleep(10)
# else:
#     print(f"Żadne pokrewne okno zalogowanej aplikacji NIE odnaleziono w tym [partial_title_win_app: {partial_title_win_app}, "
#           f"partial_title_win_app_alt: {partial_title_win_app_alt}]"
#           f"Teraz wyszukiwanie okna logowania")
#     time.sleep(10)









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

