import win32api
import win32con
import win32gui


class WindowAppObject:
    def __init__(self, hwnd_app_win=None):
        self.title_app_win = None
        self.hwnd_app_win = hwnd_app_win
        self.window_alt = False
        self.width_size = None
        self.height_size = None
        self.dict_win_data = None

    def get_window_info(self):
        self.title_app_win = win32gui.GetWindowText(self.hwnd_app_win)
        placement_win = win32gui.GetWindowPlacement(self.hwnd_app_win)
        # Pobierz pozycję i rozmiar okna (lewy, góra, prawy, dół)
        rect_position = win32gui.GetWindowRect(self.hwnd_app_win)
        x, y, right, bottom = rect_position
        self.width_size = right - x
        self.height_size = bottom - y

    def move_to_dict_object(self):
        self.dict_win_data = {
            "title_app_win": self.title_app_win,
            "hwnd_app_win": self.hwnd_app_win,
            "window_alt": self.window_alt,
            "width_size": self.width_size,
            "height_size": self.height_size
        }

