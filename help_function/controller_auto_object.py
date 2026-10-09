from pynput.mouse import Listener
from help_function.raise_exception_object import ExceptionObject


class AutoControlObject:
    def __init__(self):
        self.run_flag = True
        self.listener_run = True

    def on_move(self, x, y):
        #print(f"Mose was moved by user [x: {x} | y: {y}]")
        self.run_flag = False
        self.listener_run = False
        return False

    def start_mouse_listener(self):
        while True:
            if self.listener_run:
                print("Listener run")
                with Listener(on_move=self.on_move) as listener:
                    listener.join()


