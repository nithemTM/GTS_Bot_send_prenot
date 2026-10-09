import sys
import time
import win32gui
import pyautogui
# import keyboard

import pygetwindow as gw
import logging
import json
import re
from functools import partial
from help_function.automate_browser_driver import open_link_web_browser_chrome_driver, \
    close_web_browser_process_chromedriver, downloading_check, get_latest_file, move_download_file
from help_function.menu_function import main_menu, menu_continue
from help_function.window_titles import enum_window_titles, search_app, path_get_target, run_app, enum_window_titles_1, \
    wait_window, all_window
from help_function.win32_library import search_app_by_partial_title, find_window_stos_callback, list_all_windows, \
    close_window_callback, app_window_qty_callback, find_window, enum_child_windows, location, pobierz, \
    get_button_info_on_hover1, get_button_info_on_hover, print_class_name_on_hover
from help_function.win32_object import WinAppObjectSearch
from help_function.image_detect import image_detect
from help_function.screen_making import screenshot_active_window
from help_function.controller_automate import tab, down, up, enter, selected_key, send_mute_key, volume_set, \
    bot_speaking, put_text, backspace, f10, ctrl_q, copy, home, escape, on_move, username_get
from help_function.process_os import is_application_running, get_application_processes
from help_function.controller_auto_object import AutoControlObject
from help_function.excel_object import ExcelDataObject
from logger_config import setup_logging
# from main_GUI import Window
# from PyQt5.QtWidgets import QApplication


# is_application_running('wfica32.exe')
# get_application_processes()
# time.sleep(30)
# _, found_pid = win32process.GetWindowThreadProcessId(search_win_hwnd)
# print("wypisz")
# print(found_pid)
# time.sleep(20)


# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

logger = logging.getLogger(__name__)

def run_bot1():

    logger.info("Aplikacja uruchomiona w funkcji [run_bot]")

    path_tr_file = "C:\\Users\\matok4\\PycharmProjects\\GTS_Bot_send_prenot\\"

    excel_transit_week = ExcelDataObject('Transit week 39  19.09.xlsx', path_tr_file, 0, 'A:G', 8)
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
    multi_loop_send_prenot = False
    first_line_loop_shp = 0  # zmienna pozwalajaca stwierdzić który shp jest przerabiany - jego pierwsza linia - pozwoli to do niej wrócić gdyby się coś wysypało i zacząć od nowa
    while True:
        # send_mute_key()
        # volume_set(10)
        # bot_speaking("Bot was started")

        partial_title_win_app = 'GlobalTerminalSystem - RT2 - Registration of OPDC/transitrecei'
        # partial_title_win_app_alt = 'GlobalTerminalSystem - '
        partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'AppStarter']
        # partial_title_win_app_alt = ['GlobalTerminalSystem - ', 'GTS.AppStarter_DC78 - Global Terminal System']
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
                    header_column_transit_week = ['Data & Godz. Rozł.', 'BOT_TASK', 'Shp Id', 'RCTNo', 'INFO_BOT',
                                                  'UWAGI', 'STATUS']
                    excel_transit_permission, description = excel_transit_week.checking_file_form(
                        header_column_transit_week)
                    if not excel_transit_permission:
                        excel_error = True
                        continue
                    else:
                        excel_error = False

                    excel_transit_week.load_data()

                    query_transit_valid = 'BOT_TASK == "WRZUCIĆ"'
                    query = 'BOT_TASK == "WRZUCIĆ" and INFO_BOT != "DONE" and INFO_BOT != "PRZEBUKOWANY" and INFO_BOT != "SKASOWANY"'
                    data_frame_query_response_tr_valid = excel_transit_week.filter_data_query(query_transit_valid)
                    data_frame_query_response_tr = excel_transit_week.filter_data_query(query, 'Shp Id')
                    index_loop = 0
                    # total_index_records_tr_valid = len(data_frame_query_response_tr_valid)
                    print(data_frame_query_response_tr_valid)

                    print(data_frame_query_response_tr)
                    print(excel_transit_week.data_file_filter_query)

                    if data_frame_query_response_tr_valid is None or data_frame_query_response_tr_valid.empty:
                        total_index_records_tr = 0
                        logger.info(
                            'Nie zaznaczono w pliku partii CSMów na których ma być wykonany "Send Prenot"! -> Proszę o zaznaczenie w kolumnie "BOT_TASK"')
                        description = 'Nie zaznaczono w pliku partii CSMów na których ma być wykonany "Send Prenot"! -> Proszę o zaznaczenie w kolumnie "BOT_TASK"'
                        tasks_ended = True
                        continue
                    elif data_frame_query_response_tr is None or data_frame_query_response_tr.empty:
                        total_index_records_tr = 0
                        logger.info('Brak Receipt na których maja zostać wykonany "Send Prenot"!')
                        description = 'Brak Receipt na których maja zostać wykonany "Send Prenot"!'
                        tasks_ended = True
                        continue
                    else:
                        total_index_records_tr = len(data_frame_query_response_tr)
                        in_process = True
                        tasks_ended = False
                        starting_app = True

                        # TODO: załadowane dane df teraz przetworzyć na JSON do dokonczenia -> DONE

                        # with open("data_shipment.json", "r") as file:
                        #      browser_data = json.load(file)
                        json_d = {}
                        for index, row in excel_transit_week.data_file_origin.iterrows():

                            col1 = re.sub(r'[\s-]+', '', row['Shp Id'])
                            col2 = re.sub(r'[\s-]+', '', row['RCTNo'])
                            col3 = re.sub(r'[^\d\\.]+', '', row['STATUS'])
                            # col3 = re.sub(r'[\s-]+', '', row['STATUS'])
                            try:
                                col3 = int(float(col3))
                            except ValueError:
                                col3 = ''
                            shp_value = json_d.get(col1)
                            if shp_value is not None:
                                if shp_value.get(col2) is None:
                                    # json_d[col1][col2] = "None"
                                    if col3 == '':
                                        json_d[col1][col2] = "None"
                                    else:
                                        json_d[col1][col2] = col3

                                else:
                                    pass
                            else:
                                if col3 == '':
                                    json_d[col1] = {col2: "None"}
                                else:
                                    json_d[col1] = {col2: col3}

                            # if shp_value is not None:
                            #     if shp_value.get(col2) is None:
                            #         #json_d[col1][col2] = "None"
                            #         if col3 == '':
                            #             json_d[col1][col2] = "None"
                            #         else:
                            #             json_d[col1][col2] = col3
                            #
                            #     else:
                            #         pass
                            # else:
                            #     json_d[col1] = {col2: "None"}

                            print(f"wiersz {col1}:{col2}")

                        with open("data_shipment.json", "w", encoding="utf-8") as file:
                            json.dump(json_d, file, indent=4)

                        # time.sleep(5)
                        # break
            elif in_process and starting_app:
                a = menu_continue(app_status, description)

                if a == 0:
                    break
                elif a == 2:
                    description = "Przerwano wrzucanie prenotów!"
                    logger.info(
                        f'Przerwanie wrzucania prenotów na [index_loop: {index_loop}]'
                    )
                    in_process = False
                    tasks_ended = True
                    continue
                else:
                    starting_app = True
                    logger.info(
                        f'Wznowiono wrzucanie prenotów od [index_loop: {index_loop}]')
            elif in_process and not starting_app:
                starting_app = True
                logger.info('Kontynuacja procesu!')

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

        logger.info(f'Dane pobrane z pliku excel_transit_week: [{excel_transit_week.data_file_filter_query}]')
        logger.info(f'win_app_gts310.confirm: {win_app_gts310.confirm}')
        if win_app_gts310.confirm:
            app_started = True  # TODO: zmienna do sprawdzenia TERAZ -> DONE
            # description = "Status Aplikacji GTS DC310: [ AKTYWNA ]"
            value_next_loop_error = 0
            multi_loop_id = 0

            while index_loop < total_index_records_tr and win_app_gts310.hwnd_app_win_active == win32gui.GetForegroundWindow() and win_app_gts310.title_app_win_active == win32gui.GetWindowText(
                    win32gui.GetForegroundWindow()):
                text_valid1 = excel_transit_week.data_file_filter_query.iloc[index_loop]['RCTNo']
                shp_valid1 = excel_transit_week.data_file_filter_query.iloc[index_loop]['Shp Id']
                shp_valid1 = re.sub(r'[\s-]+', '', shp_valid1)
                with open("data_shipment.json", "r") as file:
                    data_shipment_json_csm = json.load(file)
                print(data_shipment_json_csm[shp_valid1][str(text_valid1)])
                if data_shipment_json_csm[shp_valid1][str(text_valid1)] in (1, 0, "None"):
                    print("\n######################")
                    logger.info(
                        f"window_data_info->{win_app_gts310.hwnd_app_win_active} : {win32gui.GetForegroundWindow()} | {win_app_gts310.title_app_win_active} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                    print("######################")

                    f10(1, 0.1)
                    ctrl_q(2, 0.1)

                    confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                        'gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'],
                        win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                    if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path,
                                                                                                'image/win_RT2_verify.png',
                                                                                                fit_level=0.8,
                                                                                                input_delay=1):
                        # TODO: JEST PROBLEM -> JEZELI JAKIMS SPOSOBEM IMAGE_DETECTED NIE WYKRYJE WZORCA TO WTEDY CALA PETLA PRZECHODZI DO NASTEPNEGO CSMu A TEGO NIE POWTARZA
                        # TODO: dzieje sie tutaj akurat w momencie kiedy zachodzi podgłaszanie i sciszanie dzieje sie to akurat w momencie robienia zdjecia , !!!!!!!!!!!!!!!! TERAZ
                        backspace(1, 0.1)
                        # TODO: jakikolwiek False zostanie wyrzucony mozna ten csm sprobowac jeszcze raz przepuscic,
                        #  jezeli za drugim razem nie zostanie poprawnie wprowadzony to znaczy ze w GTS pojawia sie problem z jego wrzuceniem
                        # TODO: tutaj bedzie potrzebny wrzucenie juz wspoldziałanie z plikiem excel -> DONE
                        multi_shp = False
                        text_valid = excel_transit_week.data_file_filter_query.iloc[index_loop]['RCTNo']
                        shp_valid = excel_transit_week.data_file_filter_query.iloc[index_loop]['Shp Id']
                        shp_valid = re.sub(r'[\s-]+', '', shp_valid)

                        if index_loop > 0 and not multi_loop_send_prenot:
                            shp_valid_prev = excel_transit_week.data_file_filter_query.iloc[index_loop - 1]['Shp Id']
                            shp_valid_prev = re.sub(r'[\s-]+', '', shp_valid_prev)
                            if shp_valid != shp_valid_prev:
                                first_line_loop_shp = index_loop  # TODO: chodzi o wpisanie do tej zmiennej pierwszej lini z nowym shp dzieki temu bedzie mozna do niej wrocic TERAAZZZZZZZZZZZ !!!!!!!! 26.03.2025
                                # TODO żeby tutaj ogarnąć to co próbowałem zrobić niżej to trzeba przy potwierdzonym multishp = true, multi_loop_send_prenot = False, shp_valid != shp_valid_prev

                        with open("data_shipment.json", "r") as file:
                            data_shipment_json = json.load(file)

                        if not multi_loop_send_prenot:
                            amount_csm = len(data_shipment_json.get(shp_valid))
                            print(amount_csm)
                            if amount_csm > 1:
                                print(
                                    "Pomijamy wrzucanie prenota -> interesuje nas tylko status CSM ktory musimy wrzucić późnije do pliku .json")
                                multi_shp = True
                            print(data_shipment_json)

                        if index_loop + 1 < total_index_records_tr and multi_loop_send_prenot:
                            shp_valid_next = excel_transit_week.data_file_filter_query.iloc[index_loop + 1]['Shp Id']
                            shp_valid_next = re.sub(r'[\s-]+', '', shp_valid_next)
                            if shp_valid != shp_valid_next:
                                multi_loop_send_prenot = False

                        logger.info(f"Receipt Number do przetworzenia: {text_valid}")
                        logger.info(f"SHP Number do przetworzenia: {shp_valid}")
                        fail_valid_receipt = False

                        if "elect" in str(text_valid).lower():
                            logger.error(
                                f'Elektrolux - Wrzucić ręcznie! [text_valid: {text_valid} | type: {type(text_valid)}]')
                            name_col_save = ["UWAGI"]
                            index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                            excel_transit_week.data_file_filter_query.at[
                                index_edit_row_real, "UWAGI"] = "Elektrolux/Wprowadź ręcznie"
                            excel_transit_week.save_data_single_line(index_loop, name_col_save)
                            index_loop += 1
                            continue

                        try:
                            text_valid = int(float(text_valid))
                            if len(str(text_valid)) != 9:
                                fail_valid_receipt = True
                                logger.info(f'Brak poprawnego Receipt! Sprawdz! Podany w programie: {text_valid}')
                                # TODO: uzupełnic wartości w pliku excel tranzytowym -> DONE
                                # continue
                                # break
                        except ValueError as e:
                            fail_valid_receipt = True
                            logger.error(
                                f'Konwersja na liczbę nieudana! Prawdopodobnie nie jest podany prawidłowy Receipt! [text_valid: {text_valid} | type: {type(text_valid)}]'
                                f'\n Error: {e}')
                            # TODO: uzupełnic wartości w pliku excel tranzytowym -> DONE
                            # break
                            # continue
                        finally:
                            if fail_valid_receipt:
                                name_col_save = ["UWAGI"]
                                index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                excel_transit_week.data_file_filter_query.at[
                                    index_edit_row_real, "UWAGI"] = "Uzupełnij/Popraw Receipt"
                                excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                index_loop += 1
                        if fail_valid_receipt:
                            continue
                        # amount_csm = len(data_shipment_json.get(shp_valid))
                        # print(amount_csm)
                        # if amount_csm > 1:
                        #     print(
                        #         "Pomijamy wrzucanie prenota -> interesuje nas tylko status CSM ktory musimy wrzucić późnije do pliku .json")
                        #     multi_shp = True

                        # TODO: teraz sprawdzamy czy SHP dla pobranego CMS w pliku .json posiada więcej niż jeden CSM -> DONE
                        # Sprawdzenie czy następny Reciept w DF jest z tym samym SHP
                        # TODO: TERRAAAZZZZ !!!!! to również jest do ogarniecia - cały poniższy kod, chodzi o to żeby w jakiś sposób wrócić do pierszej lini multishp
                        #  i zaczac wrzucać prenoty 26.03.2025

                        # if index_loop + 1 < total_index_records_tr:
                        #     shp_valid_next = excel_transit_week.data_file_filter_query.iloc[index_loop + 1]['Shp Id']
                        #     shp_valid_next = re.sub(r'[\s-]+', '', shp_valid_next)
                        #     if shp_valid != shp_valid_next:
                        #         if not multi_shp:
                        #
                        #         # if PRENOT
                        #         index_loop = index_loop - multi_loop_id
                        #         print("W pętlętli wracamy do index_loop pomniejszony o wartość multi_loop_id jeżeli po sprawdzeniu z JSON okazuje się że możemy wrzucić PRENOT")
                        #         # if NOT PRENOT
                        #         # multi_loop_send_prenot = False
                        #         print("Kontynuujemy pętlę i idziemy dalej index_loop pozostaje bez zmian jeżeli po sprawdzeniu z JSON okazuje się że nie możemy wrzucić PRENOT")
                        #         print('TUTAJ Zerujemy "multi_loop_id"')
                        #         multi_loop_id = 0
                        #         multi_loop_send_prenot = True
                        #     else:
                        #         multi_loop_id += 1

                        # TODO: skoro jest multi to trzeba sprawdzić ile jest csmów tego shp w DF "wrzucić" wtedy będzie można stwierdzić o ile sie cofnąć po kolejnych zapętleniach
                        # TERAZ - chyba trzeba zrobić osobną mini df po którym bedzie się poruszał i stwierdzał że już zakończyliśmy sprawdzanie
                        # później kolejno reciwy które są w statusie 1 odszukiwac w tym DF i wrzucać prenoty
                        # TODO: no i kluczowe tutaj jest właściwe odnalezienie sie w ID kolejnych lini żeby odpowiednio uzupełnić excela -> to jest najistotniejsze, TERAZ !!!!!!!!!!!!!!
                        # break

                        # 1 trzeba sprawdzić z JSON czy kwalifikuje się ten recipt z multishp do wrzucenia
                        # 2 jeżeli tak (czyli wszystkie CSMy w statusie minimum 1) podejmujemy próbę wrzucenia (może się okazać że on będzie w statusie 0 albo już prenot wysłany)
                        # 3 jeżeli nie (któryś ma status 0 bądź jeszcze status nie był sprawdzany) wtedy tworzymy filtr dla DF (dla tego shp, tylko dla tych ze statusem 0 badź brakiem)
                        # i w pętli przechodzimy po kolejnych reciptach jeżeli skończy się pętla to sprawdzamy czy już mamy całość bez statusów 0
                        # jeżeli TAK -> wracamy na początek tego DF i tym razem przechodzimy po nim wrzucając PRENOTY
                        # jeżeli NIE -> wychodzimy z pętli i przechodzimy do kolejnej lini z DF głównego 'wrzucić'

                        # TODO: tutaj należy przeprowadzić walidację z plikiem raportu z cognosa, cały proces.

                        # # posługując się text_valid -> wyfiltrowuję nr szipmentu
                        # query_cognos_shp = f'RCTNo == "{text_valid}"'
                        # value_shp = None
                        # #multi_shp = False
                        # print(f'query_cognos_sshp: {query_cognos_shp}')
                        # data_frame_query_response_cognos_shp = excel_receipt_cognos.filter_data_query(query_cognos_shp)
                        # print(data_frame_query_response_cognos_shp)
                        # if data_frame_query_response_cognos_shp is not None and not data_frame_query_response_cognos_shp.empty:
                        #     value_shp = data_frame_query_response_cognos_shp["RCTShpNo"].iloc[0]
                        #     logger.info(f'Dane pobrane df data_frame_query_response_cognos_shp: [{data_frame_query_response_cognos_shp}]')
                        #     if value_shp is not None:
                        #         query_cognos_st_0 = f'RCTShpNo == "{value_shp}" and RCTStat == "0"'
                        #         print(query_cognos_st_0)
                        #         data_frame_query_response_cognos_st_0 = excel_receipt_cognos.filter_data_query(query_cognos_st_0)
                        #         if data_frame_query_response_cognos_st_0 is not None and not data_frame_query_response_cognos_st_0.empty:
                        #             logger.info(f'Shp dla podanego CSM posiada {len(data_frame_query_response_cognos_st_0)} statusów 0: [{excel_receipt_cognos.data_file_filter_query}]'
                        #                          f'Oczekiwanie na przekrecenie')
                        #             receipt_st_0 = ",".join([row["RCTNo"] for index, row in data_frame_query_response_cognos_st_0.iterrows()])
                        #             name_col_save = ["INFO_BOT", "UWAGI"]
                        #             index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                        #             excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = f"St. 0 Receipt: {receipt_st_0}"
                        #             excel_transit_week.data_file_filter_query.at[index_edit_row_real, "INFO_BOT"] = "MULTI / STATUS 0"
                        #             excel_transit_week.save_data_single_line(index_loop, name_col_save)
                        #             logger.info(f'Wystąpił STATUS 0 / SHP multi-csm -> do odnotowania w pliku')
                        #             multi_shp = True
                        #
                        #         else:
                        #             logger.info(f'Brak statusów 0 w Shp dla podanego CSM: [{excel_receipt_cognos.data_file_filter_query}]'
                        #                          f'Mozna wprowadzac')
                        # else:
                        #     logger.info(
                        #         f'Brak danych w data_frame_query_response_cognos_shp: [{excel_receipt_cognos.data_file_filter_query}]')

                        logger.info('Walidacja numeru Receipt przebiegła pomyślnie!')
                        # if multi_shp:
                        put_text(text_valid)
                        clipboard_content, confirm_valid_clipboard = copy(1, str(text_valid))
                        if not confirm_valid_clipboard or clipboard_content is None:  # TODO: UWAGA !!!!!! do sprawdzenia TERAZ -> DONE
                            logger.info(
                                'Nie skopiowano prawidłowo wartości do pamięci podręcznej! Nastąpi ponowne przetworzenie ostatniego Receipt!')
                            # TODO: mozna tutaj dodac funkcje robiaca screena aktywnego okna zeby sprawdzic co sie wydarzyło,
                            #  dodatkowo skopiowac to co było w schowku i razem z wartoscia ktora powinna sie tam znalezc umiescic w logach
                            #  dodatkowo trzeba dac tutaj 2x powtórzenie żeby jeszcze raz spróbowało wrzucic ten recipt number dopiero jezeli nie to info do excela
                            # TODO: trzeba cos dodać żeby przywrócic ten sam index_loop przy którym właśnie był problem z validacja żeby powtórzyć to.
                            continue

                        confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                            'gts_window_screen', ['image/win_EnterReceiptnumber_verify.png'],
                            win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                        if confirm_screenshot_active and type_of_confirmation == 1 and image_detect(screenshot_path,
                                                                                                    'image/win_RT2_verify.png',
                                                                                                    fit_level=0.8,
                                                                                                    input_delay=1):
                            home(1, 0.1)
                            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                                'gts_window_screen', ['image/win_STATUS_1_verify.png', 'image/win_STATUS_0_verify.png',
                                                      'image/win_STATUS_3_verify.png', 'image/win_STATUS_4_verify.png'],
                                win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                            logger.info(
                                f"Dane po zrobieniu screena -> confirm_screenshot_active: [{confirm_screenshot_active}], type_of_confirmation: [{type_of_confirmation}], path_confirm: [{path_confirm}]")
                            if confirm_screenshot_active and type_of_confirmation == 1:
                                if multi_shp and not multi_loop_send_prenot:
                                    # TODO: musimy wcześniej na etapie tworzenia DF z shp które mamy wrzucić porównaś SHP wybrane przez użytkownika do SHP z .json i ewentualnie zwiekszyć o csmy nieobjete przez uzytkownia
                                    # TODO: tutaj musimy wysłac informacje o multishipmencie do pliku exel_tranzyt o statusie CSM
                                    # TODO: WAŻNE -> trzeba obmyśleć jak ogarnąć sprawę wrzucania sprawdzonego multishipmentu.
                                    # - chodzi tutaj o przykład kiedy sprawdzam 2,3 i kolejne csmy to muszę wpisać statusy do .json

                                    # with open("data_shipment.json", "r", encoding="utf-8") as file:
                                    #     data_shipment_json = json.load(file)
                                    uwagi = ''
                                    info_bot = ''
                                    status = 0
                                    if 'STATUS_0' in path_confirm:
                                        data_shipment_json[shp_valid][str(text_valid)] = 0
                                        uwagi = "MultiSHP - Status 0"
                                        info_bot = "STATUS 0"
                                    if 'STATUS_1' in path_confirm:
                                        data_shipment_json[shp_valid][str(text_valid)] = 1
                                        info_bot = "MULTISHP"
                                        status = 1
                                    if 'STATUS_3' in path_confirm:
                                        data_shipment_json[shp_valid][str(text_valid)] = 3
                                        uwagi = "MultiSHP - Był Wrzucony"
                                        info_bot = "DONE"
                                        status = 3
                                    if 'STATUS_4' in path_confirm:
                                        data_shipment_json[shp_valid][str(text_valid)] = 4
                                        uwagi = "MultiSHP - Był Wrzucony"
                                        info_bot = "DONE"
                                        status = 4

                                    with open("data_shipment.json", "w", encoding="utf-8") as file:
                                        json.dump(data_shipment_json, file, indent=4, ensure_ascii=False)
                                    name_col_save = ["INFO_BOT", "UWAGI", "STATUS"]
                                    index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "UWAGI"] = uwagi
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "INFO_BOT"] = info_bot
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "STATUS"] = status
                                    excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                    logger.info(f'Aktualizacja pliku dla Receipt w MultiSHP')

                                    # TODO - dać warunek -> if wszystkie csmy w tym shp są już sprawdzone to można przejść dalej i podjąć próbę wrzucenia tylko tych które mają status 1
                                    # TODO - decyzja o powrocie do 'first_line_loop_shp' wtedy wartość 'multi_loop_send_prenot = True' i 'index_loop = first_line_loop_shp' w przeciwnym razie 'index_loop += 1'
                                    with open("data_shipment.json", "r") as file:
                                        data_shipment_json_csm = json.load(file)

                                    # amount_csm_none = sum(1 for value in data_shipment_json_csm[shp_valid].values() if value in (0, "None"))
                                    amount_csm_none = {
                                        "status0": 0,
                                        "status1": 0,
                                        "status34": 0
                                    }
                                    for value in data_shipment_json_csm[shp_valid].values():
                                        if value in (0, "None"):
                                            amount_csm_none["status0"] += 1
                                        if value in (1, 2):
                                            amount_csm_none["status1"] += 1
                                        if value in (3, 4):
                                            amount_csm_none["status34"] += 1

                                    print(f'MULTI:ile 0 i Nono: {amount_csm_none["status34"]}')
                                    print(
                                        f"MULTI:przed zmianą multi_loop_send_prenot: {multi_loop_send_prenot} oraz index loop: {index_loop}")

                                    if amount_csm_none["status0"] == 0 and amount_csm_none["status1"] > 0:
                                        multi_loop_send_prenot = True
                                        index_loop = first_line_loop_shp
                                        print(
                                            f"MULTI:Po zmianie multi_loop_send_prenot: {multi_loop_send_prenot} oraz index loop = first_line_loop_shp: {first_line_loop_shp}")
                                    else:
                                        index_loop += 1
                                        print(
                                            f"MULTI:Po zmiannie multi_loop_send_prenot: {multi_loop_send_prenot} oraz index loop: {index_loop}")

                                    # TODO: TERAZZZAAAAAAA!!!!!! trzeba sprawddzić dlaczego nawet jeżeli statusy są wszystkie z 4 a tylko jeden z 0 i przy ponownej próbie wrzucania okazuje sie że jest to status 1 to przechodzi pętle 2 razy na tym CSMie a nie idzie od razu do wrzucania send prenot
                                    # input_menu = int(input(">> "))
                                    # # os.system('cls')
                                    # if input_menu == 1:
                                    #     continue
                                    # else:
                                    #     break

                                    continue

                                    # - ale problem jest jak mam wrócić do wrzucania wszystkich CSM z tego konkretnego SHP
                                    # - potrzebne jest tutaj zrobienie zmiennej która będzie przechowywac wszystkie linie CSM tego SHP
                                    # - w każdy csm w statusie innym niż 0 z tego shp wpisujemy "multiSHP -St 1/3/4" / csm z statusem 0  wtedy wpisujemy do excela "multiSHP -St 0"
                                    # - potzrebny jest również warunek który w momencie przejcia przez ostatnia linie zweryfikuje z .json czy wszystkie csmy maja inny status niż 0 i który w statusie 1 możemy wrzucić.
                                    # - jeżlei jakis jest w statusie 0 badź nie ma żadnego w statusie 1 wtedy przerywamy pętle wracającą i
                                    # - jezeli po
                                status_receipt = excel_transit_week.data_file_filter_query.iloc[index_loop]['INFO_BOT']

                                if 'STATUS_1' in path_confirm:
                                    confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                                        'gts_window_screen', ['image/win_MenuChoice_registration_verify.png'],
                                        win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                    if confirm_screenshot_active and type_of_confirmation == 1 and 'MenuChoice_registration' in path_confirm:  # image_detect(screenshot_path, 'image/win_MenuChoice_registration_verify.png', fit_level=0.8, input_delay=1):
                                        put_text('1', 0.1)
                                        enter(1, 0.1)
                                        confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                                            'gts_window_screen', ['image/win_RT2_EnterSenddatePrenot_verify.png'],
                                            win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                        if confirm_screenshot_active and type_of_confirmation == 1 and 'RT2_EnterSenddatePrenot' in path_confirm:
                                            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                                                'gts_window_screen', ['image/win_SendPrenotBtn_verify.png',
                                                                      'image/win_DeletePrenotBtn_verify.png',
                                                                      'image/win_LackPrenotBtn_verify.png'],
                                                win_app_gts310.hwnd_app_win_active, win_app_gts310.title_app_win_active)
                                            column_to_excel_uwagi = None
                                            column_to_excel_info_bot = None
                                            if confirm_screenshot_active and type_of_confirmation == 1 and 'SendPrenotBtn_' in path_confirm:
                                                # TODO: tutaj będzie można dalej pociągnąć temat kliknięc SEND PRENOT + wszelkie BŁĘDY
                                                logger.info('Możemy clikac "Send Prenot to WMS')
                                                column_to_excel_uwagi = "Send Prenot"
                                                column_to_excel_info_bot = "DONE"
                                            elif confirm_screenshot_active and type_of_confirmation == 1 and 'DeletePrenotBtn_' in path_confirm:
                                                # TODO: tutaj co w przypadku jeżeli otrzymamy DELET PRENOT
                                                logger.info('Mamy "Delate Prenot to WMS"!')
                                                column_to_excel_uwagi = "Delate Prenot"
                                                column_to_excel_info_bot = "DONE"
                                            elif confirm_screenshot_active and type_of_confirmation == 1 and 'LackPrenotBtn_' in path_confirm:
                                                # TODO: tutaj co w przypadku jeżeli otrzymamy brak przycisku
                                                logger.info(
                                                    'Brak przycisku do wysyłki zamówień tranzytowych! Prawdopodobnie nie jest to tranzyt! brak przycisku')
                                                column_to_excel_uwagi = "Receipt bez TR"
                                            else:
                                                logger.info(
                                                    'Prawdopodobnie błąd który powinien sie pokazać w nastepnej linijce kodu!')
                                            if column_to_excel_uwagi is not None or column_to_excel_info_bot is not None:
                                                if status_receipt == 'STATUS 0':
                                                    column_to_excel_uwagi = "Send Prenot dla st 0"
                                                    logger.info(
                                                        f'Dane odświeżone dla wpisu "STATUS 0" -> [column_to_excel_uwagi: {column_to_excel_uwagi}]')
                                                name_col_save = ["INFO_BOT", "UWAGI", "STATUS"]
                                                index_edit_row_real = excel_transit_week.data_file_filter_query.index[
                                                    index_loop]
                                                if column_to_excel_uwagi is not None:
                                                    excel_transit_week.data_file_filter_query.at[
                                                        index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                                                if column_to_excel_info_bot is not None:
                                                    excel_transit_week.data_file_filter_query.at[
                                                        index_edit_row_real, "INFO_BOT"] = column_to_excel_info_bot

                                                excel_transit_week.data_file_filter_query.at[
                                                    index_edit_row_real, "STATUS"] = 1

                                                excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                            logger.info(
                                                f'Dane odświeżone dla wpisu "STATUS 1" -> [column_to_excel_uwagi: {column_to_excel_uwagi}] | [column_to_excel_info_bot: {column_to_excel_info_bot}]')
                                elif 'STATUS_0' in path_confirm:
                                    name_col_save = ["INFO_BOT", "UWAGI", "STATUS"]
                                    index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "UWAGI"] = "Status 0"
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "INFO_BOT"] = "STATUS 0"
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "STATUS"] = 0
                                    excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                    logger.info(f'Wystąpił STATUS 0 -> do odnotowania w pliku')
                                elif ('STATUS_3' in path_confirm):
                                    logger.info(f'Wystąpił STATUS 3 -> Został już wprowadzony!')
                                    name_col_save = ["INFO_BOT", "UWAGI", "STATUS"]
                                    index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "UWAGI"] = "Był Wrzucony"
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "INFO_BOT"] = "DONE"
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "STATUS"] = 3
                                    excel_transit_week.save_data_single_line(index_loop, name_col_save)
                                elif ('STATUS_4' in path_confirm or 'STATUS_3' in path_confirm):
                                    logger.info(f'Wystąpił STATUS 4 -> Został już wprowadzony!')
                                    name_col_save = ["INFO_BOT", "UWAGI", "STATUS"]
                                    index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "UWAGI"] = "Był Wrzucony"
                                    excel_transit_week.data_file_filter_query.at[
                                        index_edit_row_real, "INFO_BOT"] = "DONE"
                                    excel_transit_week.data_file_filter_query.at[index_edit_row_real, "STATUS"] = 4
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
                        # TODO: potrzebna jest tablica z błędami po której bedzie zapętlanie i sprawdzanie wszystkich dostepnych ich opisów.
                        if image_detect(screenshot_path_error, 'error_image_patterns/win_ALL_NightLogOut_error.png',
                                        fit_level=0.8, input_delay=2) and value_next_loop_error <= 2:
                            logger.info(
                                'Znaleziony błąd: ALL_NightLogOut_error -> przeloguj GTS! -> Nastąpiło nocne wylogowanie aplikacji')
                            app_started = False
                            description = "Nastąpiło nocne wylogowanie aplikacji -> Uruchom ponownie GTS DC310"
                            break
                        elif image_detect(screenshot_path_error,
                                          'error_image_patterns/win_RT2_QueryCausedNoRecords_error.png', fit_level=0.8,
                                          input_delay=2) and value_next_loop_error <= 2:
                            logger.info('Znaleziony błąd: RT2_QueryCausedNoRecords')
                            column_to_excel_uwagi = "Brak Receipt w GTS"
                        elif value_next_loop_error <= 2:
                            column_to_excel_uwagi = "Nieznany Błąd"
                            logger.info(
                                f'Nieznany błąd programu na tym samy Receipt wystąpił 2 raz -> spróbuj odszukać PrintScreen dla tego błędu z podanej wcześniej ścieżki. Wpis do pliku: {column_to_excel_uwagi}')
                        if value_next_loop_error < 2:
                            logger.info('Problem z Receipt -> pierwsza próba!')
                            continue
                        else:
                            name_col_save = ["UWAGI"]
                            index_edit_row_real = excel_transit_week.data_file_filter_query.index[index_loop]
                            excel_transit_week.data_file_filter_query.at[
                                index_edit_row_real, "UWAGI"] = column_to_excel_uwagi
                            excel_transit_week.save_data_single_line(index_loop, name_col_save)
                            value_next_loop_error = 0

                        # continue

                    if not confirm_screenshot_active and type_of_confirmation == 2:
                        logger.info(
                            "Wykryto zmianę okno podczas działania programu -> Nastąpi wznowienie ostatniego procesu aby odnaleźć prawidłowe okno jeżeli istnieje!")
                        # TODO: trzeba równiez dać max 2 razy dla sprawdzenia a później pominiecie i wpisanie do pliku excel
                        # np index_loop=3
                        # continue
                        # break
                    logger.info(f'Index teraz zrobionego Recipte: {index_loop}')
                    index_loop += 1
                    # np index_loop=4
                    logger.info(f'Index następnego Recipte do zrobienia: {index_loop}')
                    print("######################")
                    logger.info(
                        f"Prównanie danych okna żądanego | systemowego -> {win_app_gts310.hwnd_app_win_active} : {win32gui.GetForegroundWindow()} | {win_app_gts310.title_app_win_active} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
                    print("######################")
                else:
                    logger.info("Transport w statusie niespełniającym opcji prenotyfikacji!")
                    logger.info(f'Index Recipte: {index_loop}')
                    index_loop += 1
                    # np index_loop=4
                    logger.info(f'Index następnego Recipte do zrobienia: {index_loop}')

            # Bot wykrył inne okno badź zakończył pracę z wrzucaniem prenotów
            # TODO: trzeba popracować nad zmienną "value_of_same_window_app" ponieważ jeżeli bot wykryje zmiane okna to juz nie wróci do pętli
            #  żeby kontynuowac wrzucanie prenotów tylko wyjdzie do menu, ponieważ wyszedł z nadrzętnej pętli, być może trzeba dodać dodatkowe menu które zatrzyma program
            #  i pozwoli wybrać czy dalej kontynuować czy zakończyć wrzucanie.
            #  Dodatkowo trzeba naprawić działanie zmiennej "index_loop" która miała pokazywać po nieoczekiwanymbłędzie zmiany okna jeszcze raz ten sam index reciptu
            #  do prenotowania. W tej chwili za kazdym razem gdy zadzieje sie błąd powoduje to cofnięcie tej zmiennej o -1 więc jeżeli zadzieje się tak poraz kolejny
            #  to znowu index bedzie cofniety o -1 i tak w koło. W poleceniu 'break' troche wyżej xjest problem, on konczy petle, ale należy pamiętac że po breaku
            #  nie przechodzimy do elsa dla pętli while
            else:
                if win_app_gts310.hwnd_app_win_active != win32gui.GetForegroundWindow() or win_app_gts310.title_app_win_active != win32gui.GetWindowText(
                        win32gui.GetForegroundWindow()):
                    logger.info(
                        f"Wymagane okno [{win_app_gts310.hwnd_app_win_active} : {win_app_gts310.title_app_win_active}] <-> Aktywne okno [{win32gui.GetForegroundWindow()} : {win32gui.GetWindowText(win32gui.GetForegroundWindow())}]"
                        f"\nZakonczono dzialanie petli! Przyczyna -> nieprawidlowe okno -> Program wznowi pracę powtarzając cały ostatni proces!")
                    win_app_gts310.value_of_same_window_app = 0
                    win32gui.EnumWindows(win_app_gts310.find_window_stos_callback_class, partial_title_tab)
                    if win_app_gts310.value_of_same_window_app > 1:
                        app_started = True
                        logger.info(
                            "Aktywne więcej niż jedno okno app GTS"
                        )
                        description = "Apkikacja GTS aktywna ze zbyt wieloma oknami bądź uruchomiona podwójnie, może byc uruchomione tylko jedno okno!!"
                    else:
                        if index_loop > 0:
                            index_loop -= 1
                        if win_app_gts310.value_of_same_window_app == 1:
                            app_started = True
                            logger.info(
                                "Aktywne jedno okno app GTS"
                            )
                            description = "Status Aplikacji GTS DC310: [ AKTYWNA ]"
                        else:
                            app_started = False
                            logger.info(
                                "Brak aktywnych okien app GTS"
                            )
                            description = "Status Aplikacji GTS DC310: [ NIEAKTYWNA ]"

                    # TODO: trzeba równiez dać max 2 razy dla sprawdzenia a później pominiecie i wpisanie do pliku excel
                elif index_loop >= total_index_records_tr:
                    logger.info("Zakonczono dzialanie petli! Przyczyna -> Zakończono wrzucanie PRENOT-ów")
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
        elif win_app_gts310.confirm_alt and 'GTS.AppStarter_DC78 - Global Terminal System' not in win32gui.GetWindowText(
                win_app_gts310.hwnd_app_win_active):
            app_started = True
            logger.info(
                f"Znaleziono alternatywne okno: {win_app_gts310.hwnd_app_win_active} | {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)}")
            print("teraz cofamy sie do okna które powinno byc ustawione!")
            f10(1, 0.1)
            ctrl_q(1, 0.1)
            put_text('RT2')
            enter(1, 0.1)
            starting_app = False

        elif win_app_gts310.confirm_alt and 'GTS.AppStarter_DC78 - Global Terminal System' in win32gui.GetWindowText(
                win_app_gts310.hwnd_app_win_active):
            app_started = True
            logger.info(
                f"Znaleziono alternatywne okno logowania: {win_app_gts310.hwnd_app_win_active} | {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)}")
            confirm_screenshot_active, type_of_confirmation, path_confirm = screenshot_active_window(
                'gts_window_screen', ['image/win_LOG_verify.png'], win_app_gts310.hwnd_app_win_active,
                win_app_gts310.title_app_win_active)
            # TODO: można dopracować to pod kątem sprawdzania czy destynacja jest już ustawiona na starcie czy trzeba ją ustawić
            if confirm_screenshot_active and type_of_confirmation == 1:
                tab(2)
                up(29)
                down(20)
                active_window = gw.getActiveWindow()
                logger.info(
                    f"Dane okna przed zrobieniem screena: {active_window} | hwnd_: {win_app_gts310.hwnd_app_win_active} | przek_: {win32gui.GetWindowText(win_app_gts310.hwnd_app_win_active)} | win32gui.GetForegroundWindow()_: {win32gui.GetForegroundWindow()}")
                # list_all_windows()
                # time.sleep(1)
                if image_detect(screenshot_path, 'image/databaseDC310_alternative_screen.png', fit_level=0.8,
                                input_delay=1):
                    logger.info(f"Wykryto okno po kontrolce [image/databaseDC310_alternative_screen.png]")
                    tab(1)
                    enter(1, 0.1)
                else:
                    logger.info(
                        "Nie znaleziono na screenie prawidłowej destynacji do logowania -> [ GTS310 Jarosty ], przerwano prace")
                    description = "Nie znaleziono na screenie prawidłowej destynacji do logowania -> [ GTS310 Jarosty ]"
                    # break
                    continue
            if not confirm_screenshot_active and type_of_confirmation == 1:
                logger.info('Niezidentyfikowany błąd podczas próby logowania!')
                description = 'Niezidentyfikowany błąd podczas próby logowania! Zrób screena i zapisz na dysku! Zaloguj GTS ręcznie!'
                continue
            if not confirm_screenshot_active and type_of_confirmation == 2:
                logger.info('Nastąpiła zmiana aktywnego okna podczas próby logowania!')
                description = 'Nastąpiła zmiana aktywnego okna podczas próby logowania!'
                continue
            starting_app = False
        elif len(win_app_gts310.table_window_object) > 1:
            logger.info(
                f"Aplikacja GTS nie została uruchomiona prawidłowo! -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!"
                f"\n Ilość otworzonych okien: {len(win_app_gts310.table_window_object)}"
                f"\n Dane okien w słowniku: {win_app_gts310.table_window_object}")
            description = (
                "\t -> Aplikacja GTS ma uruchomione więcej niż jedno okno tej aplikacji (Zamknij niepotrzebne, aktywne może byc tylko jedno)!")
        elif not win_app_gts310.confirm and not win_app_gts310.confirm_alt and not app_started:
            app_started = False
            in_process = False
            description = "Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!"
            logger.info(
                "Aplikacja GTS nie została uruchomiona! -> Aplikacja GTS nie została uruchomiona w trakcie ostatniej sesji programu!")
            continue
        if not win_app_gts310.confirm and not win_app_gts310.confirm_alt:
            description = "Aplikacja GTS przestała odpowiadać!"
            logger.info("Aplikacja GTS przestała odpowiadać! - Uruchom ponownie!")
            app_started = False
            if tasks_ended:
                in_process = False


def run_bot():
    path_tr_file = "C:\\Users\\matok4\\PycharmProjects\\Send_Prenot_Bot_GTS - class\\"
    tr_excel_info = ExcelDataObject('Transit week 39  19.09.xlsx', path_tr_file, 0, 'A:F', 8)
    tr_excel_info.load_data(0, 'A:F', 8)
    # a = tr_excel_info.filter_data('BOT', 'WRZUCIĆ')
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
    # print(tr_excel_info.list_file_data)
    # print(tr_excel_info.data_file_origin)