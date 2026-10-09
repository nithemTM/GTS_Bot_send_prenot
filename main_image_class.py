import win32gui
import pygetwindow as gw
import logging
from help_function.menu_function import main_menu
from help_function.window_titles import enum_window_titles, search_app, path_get_target, run_app, enum_window_titles_1, wait_window, all_window
from help_function.win32_library import search_app_by_partial_title, find_window_stos_callback, list_all_windows, close_window_callback, app_window_qty_callback, find_window, enum_child_windows, location, pobierz, get_button_info_on_hover1, get_button_info_on_hover, print_class_name_on_hover
from help_function.win32_object import WinAppObjectSearch
from help_function.image_detect import image_detect
from help_function.screen_making import screenshot_active_window
from help_function.controller_automate import tab, down, up, enter, selected_key, send_mute_key, volume_set, bot_speaking, put_text, backspace, f10, ctrl_q, copy, home, escape, on_move
from help_function.process_os import is_application_running, get_application_processes
from help_function.controller_auto_object import AutoControlObject
from help_function.excel_object import ExcelDataObject

# is_application_running('wfica32.exe')
#get_application_processes()
#time.sleep(30)
# _, found_pid = win32process.GetWindowThreadProcessId(search_win_hwnd)
# print("wypisz")
# print(found_pid)
# time.sleep(20)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def run_bot1():

    logging.info("Aplikacja uruchomiona w funkcji [run_bot]")

    path_tr_file = "C:\\Users\\matok4\\PycharmProjects\\Send_Prenot_Bot_GTS - class\\"

    tr_excel_info = ExcelDataObject('Transit week 39  19.09.xlsx', path_tr_file, 0, 'A:F', 8)
    path_app_shortcut = "C:\\Users\\matok4\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\GTSGUI_DC78^.lnk"
    window_title = "Consafe Logistics - Astro WMS -  Jarosty DC CDC 310 004 Linux PROD  (M2_Jarosty-DSPL310-NB0066.awc)"
    path_app = path_get_target(path_app_shortcut)

    app_started = False
    tasks_ended = False
    excel_error = False
    description = None
    app_status = 'NIEAKTYWNA'
    several_window = 0
    index_loop = None
    total_index_records = None
    index_receipt_loop = None
    data_frame_query_response = None

    while True:
        #send_mute_key()
        volume_set(10)
        bot_speaking("Bot was started")

        partial_title_win_app = 'GlobalTerminalSystem - RT2 - Registration of OPDC/transitrecei'
        # partial_title_win_app_alt = 'GlobalTerminalSystem - '
        #partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'AppStarter']
        partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'GTS.AppStarter_DC78 - Global Terminal System']
        title_not_responding = " GlobalTerminalSystem - RE2 - Change of notification/receipt (N - \\\\Remote"
        win_app_gts310 = WinAppObjectSearch(partial_title_win_app, partial_title_win_app_alt)

        partial_title = ['Terminal', 'GTS GUI']
        win32gui.EnumWindows(win_app_gts310.find_window_stos_callback_class, partial_title)
        if not win_app_gts310.status_demanded_app:
            app_status = 'NIEAKTYWNA'
            if description is None:
                description = 'Uruchom aplikacje GTS_DC78'
        elif win_app_gts310.status_demanded_app:
            app_status = 'AKTYWNA'
        if win_app_gts310.value_of_same_window_app > 1:
            description = "Apkikacja GTS aktywna ze zbyt wieloma oknami bądź uruchomiona podwójnie, może byc uruchomione tylko jedno okno!!"
        if description is None:
            description = 'Brak dostępnych uwag!'
        if not app_started or win_app_gts310.value_of_same_window_app > 1 or tasks_ended or excel_error:
            a = main_menu(app_status, description)

            if not a:
                break
            else:
                header_name_column = ['Data & Godz. Rozł.', 'BOT_TASK', 'Shp Id', 'RCTNo', 'INFO_BOT', 'UWAGI']
                file_excel_permission, description = tr_excel_info.checking_file_form(header_name_column)
                if not file_excel_permission:
                    excel_error = True
                    continue
                else:
                    excel_error = False
                tr_excel_info.load_data()
                query_1 = 'BOT_TASK == "WRZUCIĆ"'
                query = 'BOT_TASK == "WRZUCIĆ" and INFO_BOT != "DONE" and INFO_BOT != "PRZEBUKOWANY" and INFO_BOT != "SKASOWANY"'
                data_frame_query_response_1 = tr_excel_info.filter_data_query(query_1)
                data_frame_query_response = tr_excel_info.filter_data_query(query)
                index_loop = 0
                tasks_ended = False
                total_index_records_1 = len(data_frame_query_response_1)
                total_index_records = len(data_frame_query_response)
                if total_index_records_1 == 0:
                    logging.info('Nie zaznaczono w pliku partii CSMów na których ma być wykonany "Send Prenot"! -> Proszę o zaznaczenie w kolumnie "BOT_TASK"')
                    description = 'Nie zaznaczono w pliku partii CSMów na których ma być wykonany "Send Prenot"! -> Proszę o zaznaczenie w kolumnie "BOT_TASK"'
                    tasks_ended = True
                    continue
                elif total_index_records == 0:
                    #print('\nBrak Receipt na których maja zostać wykonany "Send Prenot" -> prawdopodobnie nie zostały zaznaczone w pliku!')
                    logging.info('Brak Receipt na których maja zostać wykonany "Send Prenot" -> Wszystkie zaznaczone są już wrzucone i zweryfikowane!')
                    description = 'Brak Receipt na których maja zostać wykonany "Send Prenot" -> Wszystkie zaznaczone są już wrzucone i zweryfikowane!'
                    tasks_ended = True
                    continue
        # while win_app_gts310.hwnd_app_win_active is None and len(win_app_gts310.table_window_object) < 2:
        #     win32gui.EnumWindows(win_app_gts310.find_windows_callback_class, None)
        #     if not win_app_gts310.search_app_by_partial_title_class(3):
        #         break
        # if not win_app_gts310.search_app_by_partial_title_class(3):
        #     continue
        win_app_gts310.search_app_by_partial_title_class(3)
        win_app_gts310.bring_window_to_front_class(5)
        # list_all_windows()

        screenshot_path = 'gts_window_screen.png'
        screenshot_path_error = 'error_process_active_win.png'

        logging.info(f'Dane pobrane z pliku excel: [{tr_excel_info.data_file_filter_query}]')
        if win_app_gts310.confirm:
            app_started = True
            description = "Status Aplikacji GTS DC310: [ AKTYWNA ]"
            value_next_loop_error = 0
            while index_loop < total_index_records and win_app_gts310.hwnd_app_win_active == win32gui.GetForegroundWindow() and win_app_gts310.title_app_win_active == win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active):

                print("\n######################")
                logging.info(f"window_data_info->{win_app_gts310.hwnd_app_win_active} : {win32gui.GetForegroundWindow()} | {win_app_gts310.title_app_win_active} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                print("######################")

                f10(1, 0.1)
                ctrl_q(2, 0.1)

                confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path, 'image/win_RT2_verify.png', fit_level=0.8, input_delay=1):
                    backspace(1, 0.1)
                    # TODO: jakikolwiek False zostanie wyrzucony mozna ten csm sprobowac jeszcze raz przepuscic,
                    #  jezeli za drugim razem nie zostanie poprawnie wprowadzony to znaczy ze w GTS pojawia sie problem z jego wrzuceniem
                    # TODO: tutaj bedzie potrzebny wrzucenie juz wspoldziałanie z plikiem excel

                    text_valid = tr_excel_info.data_file_filter_query.iloc[index_loop]['RCTNo']
                    logging.info(f"Receipt Number do przetworzenia: {text_valid}")
                    valid_receipt = False
                    try:
                        text_valid = int(float(text_valid))
                        if len(str(text_valid)) != 9:
                            valid_receipt = True
                            logging.info(f'Brak poprawnego Receipt! Sprawdz! Podany w programie: {text_valid}')
                            # TODO: uzupełnic wartości w pliku excel tranzytowym
                            #continue
                            #break
                    except ValueError as e:
                        valid_receipt = True
                        logging.error(f'Konwersja na liczbę nieudana! Prawdopodobnie nie jest podany prawidłowy Receipt! [text_valid: {text_valid} | type: {type(text_valid)}]'
                                      f'\n Error: {e}')
                        # TODO: uzupełnic wartości w pliku excel tranzytowym
                        #break
                        #continue
                    finally:
                        if valid_receipt:
                            name_col_save = ["UWAGI"]
                            index_edit_row_real = tr_excel_info.data_file_filter_query.index[index_loop]
                            tr_excel_info.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Uzupełnij/Popraw Receipt"
                            tr_excel_info.save_data_single_line(index_loop, name_col_save)
                            index_loop += 1
                            continue
                    logging.info('Walidacja numeru Receipt przebiegła pomyślnie!')
                    put_text(text_valid)
                    clipboard_content, confirm_valid_clipboard = copy(1, str(text_valid))
                    if not confirm_valid_clipboard or clipboard_content is None:
                        logging.info('Nie skopiowano prawidłowo wartości do pamięci podręcznej! Nastąpi ponowne przetworzenie ostatniego Receipt!')
                        # TODO: mozna tutaj dodac funkcje robiaca scrina aktywnego okna zeby sprawdzic co sie wydarzyło,
                        #  dodatkowo skopiowac to co było w schowku i razem z wartoscia ktora powinna sie tam znalezc umiescic w logach
                        #  dodatkowo trzeba dac tutaj 2x powtórzenie żeby jeszcze raz spróbowało wrzucic ten recipt number dopiero jezeli nie to info do excela
                        #continue
                        break
                    confirm_screenshot_active, type_of_confirmation, path_confirm = win_app_gts310.screenshot_active_window_class('gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'])
                    # confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                    if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path,'image/win_RT2_verify.png', fit_level=0.8, input_delay=1):
                        home(1, 0.1)
                        confirm_screenshot_active, type_of_confirmation, path_confirm = win_app_gts310.screenshot_active_window_class('gts_window_screen', ['image/win_STATUS_1_verify.png', 'image/win_STATUS_0_verify.png', 'image/win_STATUS_3_verify.png', 'image/win_STATUS_4_verify.png'])
                        #confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_STATUS_1_verify.png', 'image/win_STATUS_0_verify.png', 'image/win_STATUS_3_verify.png', 'image/win_STATUS_4_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                        logging.info(f"Dane po zrobieniu screena -> confirm_screenshot_active: [{confirm_screenshot_active}], type_of_confirmation: [{type_of_confirmation}], path_confirm: [{path_confirm}]")
                        if confirm_screenshot_active and type_of_confirmation == 1:
                            status_receipt = tr_excel_info.data_file_filter_query.iloc[index_loop]['INFO_BOT']
                            if status_receipt == 'STATUS 0':
                                column_to_excel_uwagi = None
                                if 'STATUS_1' in path_confirm:
                                    column_to_excel_uwagi = 'Nowy Status-> 1'
                                if 'STATUS_3' in path_confirm:
                                    column_to_excel_uwagi = 'Nowy Status-> 3'
                                if 'STATUS_4' in path_confirm:
                                    column_to_excel_uwagi = 'Nowy Status-> 4'
                                if column_to_excel_uwagi is not None:
                                    name_col_save = ["UWAGI"]
                                    index_edit_row_real = tr_excel_info.data_file_filter_query.index[index_loop]
                                    tr_excel_info.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                                    tr_excel_info.save_data_single_line(index_loop, name_col_save)
                                logging.info(f'Dane odświeżone dla wpisu "STATUS 0" -> [column_to_excel_uwagi: {column_to_excel_uwagi}]')

                            elif 'STATUS_1' in path_confirm:
                                confirm_screenshot_active, type_of_confirmation, path_confirm = win_app_gts310.screenshot_active_window_class('gts_window_screen', ['image/win_MenuChoice_registration_verify.png'])
                                #confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_MenuChoice_registration_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                if confirm_screenshot_active and type_of_confirmation == 1 and 'MenuChoice_registration' in path_confirm: #image_detect(screenshot_path, 'image/win_MenuChoice_registration_verify.png', fit_level=0.8, input_delay=1):
                                    put_text('1', 0.1)
                                    enter(1, 0.1)
                                    confirm_screenshot_active, type_of_confirmation, path_confirm = win_app_gts310.screenshot_active_window_class('gts_window_screen', ['image/win_RT2_EnterSenddatePrenot_verify.png'])
                                    #confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_RT2_EnterSenddatePrenot_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                    if confirm_screenshot_active and type_of_confirmation == 1 and 'RT2_EnterSenddatePrenot' in path_confirm:
                                        confirm_screenshot_active, type_of_confirmation, path_confirm = win_app_gts310.screenshot_active_window_class('gts_window_screen', ['image/win_SendPrenotBtn_verify.png', 'image/win_DeletePrenotBtn_verify.png', 'image/win_LackPrenotBtn_verify.png'])
                                        #confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_SendPrenotBtn_verify.png', 'image/win_DeletePrenotBtn_verify.png', 'image/win_LackPrenotBtn_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                        column_to_excel_uwagi = None
                                        column_to_excel_info_bot = None
                                        if confirm_screenshot_active and type_of_confirmation == 1 and 'SendPrenotBtn_' in path_confirm:
                                            # TODO: tutaj będzie można dalej pociągnąć temat kliknięc SEND PRENOT + wszelkie BŁĘDY
                                            logging.info('Możemy clikac "Send Prenot to WMS')
                                            column_to_excel_uwagi = "Send Prenot"
                                            column_to_excel_info_bot = "DONE"
                                        elif confirm_screenshot_active and type_of_confirmation == 1 and 'DeletePrenotBtn_' in path_confirm:
                                            # TODO: tutaj co w przypadku jeżeli otrzymamy DELET PRENOT
                                            logging.info('Mamy "Delate Prenot to WMS"!')
                                            column_to_excel_uwagi = "Delate Prenot"
                                            column_to_excel_info_bot = "DONE"
                                        elif confirm_screenshot_active and type_of_confirmation == 1 and 'LackPrenotBtn_' in path_confirm:
                                            # TODO: tutaj co w przypadku jeżeli otrzymamy brak przycisku
                                            logging.info('Brak przycisku do wysyłki zamówień tranzytowych! Prawdopodobnie nie jest to tranzyt! brak przycisku')
                                            column_to_excel_uwagi = "Receipt bez TR"
                                        else:
                                            logging.info('Prawdopodobnie błąd który powinien sie pokazać w nastepnej linijce kodu!')
                                        if column_to_excel_uwagi is not None or column_to_excel_info_bot is not None:
                                            name_col_save = ["INFO_BOT", "UWAGI"]
                                            index_edit_row_real = tr_excel_info.data_file_filter_query.index[index_loop]
                                            if column_to_excel_uwagi is not None:
                                                tr_excel_info.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                                            if column_to_excel_info_bot is not None:
                                                tr_excel_info.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = column_to_excel_info_bot
                                            tr_excel_info.save_data_single_line(index_loop, name_col_save)
                                        logging.info(f'Dane odświeżone dla wpisu "STATUS 1" -> [column_to_excel_uwagi: {column_to_excel_uwagi}] | [column_to_excel_info_bot: {column_to_excel_info_bot}]')
                            elif 'STATUS_0' in path_confirm:
                                name_col_save = ["INFO_BOT", "UWAGI"]
                                index_edit_row_real = tr_excel_info.data_file_filter_query.index[index_loop]
                                tr_excel_info.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Status 0"
                                tr_excel_info.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = "STATUS 0"
                                tr_excel_info.save_data_single_line(index_loop, name_col_save)
                                logging.info(f'Wystąpił STATUS 0 -> do odnotowania w pliku')
                            elif ('STATUS_4' in path_confirm or 'STATUS_3' in path_confirm):
                                logging.info(f'Wystąpił STATUS 3 lub 4 tego transportu - > Został już wprowadzony!')
                                name_col_save = ["INFO_BOT", "UWAGI"]
                                index_edit_row_real = tr_excel_info.data_file_filter_query.index[index_loop]
                                tr_excel_info.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Status 3 lub 4"
                                tr_excel_info.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = "DONE"
                                tr_excel_info.save_data_single_line(index_loop, name_col_save)
                        # elif confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path, 'image/win_CommonTransport_verify.png', fit_level=0.8, input_delay=1):
                        #     print("Nie jest to tranzytowy Receipt!")
                        #     continue

                            # TODO: do oznakowania jako 'do sprawdzenia' w excel, później można dodać opcję sprawdzania błędów, tablice która przeleci po wszystkich scrinach z błędami i sprawdzi czy to błąd i wypisze go w logach
                            #  w osobnym folderze trzeba zrobić możliwosc zapisywania zrzutów aplikacji jeżeli wystąpi problem, wtedy poznamy wszystkie błędy jakie są dostepne
                            # TODO: Niezbedne bedzie tez wypisanie w logach dodatkowych informacji o tym co było szukane itd.
                if not confirm_screenshot_active and type_of_confirmation == 1:
                    # TODO: jezeli bład powtórzy sie dwa razy z rzedu a nie jest on błędem z podwójnym oknem(trzeba to wykluczyć)
                    #  tylko błędem wartości bądz innym wyświetlanym tylko na dole okna wtedy pomijamy go, i zaznaczamy w pliku dla USERA
                    column_to_excel_uwagi = ''
                    value_next_loop_error += 1
                    #TODO: potrzebna jest tablica z błędami po której bedzie zapętlanie i sprawdzanie wszystkich dostepnych ich opisów.
                    if image_detect(screenshot_path_error, 'error_image_patterns/win_ALL_NightLogOut_error.png', fit_level=0.8, input_delay=2) and value_next_loop_error <= 2:
                        logging.info('Znaleziony błąd: ALL_NightLogOut_error -> przeloguj GTS! -> Nastąpiło nocne wylogowanie aplikacji')
                        app_started = False
                        description = "Nastąpiło nocne wylogowanie aplikacji -> Uruchom ponownie GTS DC310"
                        break
                    elif image_detect(screenshot_path_error, 'error_image_patterns/win_RT2_QueryCausedNoRecords_error.png', fit_level=0.8, input_delay=2) and value_next_loop_error <= 2:
                        logging.info('Znaleziony błąd: RT2_QueryCausedNoRecords')
                        column_to_excel_uwagi = "Brak Receipt w GTS"
                    elif value_next_loop_error <= 2:
                        column_to_excel_uwagi = "Nieznany Błąd"
                        logging.info(f'Nieznany błąd programu na tym samy Receipt wystąpił 2 raz -> spróbuj odszukać PrintScreen dla tego błędu z podanej wcześniej ścieżki. Wpis do pliku: {column_to_excel_uwagi}')
                    if value_next_loop_error < 2:
                        logging.info('Problem z Receipt -> pierwsza próba!')
                        continue
                    else:
                        name_col_save = ["UWAGI"]
                        index_edit_row_real = tr_excel_info.data_file_filter_query.index[index_loop]
                        tr_excel_info.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                        tr_excel_info.save_data_single_line(index_loop, name_col_save)
                        value_next_loop_error = 0

                    #continue

                if not confirm_screenshot_active and type_of_confirmation == 2:
                    logging.info("Wykryto zmianę okno podczas działania programu -> Nastąpi wznowienie ostatniego procesu aby odnaleźć prawidłowe okno jeżeli istnieje!")
                    # TODO: trzeba równiez dać max 2 razy dla sprawdzenia a później pominiecie i wpisanie do pliku excel
                    #continue
                    break
                logging.info(f'Index teraz zrobionego Recipte: {index_loop}')
                index_loop += 1
                logging.info(f'Index następnego Recipte do zrobienia: {index_loop}')
                print("######################")
                logging.info(f"Prównanie danych okna żądanego | systemowego -> {win_app_gts310.hwnd_app_win_active} : {win32gui.GetForegroundWindow()} | {win_app_gts310.title_app_win_active} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                print("######################")
            # Bot wykrył inne okno badź zakończył pracę z wrzucaniem prenotów
            else:
                if win_app_gts310.hwnd_app_win_active != win32gui.GetForegroundWindow() or win_app_gts310.title_app_win_active != win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active):
                    logging.info(f"Wymagane okno [{win_app_gts310.hwnd_app_win_active} : {win_app_gts310.title_app_win_active}] <-> Aktywne okno [{win32gui.GetForegroundWindow()} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}]"
                                 f"\nZakonczono dzialanie petli! Przyczyna -> nieprawidlowe okno -> Program wznowi pracę powtarzając cały ostatni proces!")
                    if index_loop > 0:
                        index_loop -= 1
                    # TODO: trzeba równiez dać max 2 razy dla sprawdzenia a później pominiecie i wpisanie do pliku excel
                elif index_loop >= total_index_records:
                    logging.info("Zakonczono dzialanie petli! Przyczyna -> Zakończono wrzucanie PRENOT-ów")
                    # TODO: tutaj można dodać statystyki wrzuconych prenotów z exportem do pliku tekstowego!
                    description = "Zakończono wrzucanie partii ReceiptNo!"
                    tasks_ended = True
                    f10(1, 0.1)


                # TODO: trzeba doprecyzowac jaka przyczyna wywalenia pętli tutaj bedzie można wkleić wartosc receiptno i dalsze kroki.

            input_menu = int(input(">> "))
            # os.system('cls')
            if input_menu == 1:
                continue
            else:
                break
        elif win_app_gts310.confirm_alt and 'GTS.AppStarter_DC78 - Global Terminal System' not in win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active):
            app_started = True
            logging.info(f"Znaleziono alternatywne okno: {win_app_gts310.hwnd_app_win_active} | {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)}")
            f10(1, 0.1)
            ctrl_q(1, 0.1)
            put_text('RT2')
            enter(1, 0.1)

        elif win_app_gts310.confirm_alt and 'GTS.AppStarter_DC78 - Global Terminal System' in win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active):
            app_started = True
            logging.info(f"Znaleziono alternatywne okno logowania: {win_app_gts310.hwnd_app_win_active} | {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)}")
            confirm_screenshot_active, type_of_confirmation, path_confirm = win_app_gts310.screenshot_active_window_class('gts_window_screen', ['image/win_LOG_verify.png'])
            if confirm_screenshot_active and type_of_confirmation == 1:
                tab(2)
                up(29)
                down(22)
                active_window = gw.getActiveWindow()
                logging.info(f"Dane okna przed zrobieniem screena: {active_window} | hwnd_: {win_app_gts310.hwnd_app_win_active} | przek_: {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
                # list_all_windows()
                # time.sleep(1)

                # screenshot_active_window('gts_window_screen', ['image/win_LOG_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                if image_detect(screenshot_path, 'image/databaseDC310_alternative_screen.png', fit_level=0.8, input_delay=1):
                    logging.info(f"Wykryto okno po kontrolce [image/databaseDC310_alternative_screen.png]")
                    tab(1)
                    enter(1, 0.1)
                    #TODO: tutaj program stwierdza że uruchamia logowanie -> tak więc należy zaraz zweryfikowac czy jestesmy gotowi do wrzucania prenotów
                else:
                    logging.info("Nie ustawiono prawidłowo departamentu jako DC310 bądź nie wykryto już okna")
                    break
            elif not confirm_screenshot_active:
                logging.info("Nie zrobiono screenshota okna logowania - być może w trakcie zostało zmienione na inne!")
                break
        elif len(win_app_gts310.table_window_object) > 1:
            logging.info(f"Aplikacja GTS nie została uruchomiona prawidłowo! -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!"
                         f"\n Ilość otworzonych okien: {len(win_app_gts310.table_window_object)}"
                         f"\n Dane okien w słowniku: {win_app_gts310.table_window_object}")
            description = ("\t -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!")
        elif not win_app_gts310.confirm and not win_app_gts310.confirm_alt and not app_started:
            app_started = False
            description = "Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!"
            logging.info("Aplikacja GTS nie została uruchomiona! -> Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!")


def run_bot():
    path_tr_file = "C:\\Users\\matok4\\PycharmProjects\\Send_Prenot_Bot_GTS - fun\\"
    tr_excel_info = ExcelDataObject('Transit week 39  19.09.xlsx', path_tr_file, 0, 'A:F', 8)
    tr_excel_info.load_data(0, 'A:F', 8)
    #a = tr_excel_info.filter_data('BOT', 'WRZUCIĆ')
    query = 'BOT_TASK == "WRZUCIĆ" and INFO_BOT != "DONE" and INFO_BOT != "PRZEBUKOWANY" and INFO_BOT != "SKASOWANY" and  INFO_BOT != "STATUS 0"'
    tr_excel_info.filter_data_query(query)
    print(tr_excel_info.data_file_origin)
    index = len(tr_excel_info.data_file_filter_query) - 1
    while index >= 0:
        text_valid = tr_excel_info.data_file_filter_query.iloc[index]['RCTNo']
        try:
            text_valid = int(float(text_valid))
            if len(str(text_valid)) != 9:
                print("Brak poprawnego Receipt! Sprawdz!")
        except ValueError:
            print("Konwersja na liczbę nieudana! Prawdopodobnie nie jest podany prawidłowy Receipt")

        print(text_valid)
        index -= 1
    #print(tr_excel_info.list_file_data)
    #print(tr_excel_info.data_file_origin)


if __name__ == '__main__':
    run_bot1()



