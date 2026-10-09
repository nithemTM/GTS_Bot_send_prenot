import os
import time

import win32gui
import win32com.client
import subprocess
from pywinauto import Application, Desktop


def all_window():
    all_windows = Desktop(backend="uia").windows()

    # Wypisanie tytułów wszystkich widocznych okien
    for window in all_windows:
        print(f"Tytuł okna: '{window.window_text()}'")

def wait_window(window_title):
    # all_windows = Desktop(backend="uia").windows()

    # Wypisanie tytułów wszystkich widocznych okien
    # for window in all_windows:
    #     print(f"Tytuł okna: '{window.window_text()}'")
    while True:
        try:
            all_windows = Desktop(backend="uia").windows()
            for window in all_windows:
                print(f"Tytuł okna: '{window.window_text()}'")
                if window_title == window.window_text():
                    print("Okno zostało uruchomione i jest widoczne.")
                    return 0



        except Exception as e:
            print("Okno nie zostało uruchomione lub nie jest widoczne:", e)
            time.sleep(1)




def run_app(path_app):
    app = Application().start(path_app)
    time.sleep(5)


def enum_window_titles_1(title):
    hwnd = None

    def callback(h, _):
        if title in win32gui.GetWindowText(h):
            nonlocal hwnd
            hwnd = h
            return False

    win32gui.EnumWindows(callback, None)

    return hwnd


def enum_window_titles():
    def callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd):
            titles.append(win32gui.GetWindowText(hwnd))
    titles = []
    win32gui.EnumWindows(callback, titles)

    for title in titles:
        print(f"Window Title: {title}")


def path_get_target(path_shortcut):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path_shortcut)
    # arguments = '-launch -reg "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ictx-1649030d@@IWTS6_Global.GTSGUI RO^_1"'
    #subprocess.Popen(f'"{shortcut.Targetpath}" {shortcut.Arguments}')
    path_app = f'"{shortcut.Targetpath}" {shortcut.Arguments}'
    print(path_app)
    return path_app


def search_app(path_app, window_title):
    #app = Application().start(path_app)
    app = Application(backend='win32').connect(title_re="Consafe Logistics - Astro WMS -  Jarosty DC CDC 310 004 Linux PROD  (M2_Jarosty-DSPL310-NB0066.awc)")
    windows = app.window(title_re='Consafe Logistics - Astro WMS -  Jarosty DC CDC 310 004 Linux PROD  (M2_Jarosty-DSPL310-NB0066.awc)')

    wait_window('Consafe Logistics - Astro WMS -  Jarosty DC CDC 310 004 Linux PROD  (M2_Jarosty-DSPL310-NB0066.awc)')
    print("masz 15 sek")
    time.sleep(15)
    windows.set_focus()



