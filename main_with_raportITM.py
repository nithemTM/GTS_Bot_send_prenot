import time
import win32gui
import pygetwindow as gw
import logging
import json
from functools import partial
from help_function.automate_browser_driver import open_link_web_browser_chrome_driver, close_web_browser_process_chromedriver, downloading_check, get_latest_file, move_download_file
from help_function.menu_function import main_menu, menu_continue
from help_function.window_titles import enum_window_titles, search_app, path_get_target, run_app, enum_window_titles_1, wait_window, all_window
from help_function.win32_library import search_app_by_partial_title, find_window_stos_callback, list_all_windows, close_window_callback, app_window_qty_callback, find_window, enum_child_windows, location, pobierz, get_button_info_on_hover1, get_button_info_on_hover, print_class_name_on_hover
from help_function.win32_object import WinAppObjectSearch
from help_function.image_detect import image_detect
from help_function.screen_making import screenshot_active_window
from help_function.controller_automate import tab, down, up, enter, selected_key, send_mute_key, volume_set, bot_speaking, put_text, backspace, f10, ctrl_q, copy, home, escape, on_move, username_get
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
    path_cognos_rep = "\\\\DSPL310-FS0001.ikea.com\\Common_A\\FM_Astro SU\\Programy_FM\\raport\\"
    
    excel_transit_week = ExcelDataObject('Transit week 39  19.09.xlsx', path_tr_file, 0, 'A:F', 8)
    excel_receipt_cognos = ExcelDataObject('Suma Receipt.xlsx', path_cognos_rep, 0, 'A:E', 1)
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
    in_process = False
    starting_app = False
    total_index_records_tr = None
    index_receipt_loop = None
    data_frame_query_response_tr = None

    while True:
        #send_mute_key()
        volume_set(10)
        #bot_speaking("Bot was started")

        partial_title_win_app = 'GlobalTerminalSystem - RT2 - Registration of OPDC/transitrecei'
        # partial_title_win_app_alt = 'GlobalTerminalSystem - '
        partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'AppStarter']
        #partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'GTS.AppStarter_DC78 - Global Terminal System']
        title_not_responding = " GlobalTerminalSystem - RE2 - Change of notification/receipt (N - \\\\Remote"
        win_app_gts310 = WinAppObjectSearch(partial_title_win_app, partial_title_win_app_alt)

        partial_title_tab = ['Terminal']
        win32gui.EnumWindows(win_app_gts310.find_window_stos_callback_class, partial_title_tab)
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
        if not app_started or win_app_gts310.value_of_same_window_app >= 1 or tasks_ended or excel_error:
            if not in_process:
                a = main_menu(app_status, description)

                if not a:
                    break
                else:
                    header_column_transit_week = ['Data & Godz. Rozł.', 'BOT_TASK', 'Shp Id', 'RCTNo', 'INFO_BOT', 'UWAGI']
                    excel_transit_permission, description = excel_transit_week.checking_file_form(header_column_transit_week)
                    if not excel_transit_permission:
                        excel_error = True
                        continue
                    else:
                        excel_error = False
                    header_column_report = ['RCTShpNo', 'RCTNo', 'Data Item2', 'RCTStat', 'RCTSubType']
                    excel_report_permission, description = excel_receipt_cognos.checking_file_form(header_column_report)
                    if not excel_report_permission:
                        excel_error = True
                        continue
                    else:
                        excel_error = False

                    excel_transit_week.load_data()
                    query_transit_valid = 'BOT_TASK == "WRZUCIĆ"'
                    query = 'BOT_TASK == "WRZUCIĆ" and INFO_BOT != "DONE" and INFO_BOT != "PRZEBUKOWANY" and INFO_BOT != "SKASOWANY"'
                    data_frame_query_response_tr_valid = excel_transit_week.filter_data_query(query_transit_valid)
                    data_frame_query_response_tr = excel_transit_week.filter_data_query(query)
                    index_loop = 0
                    #total_index_records_tr_valid = len(data_frame_query_response_tr_valid)
                    print(data_frame_query_response_tr_valid)

                    if data_frame_query_response_tr_valid is None or data_frame_query_response_tr_valid.empty:
                        total_index_records_tr = 0
                        logging.info('Nie zaznaczono w pliku partii CSMów na których ma być wykonany "Send Prenot"! -> Proszę o zaznaczenie w kolumnie "BOT_TASK"')
                        description = 'Nie zaznaczono w pliku partii CSMów na których ma być wykonany "Send Prenot"! -> Proszę o zaznaczenie w kolumnie "BOT_TASK"'
                        tasks_ended = True
                        continue
                    elif data_frame_query_response_tr is None or data_frame_query_response_tr.empty:
                        total_index_records_tr = 0
                        logging.info('Brak Receipt na których maja zostać wykonany "Send Prenot"!')
                        description = 'Brak Receipt na których maja zostać wykonany "Send Prenot"!'
                        tasks_ended = True
                        continue
                    else:
                        total_index_records_tr = len(data_frame_query_response_tr)
                        # with open("data.json", "r") as file:
                        #     browser_data = json.load(file)
                        folder_path_target = r"\\DSPL310-FS0001.ikea.com\Common_A\FM_Astro SU\Programy_FM\raport"
                        url_web = "https://cognosanalytics.apps.ikea.com/ibmcognos/bi/?perspective=authoring&id=i636125E1AFD0473CA710794598F96CCC&objRef=i636125E1AFD0473CA710794598F96CCC&action=run&format=spreadsheetML&cmPropStr=%7B%22id%22%3A%22i636125E1AFD0473CA710794598F96CCC%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%22Suma%20Receipt%20w%20Ship%20v2%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D"
                        file_download_path = r"C:\Users\NAZWA_UŻYTKOWNIKA\Downloads\\"
                        user_login = username_get()
                        # callback_downloading_check = partial(downloading_check, file_name="Suma Receipt w Ship",
                        #                                      folder_name=file_download_path,
                        #                                      user_name=user_login)

                        # TODO: Tutaj ma sie wykonać pobranie raportu z Cognosa
                        #  następnie przeniesienie całej jego zawartości z pobranego pliku do pliku w folderze
                        #  nastepnie usuniecie pobranego pliku (żeby zabezpieczyć plik z podaną nazwa przed pomyłką, chyba że uda się zrobić to z wyszukaniem plku o najświeższej dacie)
                        #  nastepnie pobranie danych do formatu DataFrame aby można było z nich korzystać w trakcie działania programu.
                        in_process = True
                        tasks_ended = False
                        starting_app = True
                        browser = "edge"
                        latest_file = None
                        latest_data_reg = None


                        # while True:
                        #     try:
                        #         browser_name_menu = int(
                        #             input("Z jakiej przeglądarki korzystasz? [ 1 - MS Edge / 2 - Chrome ] > "))
                        #         if browser_name_menu == 1:
                        #             browser = "edge"
                        #         else:
                        #             browser = "chrome"
                        #     except:
                        #         print("Wprowadzono błędną wartość. Uruchamiam domyślnie w MD Edge")
                        #     latest_file, latest_data_reg = get_latest_file(file_name_pattern="Suma Receipt w Ship",
                        #                                                    folder_path=file_download_path,
                        #                                                    user_name=user_login)
                        #     browser_process = open_link_web_browser_chrome_driver(url_web, browser_data[browser],
                        #                                                           user_name=user_login)
                        #     if browser_process is not None:
                        #         break
                        # confirm_download, name_file_download = downloading_check(
                        #                                                     file_name_pattern="Suma Receipt w Ship",
                        #                                                     folder_path=file_download_path,
                        #                                                     user_name=user_login,
                        #                                                     latest_file=latest_file,
                        #                                                     latest_data_reg=latest_data_reg,
                        #                                                     timeout=20,
                        #                                                     callback_get_latest_file=get_latest_file)
                        # move_download_file(folder_path_source=file_download_path,
                        #                    filename=name_file_download,
                        #                    user_name=user_login,
                        #                    folder_path_target=folder_path_target)
                        # close_web_browser_process_chromedriver(browser_process)

                        excel_receipt_cognos.load_data()

                        # time.sleep(5)
                        # break
            elif in_process and starting_app:
                a = menu_continue(app_status, description)

                if a == 0:
                    break
                elif a == 2:
                    description = "Przerwano wrzucanie prenotów!"
                    logging.info(
                        f'Przerwanie wrzucania prenotów na [index_loop: {index_loop}]'
                    )
                    in_process = False
                    tasks_ended = True
                    continue
                else:
                    starting_app = True
                    logging.info(
                        f'Wznowiono wrzucanie prenotów od [index_loop: {index_loop}]')
            elif in_process and not starting_app:
                starting_app = True
                logging.info('Kontynuacja procesu!')

        # while win_app_gts310.hwnd_app_win_active is None and len(win_app_gts310.table_window_object) < 2:
        #     win32gui.EnumWindows(win_app_gts310.find_windows_callback_class, None)
        #     if not win_app_gts310.search_app_by_partial_title_class(3):
        #         break
        # if not win_app_gts310.search_app_by_partial_title_class(3):
        #     continue
        print(f"tablica okien: {win_app_gts310.table_window_object}")
        win_app_gts310.search_app_by_partial_title_class(3)
        win_app_gts310.bring_window_to_front_class(5)
        # list_all_windows()

        screenshot_path = 'gts_window_screen.png'
        screenshot_path_error = 'error_process_active_win.png'

        logging.info(f'Dane pobrane z pliku excel_transit_week: [{excel_transit_week.data_file_filter_query}]')
        logging.info(f'win_app_gts310.confirm: {win_app_gts310.confirm}')
        if win_app_gts310.confirm:
            app_started = True # TODO: zmienna do sprawdzenia TERAZ -> DONE
            # description = "Status Aplikacji GTS DC310: [ AKTYWNA ]"
            value_next_loop_error = 0
            while index_loop < total_index_records_tr and win_app_gts310.hwnd_app_win_active == win32gui.GetForegroundWindow() and win_app_gts310.title_app_win_active == win32gui.GetWindowText(win32gui.GetForegroundWindow()):

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
                    # TODO: tutaj bedzie potrzebny wrzucenie juz wspoldziałanie z plikiem excel -> DONE

                    text_valid = excel_transit_week.data_file_filter_query.iloc[index_loop]['RCTNo']
                    logging.info(f"Receipt Number do przetworzenia: {text_valid}")
                    fail_valid_receipt = False

                    if "elect" in str(text_valid).lower():
                        logging.error(f'Elektrolux - Wrzucić ręcznie! [text_valid: {text_valid} | type: {type(text_valid)}]')
                        name_col_save = ["UWAGI"]
                        index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                        excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Elektrolux/Wprowadź ręcznie"
                        excel_transit_week.save_data_single_line(index_loop, name_col_save)
                        index_loop += 1
                        continue
                    try:
                        text_valid = int(float(text_valid))
                        if len(str(text_valid)) != 9:
                            fail_valid_receipt = True
                            logging.info(f'Brak poprawnego Receipt! Sprawdz! Podany w programie: {text_valid}')
                            # TODO: uzupełnic wartości w pliku excel tranzytowym -> DONE
                            #continue
                            #break
                    except ValueError as e:
                        fail_valid_receipt = True
                        logging.error(f'Konwersja na liczbę nieudana! Prawdopodobnie nie jest podany prawidłowy Receipt! [text_valid: {text_valid} | type: {type(text_valid)}]'
                                      f'\n Error: {e}')
                        # TODO: uzupełnic wartości w pliku excel tranzytowym -> DONE
                        #break
                        #continue
                    finally:
                        if fail_valid_receipt:
                            name_col_save = ["UWAGI"]
                            index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                            excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Uzupełnij/Popraw Receipt"
                            excel_transit_week.save_data_single_line(index_loop, name_col_save)
                            index_loop += 1
                            continue

                    # TODO: tutaj należy przeprowadzić walidację z plikiem raportu z cognosa, cały proces.
                    # posługując się text_valid -> wyfiltrowuję nr szipmentu
                    query_cognos_shp = f'RCTNo == "{text_valid}"'
                    value_shp = None
                    multi_shp = False
                    print(f'query_cognos_sshp: {query_cognos_shp}')
                    data_frame_query_response_cognos_shp = excel_receipt_cognos.filter_data_query(query_cognos_shp)
                    print(data_frame_query_response_cognos_shp)
                    if data_frame_query_response_cognos_shp is not None and not data_frame_query_response_cognos_shp.empty:
                        value_shp = data_frame_query_response_cognos_shp["RCTShpNo"].iloc[0]
                        logging.info(f'Dane pobrane df data_frame_query_response_cognos_shp: [{data_frame_query_response_cognos_shp}]')
                        if value_shp is not None:
                            query_cognos_st_0 = f'RCTShpNo == "{value_shp}" and RCTStat == "0"'
                            print(query_cognos_st_0)
                            data_frame_query_response_cognos_st_0 = excel_receipt_cognos.filter_data_query(query_cognos_st_0)
                            if data_frame_query_response_cognos_st_0 is not None and not data_frame_query_response_cognos_st_0.empty:
                                logging.info(f'Shp dla podanego CSM posiada {len(data_frame_query_response_cognos_st_0)} statusów 0: [{excel_receipt_cognos.data_file_filter_query}]'
                                             f'Oczekiwanie na przekrecenie')
                                receipt_st_0 = ",".join([row["RCTNo"] for index, row in data_frame_query_response_cognos_st_0.iterrows()])
                                name_col_save = ["INFO_BOT", "UWAGI"]
                                index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = f"St. 0 Receipt: {receipt_st_0}"
                                excel_transit_week.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = "MULTI / STATUS 0"
                                excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                logging.info(f'Wystąpił STATUS 0 / SHP multi-csm -> do odnotowania w pliku')
                                multi_shp = True

                            else:
                                logging.info(f'Brak statusów 0 w Shp dla podanego CSM: [{excel_receipt_cognos.data_file_filter_query}]'
                                             f'Mozna wprowadzac')
                    else:
                        logging.info(
                            f'Brak danych w data_frame_query_response_cognos_shp: [{excel_receipt_cognos.data_file_filter_query}]')

                    logging.info('Walidacja numeru Receipt przebiegła pomyślnie!')
                    if not multi_shp:
                        put_text(text_valid)
                        clipboard_content, confirm_valid_clipboard = copy(1, str(text_valid))
                        if not confirm_valid_clipboard or clipboard_content is None: #TODO: UWAGA !!!!!! do sprawdzenia TERAZ -> DONE
                            logging.info('Nie skopiowano prawidłowo wartości do pamięci podręcznej! Nastąpi ponowne przetworzenie ostatniego Receipt!')
                            # TODO: mozna tutaj dodac funkcje robiaca screena aktywnego okna zeby sprawdzic co sie wydarzyło,
                            #  dodatkowo skopiowac to co było w schowku i razem z wartoscia ktora powinna sie tam znalezc umiescic w logach
                            #  dodatkowo trzeba dac tutaj 2x powtórzenie żeby jeszcze raz spróbowało wrzucic ten recipt number dopiero jezeli nie to info do excela
                            # TODO: trzeba cos dodać żeby przywrócic ten sam index_loop przy którym właśnie był problem z validacja żeby powtórzyć to.
                            continue

                        confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                        if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path,'image/win_RT2_verify.png', fit_level=0.8, input_delay=1):
                            home(1, 0.1)
                            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_STATUS_1_verify.png', 'image/win_STATUS_0_verify.png', 'image/win_STATUS_3_verify.png', 'image/win_STATUS_4_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                            logging.info(f"Dane po zrobieniu screena -> confirm_screenshot_active: [{confirm_screenshot_active}], type_of_confirmation: [{type_of_confirmation}], path_confirm: [{path_confirm}]")
                            if confirm_screenshot_active and type_of_confirmation == 1:
                                status_receipt = excel_transit_week.data_file_filter_query.iloc[index_loop]['INFO_BOT']
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
                                        index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                        excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                                        excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                    logging.info(f'Dane odświeżone dla wpisu "STATUS 0" -> [column_to_excel_uwagi: {column_to_excel_uwagi}]')

                                if 'STATUS_1' in path_confirm:
                                    confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_MenuChoice_registration_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                    if confirm_screenshot_active and type_of_confirmation == 1 and 'MenuChoice_registration' in path_confirm: #image_detect(screenshot_path, 'image/win_MenuChoice_registration_verify.png', fit_level=0.8, input_delay=1):
                                        put_text('1', 0.1)
                                        enter(1, 0.1)
                                        confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_RT2_EnterSenddatePrenot_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                        if confirm_screenshot_active and type_of_confirmation == 1 and 'RT2_EnterSenddatePrenot' in path_confirm:
                                            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_SendPrenotBtn_verify.png', 'image/win_DeletePrenotBtn_verify.png', 'image/win_LackPrenotBtn_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
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
                                                index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                                if column_to_excel_uwagi is not None:
                                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                                                if column_to_excel_info_bot is not None:
                                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = column_to_excel_info_bot
                                                excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                            logging.info(f'Dane odświeżone dla wpisu "STATUS 1" -> [column_to_excel_uwagi: {column_to_excel_uwagi}] | [column_to_excel_info_bot: {column_to_excel_info_bot}]')
                                elif 'STATUS_0' in path_confirm:
                                    name_col_save = ["INFO_BOT", "UWAGI"]
                                    index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Status 0"
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = "STATUS 0"
                                    excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                    logging.info(f'Wystąpił STATUS 0 -> do odnotowania w pliku')
                                elif ('STATUS_4' in path_confirm or 'STATUS_3' in path_confirm):
                                    logging.info(f'Wystąpił STATUS 3 lub 4 tego transportu - > Został już wprowadzony!')
                                    name_col_save = ["INFO_BOT", "UWAGI"]
                                    index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = "Status 3 lub 4"
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = "DONE"
                                    excel_transit_week.save_data_single_line(index_loop, name_col_save)
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
                        index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                        excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                        excel_transit_week.save_data_single_line(index_loop, name_col_save)
                        value_next_loop_error = 0

                    #continue

                if not confirm_screenshot_active and type_of_confirmation == 2:
                    logging.info("Wykryto zmianę okno podczas działania programu -> Nastąpi wznowienie ostatniego procesu aby odnaleźć prawidłowe okno jeżeli istnieje!")
                    # TODO: trzeba równiez dać max 2 razy dla sprawdzenia a później pominiecie i wpisanie do pliku excel
                    # np index_loop=3
                    #continue
                    #break
                logging.info(f'Index teraz zrobionego Recipte: {index_loop}')
                index_loop += 1
                # np index_loop=4
                logging.info(f'Index następnego Recipte do zrobienia: {index_loop}')
                print("######################")
                logging.info(f"Prównanie danych okna żądanego | systemowego -> {win_app_gts310.hwnd_app_win_active} : {win32gui.GetForegroundWindow()} | {win_app_gts310.title_app_win_active} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                print("######################")
            # Bot wykrył inne okno badź zakończył pracę z wrzucaniem prenotów
            # TODO: trzeba popracować nad zmienną "value_of_same_window_app" ponieważ jeżeli bot wykryje zmiane okna to juz nie wróci do pętli
            #  żeby kontynuowac wrzucanie prenotów tylko wyjdzie do menu, ponieważ wyszedł z nadrzętnej pętli, być może trzeba dodać dodatkowe menu które zatrzyma program
            #  i pozwoli wybrać czy dalej kontynuować czy zakończyć wrzucanie.
            #  Dodatkowo trzeba naprawić działanie zmiennej "index_loop" która miała pokazywać po nieoczekiwanymbłędzie zmiany okna jeszcze raz ten sam index reciptu
            #  do prenotowania. W tej chwili za kazdym razem gdy zadzieje sie błąd powoduje to cofnięcie tej zmiennej o -1 więc jeżeli zadzieje się tak poraz kolejny
            #  to znowu index bedzie cofniety o -1 i tak w koło. W poleceniu 'break' troche wyżej xjest problem, on konczy petle, ale należy pamiętac że po breaku
            #  nie przechodzimy do elsa dla pętli while
            else:
                if win_app_gts310.hwnd_app_win_active != win32gui.GetForegroundWindow() or win_app_gts310.title_app_win_active != win32gui.GetWindowText(win32gui.GetForegroundWindow()):
                    logging.info(f"Wymagane okno [{win_app_gts310.hwnd_app_win_active} : {win_app_gts310.title_app_win_active}] <-> Aktywne okno [{win32gui.GetForegroundWindow()} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}]"
                                 f"\nZakonczono dzialanie petli! Przyczyna -> nieprawidlowe okno -> Program wznowi pracę powtarzając cały ostatni proces!")
                    win_app_gts310.value_of_same_window_app = 0
                    win32gui.EnumWindows(win_app_gts310.find_window_stos_callback_class, partial_title_tab)
                    if win_app_gts310.value_of_same_window_app > 1:
                        app_started = True
                        logging.info(
                            "Aktywne więcej niż jedno okno app GTS"
                        )
                        description = "Apkikacja GTS aktywna ze zbyt wieloma oknami bądź uruchomiona podwójnie, może byc uruchomione tylko jedno okno!!"
                    else:
                        if index_loop > 0:
                            index_loop -= 1
                        if win_app_gts310.value_of_same_window_app == 1:
                            app_started = True
                            logging.info(
                                "Aktywne jedno okno app GTS"
                            )
                            description = "Status Aplikacji GTS DC310: [ AKTYWNA ]"
                        else:
                            app_started = False
                            logging.info(
                                "Brak aktywnych okien app GTS"
                            )
                            description = "Status Aplikacji GTS DC310: [ NIEAKTYWNA ]"


                    # TODO: trzeba równiez dać max 2 razy dla sprawdzenia a później pominiecie i wpisanie do pliku excel
                elif index_loop >= total_index_records_tr:
                    logging.info("Zakonczono dzialanie petli! Przyczyna -> Zakończono wrzucanie PRENOT-ów")
                    # TODO: tutaj można dodać statystyki wrzuconych prenotów z exportem do pliku tekstowego!
                    description = "Zakończono wrzucanie partii ReceiptNo!"
                    tasks_ended = True
                    in_process = False
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
            print("teraz cofamy sie do okna które powinno byc ustawione!")
            f10(1, 0.1)
            ctrl_q(1, 0.1)
            put_text('RT2')
            enter(1, 0.1)
            starting_app = False

        elif win_app_gts310.confirm_alt and 'GTS.AppStarter_DC78 - Global Terminal System' in win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active):
            app_started = True
            logging.info(f"Znaleziono alternatywne okno logowania: {win_app_gts310.hwnd_app_win_active} | {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)}")
            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window('gts_window_screen', ['image/win_LOG_verify.png'], win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
            # TODO: można dopracować to pod kątem sprawdzania czy destynacja jest już ustawiona na starcie czy trzeba ją ustawić
            if confirm_screenshot_active and type_of_confirmation == 1:
                tab(2)
                up(29)
                down(22)
                active_window = gw.getActiveWindow()
                logging.info(f"Dane okna przed zrobieniem screena: {active_window} | hwnd_: {win_app_gts310.hwnd_app_win_active} | przek_: {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
                # list_all_windows()
                # time.sleep(1)
                if image_detect(screenshot_path, 'image/databaseDC310_alternative_screen.png', fit_level=0.8, input_delay=1):
                    logging.info(f"Wykryto okno po kontrolce [image/databaseDC310_alternative_screen.png]")
                    tab(1)
                    enter(1, 0.1)
                else:
                    logging.info("Nie znaleziono na screenie prawidłowej destynacji do logowania -> [ GTS310 Jarosty ], przerwano prace")
                    description = "Nie znaleziono na screenie prawidłowej destynacji do logowania -> [ GTS310 Jarosty ]"
                    # break
                    continue
            if not confirm_screenshot_active and type_of_confirmation == 1:
                logging.info('Niezidentyfikowany błąd podczas próby logowania!')
                description = 'Niezidentyfikowany błąd podczas próby logowania! Zrób screena i zapisz na dysku! Zaloguj GTS ręcznie!'
                continue
            if not confirm_screenshot_active and type_of_confirmation == 2:
                logging.info('Nastąpiła zmiana aktywnego okna podczas próby logowania!')
                description = 'Nastąpiła zmiana aktywnego okna podczas próby logowania!'
                continue
            starting_app = False
        elif len(win_app_gts310.table_window_object) > 1:
            logging.info(f"Aplikacja GTS nie została uruchomiona prawidłowo! -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!"
                         f"\n Ilość otworzonych okien: {len(win_app_gts310.table_window_object)}"
                         f"\n Dane okien w słowniku: {win_app_gts310.table_window_object}")
            description = ("\t -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!")
        elif not win_app_gts310.confirm and not win_app_gts310.confirm_alt and not app_started:
            app_started = False
            in_process = False
            description = "Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!"
            logging.info("Aplikacja GTS nie została uruchomiona! -> Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!")
            continue
        if not win_app_gts310.confirm and not win_app_gts310.confirm_alt:
            description = "Aplikacja GTS przestała odpowiadać!"
            logging.info("Aplikacja GTS przestała odpowiadać! - Uruchom ponownie!")
            app_started = False
            if tasks_ended:
                in_process = False


def run_bot():
    path_tr_file = "C:\\Users\\matok4\\PycharmProjects\\Send_Prenot_Bot_GTS - class\\"
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

