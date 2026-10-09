import logging
from datetime import datetime
from pynput.keyboard import Key, Controller, KeyCode
from pynput.mouse import Listener
import win32clipboard
import time
import ctypes
import pyttsx3
import os
import webbrowser
import subprocess
import re
from enum import Enum
import pythoncom

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

logger = logging.getLogger(__name__)

# class SpecialKey(Enum):
#     ENTER = 0x0D
#     BACKSPACE = 0x08
#     TAB = 0x09
#     ESCAPE = 0x1B
#     SPACE = 0x20
#     ALT = 0x12
#     CONTROL = 0x11
#     SHIFT = 0x10
#     SUBTRACT = 0x6D
#
#     # Przyjazne nazwy dla klawiszy
#     descriptions = {
#         "enter": ENTER,
#         "backspace": BACKSPACE,
#         "tab": TAB,
#         "escape": ESCAPE,
#         "space": SPACE,
#         "alt": ALT,
#         "ctrl": CONTROL,
#         "shift": SHIFT,
#         "subtract": SUBTRACT
#     }
#
#     def key_y(self, key_short, click_qty, delay=None):
#         key = self.descriptions[key_short].value
#         #key_hex = int(f"0x{key.value:02X}")
#         for i in range(0, click_qty):
#             if delay is not None:
#                 time.sleep(delay)
#             keyboard = Controller()
#             keyboard.press(KeyCode.from_vk(key.value))
#             keyboard.release(KeyCode.from_vk(key.value))
run_flag = [True]
listener_run = [True]


def username_get():
    user_name = os.getenv("USERNAME")
    print(f"Jesteś zalogowany jako: [ {user_name} ]")

    return user_name


def bot_speaking(text_to_say):
    engin = pyttsx3.init()
    voices = engin.getProperty('voices')
    engin.setProperty('rate', 130)
    polish_voice_found = False
    for voice in voices:
        if 'polski' in voice.languages:
            engin.setProperty('voice', voice.id)
            polish_voice_found = True
            break

    if not polish_voice_found:
        print("Brak polskiego głosu")
    engin.say(text_to_say)
    engin.runAndWait()


def on_move(x, y):
    print(f"Mose was moved by user [x: {x} | y: {y}]")
    run_flag[0] = False
    listener_run[0] = False


def start_mouse_listener():
    with Listener(on_move=on_move) as listener:
        listener.join()


def funkcja_run():
    a = 10
    while a > 0:
        time.sleep(1)
        if run_flag[0]:
            print(f"{a}) worker work!")
            a -= 1
            run_flag[0] = True
        else:
            print(f"{a})worker stop and run the same one!")
            run_flag[0] = True
            input("press")
            listener_run[0] = True


def tab(click_qty):
    #time.sleep(0.5)
    for i in range(0, click_qty):
        keyboard = Controller()
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        #print(f"tab nr: {i}")


def down(click_qty):
    #time.sleep(0.2)
    for i in range(0, click_qty):
        keyboard = Controller()
        keyboard.press(Key.down)
        keyboard.release(Key.down)


def f10(click_qty, delay=None):
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        keyboard = Controller()
        keyboard.press(Key.f10)
        keyboard.release(Key.f10)


def escape(click_qty, delay=None):
    keyboard = Controller()
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        with keyboard.pressed(Key.ctrl):
            print("klikam esc")
            vk_escape = 0x1B
            time.sleep(1)
            keyboard.press(KeyCode.from_vk(vk_escape))
            keyboard.release(KeyCode.from_vk(vk_escape))


def send_mute_key():
    keyboard = Controller()
    print("klikam mute")
    vk_volume_mute_key = 0xAD
    keyboard.press(KeyCode.from_vk(vk_volume_mute_key))
    keyboard.release(KeyCode.from_vk(vk_volume_mute_key))


def volume_set(level):
    keyboard = Controller()
    for _ in range(50):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)

    for _ in range(round(level/2)):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)


def up(click_qty, delay=None):
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        keyboard = Controller()
        keyboard.press(Key.up)
        keyboard.release(Key.up)


def ctrl_q(click_qty, delay=None):
    keyboard = Controller()
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        with keyboard.pressed(Key.ctrl):
            keyboard.press('q')
            keyboard.release('q')


def copy(delay=None, value_to_check=None):
    pythoncom.CoInitialize()
    import pyperclip
    error_copy = False
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    keyboard = Controller()
    with keyboard.pressed(Key.ctrl):
        keyboard.press('a')
        keyboard.release('a')
        keyboard.press('c')
        keyboard.release('c')
    if delay is not None:
        time.sleep(delay)
    try:
        win32clipboard.OpenClipboard()
        content_clipboard = win32clipboard.GetClipboardData()
        logger.info(f'value_to_check: [{value_to_check}')
    except Exception as e:
        content_clipboard = None
        error_copy = True
        logger.info(f"\nError Pobierania ze schowka przy funkcji (copy): {e}")
        logger.info(f'clipboard_content: [content_clipboard: None], value_to_check: [{value_to_check}]')
    finally:
        win32clipboard.CloseClipboard()
        pythoncom.CoUninitialize()

    if error_copy:
        logger.info(
            f'Kopiowanie zakończone niepowodzeniem -> clipboard_content: [{content_clipboard}], confirm_valid_clipboard: [False], value_to_check: [{value_to_check}]'
        )
        return content_clipboard, False
    elif not error_copy:
        is_content_equal = content_clipboard == value_to_check

        if value_to_check is not None:
            if is_content_equal:
                logger.info(
                    f'Kopiowanie zakończone powodzeniem ValueNotNone 1-> clipboard_content: [{content_clipboard[:15]}], confirm_valid_clipboard: [True], value_to_check: [{value_to_check}]'
                )
                return content_clipboard, True
            else:
                logger.info(
                    f'Kopiowanie zakończone powodzeniem ValueNotNone 2-> clipboard_content: [{content_clipboard[:15]}], confirm_valid_clipboard: [False], value_to_check: [{value_to_check}]'
                )
                return content_clipboard, False
        else:
            if content_clipboard is not None:
                logger.info(
                    f'Kopiowanie zakończone powodzeniem ValueNone 1-> clipboard_content: [{content_clipboard[:15]}], confirm_valid_clipboard: [True], value_to_check: [{value_to_check}]'
                )
                return content_clipboard, True
            else:
                logger.info(
                    f'Kopiowanie zakończone powodzeniem ValueNone 2-> clipboard_content: [{content_clipboard}], confirm_valid_clipboard: [False], value_to_check: [{value_to_check}]'
                )
                return content_clipboard, False

        # if value_to_check is not None:
        #     if content_clipboard == value_to_check:
        #         logger.info(
        #             f'Kopiowanie zakończone powodzeniem ValueNotNone 1-> clipboard_content: [{content_clipboard[:15]}], confirm_valid_clipboard: [True], value_to_check: [{value_to_check}]'
        #         )
        #         return content_clipboard, True
        #     elif content_clipboard != value_to_check and content_clipboard is not None:
        #         logger.info(
        #             f'Kopiowanie zakończone powodzeniem ValueNotNone 2-> clipboard_content: [{content_clipboard[:15]}], confirm_valid_clipboard: [False], value_to_check: [{value_to_check}]'
        #         )
        #         return content_clipboard, False
        #     else:
        #         logger.info(
        #             f'Kopiowanie zakończone powodzeniem ValueNotNone 3-> clipboard_content: [{content_clipboard}], confirm_valid_clipboard: [False], value_to_check: [{value_to_check}]'
        #         )
        #         return content_clipboard, False
        #
        # elif value_to_check is None:
        #     if content_clipboard != value_to_check:
        #         logger.info(
        #             f'Kopiowanie zakończone powodzeniem ValueNone 1-> clipboard_content: [{content_clipboard[:15]}], confirm_valid_clipboard: [True], value_to_check: [{value_to_check}]'
        #         )
        #         return content_clipboard, True
        #     else:
        #         logger.info(
        #             f'Kopiowanie zakończone powodzeniem ValueNotNone 2-> clipboard_content: [{content_clipboard}], confirm_valid_clipboard: [False], value_to_check: [{value_to_check}]'
        #         )
        #         return content_clipboard, False


def enter(click_qty, delay=None):
    a = 0x0D
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        keyboard = Controller()
        keyboard.press(KeyCode.from_vk(a))
        keyboard.release(KeyCode.from_vk(a))


def home(click_qty, delay=None):
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        keyboard = Controller()
        keyboard.press(Key.home)
        keyboard.release(Key.home)


def selected_key(key, click_qty=1, delay=None):
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        keyboard = Controller()
        keyboard.press(key)
        keyboard.release(key)


def backspace(click_qty=1, delay=None):
    for i in range(0, click_qty):
        if delay is not None:
            time.sleep(delay)
        keyboard = Controller()
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)


def put_text(value, delay=None):
    keyboard = Controller()
    if delay is not None:
        time.sleep(delay)
    keyboard.type(str(value))


