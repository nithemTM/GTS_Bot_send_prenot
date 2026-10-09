import os.path
import os
import time
import logging
import shutil
import subprocess
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ServiceChrom
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as ServiceEdge
from selenium.webdriver.edge.options import Options

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

logger = logging.getLogger(__name__)


def move_download_file(folder_path_source=None, filename=None, user_name=None, folder_path_target=None):
    # folder_path_source = r"C:\Users\matok4\Downloads"
    # folder_path_target = r"\\DSPL310-FS0001.ikea.com\Common_A\FM_Astro SU\Programy_FM\raport"
    folder_path_source = folder_path_source.replace("NAZWA_UŻYTKOWNIKA", user_name)
    source_path = str(os.path.join(folder_path_source, filename))
    target_path = str(os.path.join(folder_path_target, "Suma Receipt.xlsx"))
    while True:
        try:
            if os.path.exists(source_path):
                shutil.move(source_path, target_path)
                print(f"Plik został przeniesiony do {target_path}")
                return True
        except:
            print(f"Plik {filename} nie istnieje w {source_path}.")


def get_latest_file(folder_path, file_name_pattern, user_name):
    folder_path_correct = folder_path.replace("NAZWA_UŻYTKOWNIKA", user_name)
    #expected_file = os.path.join(folder_path_correct, file_name_pattern)
    # Filtruje pliki pasujące do nazwy
    files_list = []
    for file in os.listdir(folder_path_correct):
        if file.endswith(file_name_pattern):
            return ".crdownload", 'today'
        if file.startswith(file_name_pattern):
            files_list.append(file)

    if len(files_list) == 0:
        print(f"Brak plików o takiej nazwie: [ {file_name_pattern} ]")
        return None, None
    # Pobieramy pełne ścieżki do plików i ich daty modyfikacji
    files_data_list = []
    for file in files_list:
        files_data_list.append((file, os.path.getmtime(os.path.join(folder_path_correct, file))))


    # Sortujemy pliki według daty (od najstarszego do najnowszego)
    latest_file, latest_data_reg = max(files_data_list, key=lambda x: x[1])
    print(f"najnowszy: {latest_file}, Data: {datetime.fromtimestamp(latest_data_reg)}")
    return latest_file, latest_data_reg,


def downloading_check(file_name_pattern, folder_path, user_name, latest_file=None, latest_data_reg=None, timeout=15, callback_get_latest_file=None):
    folder_path_correct = folder_path.replace("NAZWA_UŻYTKOWNIKA", user_name)
    #expected_file = os.path.join(folder_path_correct, file_name_pattern)
    files_list = []
    start_time = time.time()
    print(f"Oczekiwanie na pobranie raportu...")
    last_size = -1
    while True:
        cr_download_file, cr_download_file_reg = callback_get_latest_file(folder_path, ".crdownload", user_name)
        if cr_download_file is None:
            latest_file_new, latest_data_reg_new = callback_get_latest_file(folder_path, file_name_pattern, user_name)

            if latest_file_new is not None and ((latest_file is not None and (latest_data_reg_new > latest_data_reg)) or (latest_file is None)):
                expected_file = os.path.join(folder_path_correct, latest_file_new)

                while True:
                    current_size = os.path.getsize(expected_file)
                    if current_size != last_size:
                        print(
                            f"rozmiar obecny: {current_size}, stary: {last_size}")
                        last_size = current_size
                    else:
                        print(
                            f"Nowy plik jest stabilny pobrany: {latest_file_new}, Data: {datetime.fromtimestamp(latest_data_reg_new)}"
                            f"rozmiar obecny: {current_size}, stary: {last_size}")
                        return True, latest_file_new
            else:
                print(f"Nie odnaleziono plików o nazwie zawierającej podany wzór: [ {file_name_pattern} ]")
            if time.time() - start_time > timeout:
                print("Przekroczono dopuszczalny czas oczekiwania na pobranie pliku...")
                return False, None
        #time.sleep(1)


def open_link_web_browser_chrome_driver(url_web=None, browser_data=None, user_name=None):
    driver = None
    service = None
    folder_path = browser_data['path_empty_profile']

    browser_path = None
    for path in browser_data['path']:
        path = path.replace("USER_NAME", user_name)
        if os.path.exists(path):
            browser_path = path
            break
    if browser_path:
        print(f"Odnaleziono {browser_data['exe_name']} przeglądarki!")
    else:
        print("Nie znaleziono .exe w żadnej z domyślnych ścieżek! Wybierz inną przeglądarkę!")
        return None

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Tworzy folder, jeśli go nie ma
        print("Folder został utworzony:", folder_path)
    else:
        print("Folder już istnieje:", folder_path)
    time.sleep(1)

    if "edge" in browser_data['exe_name']:
        options = webdriver.EdgeOptions()
        for arg in browser_data['arguments']:
            options.add_argument(arg)
        driver_path = EdgeChromiumDriverManager().install()
        service = ServiceEdge(driver_path)
        driver = webdriver.Edge(service=service, options=options)
    elif "chrome" in browser_data['exe_name']:
        options = webdriver.ChromeOptions()
        for arg in browser_data['arguments']:
            options.add_argument(arg)
        driver_path = ChromeDriverManager().install()
        service = ServiceChrom(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    print(folder_path)
    # Sprawdzenie, i zamknięcie wszystkich procesów przeglądarki

    # try:
    #     subprocess.run(["taskkill", "/F", "/IM", browser_data['exe_name']], check=True)
    #     print("Wszystkie procesy przeglądarki zostały zamknięte.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Nie udało się zamknąć procesów Edge: {e}")

    # Sprawdzenie, czy folder temp dla danej przeglądarki istnieje
    try:
        driver.get(url_web)
    except:
        print(f"Uruchomienie {browser_data['exe_name']} nie powiodło się!")
        return None

    print(f"{browser_data['exe_name']} uruchomiony z PID: {service.process.pid}")
    return driver


def close_web_browser_process_chromedriver(browser_process=None):
    if browser_process is not None:
        print(f"Zamykanie procesu i sesji przeglądarki {browser_process.name} | {browser_process.session_id}")
        browser_process.quit()
        return True


def open_link_web_browser_subprocess(url_web=None, browser_data=None, user_name=None):
    folder_path = browser_data['path_empty_profile']
    print(folder_path)
    # Sprawdzenie, i zamknięcie wszystkich procesów przeglądarki
    try:
        subprocess.run(["taskkill", "/F", "/IM", browser_data['exe_name']], check=True)
        print("Wszystkie procesy Edge zostały zamknięte.")
    except subprocess.CalledProcessError as e:
        print(f"Nie udało się zamknąć procesów Edge: {e}")
    time.sleep(1)
    # Sprawdzenie, czy folder istnieje

    browser_path = None
    for path in browser_data['path']:
        path = path.replace("USER_NAME", user_name)
        if os.path.exists(path):
            browser_path = path
            break
    if browser_path:
        print(f"Odnaleziono {browser_data['exe_name']} przeglądarki!")
    else:
        print("Nie znaleziono .exe w żadnej z domyślnych ścieżek! Przejście na inną przeglądarkę!")
        return None

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Tworzy folder, jeśli go nie ma
        print("Folder został utworzony:", folder_path)
    else:
        print("Folder już istnieje:", folder_path)

    browser_process = subprocess.Popen([browser_path, *browser_data['arguments'], url_web])
    print(f"Edge uruchomiony z PID: {browser_process.pid}")
    return browser_process


def close_web_browser_process_subprocess(browser_process=None):

    if browser_process is not None:
        print(f"Zamykanie procesu przeglądarki o PID: [ {browser_process.pid} ]")
        browser_process.terminate()
        return True

