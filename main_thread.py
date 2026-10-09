from pynput.mouse import Listener
from help_function.controller_automate import listener_run, on_move, start_mouse_listener,funkcja_run
# control_event = threading.Event()
# control_event.clear()
# run_flag = [False]


from help_function.controller_auto_object import AutoControlObject
from help_function.raise_exception_object import ExceptionObject
import time
import threading


def function_run(control):
    a = 10
    while a > 0:
        time.sleep(1)
        if control.run_flag:
            print(f"{a}) worker work!")
            a -= 1
            control.run_flag = True
        else:
            print(f"{a})worker stop and run the same one!")
            control.run_flag = True
            input("press")
            control.listener_run = True
    else:
        print("Finish")


control_listener = AutoControlObject()
listener_thread = threading.Thread(target=control_listener.start_mouse_listener)
listener_thread1 = threading.Thread(target=function_run, args=(control_listener,))
listener_thread.start()
listener_thread1.start()
listener_thread.join()
listener_thread1.join()


