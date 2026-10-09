import psutil


def is_application_running(partial_name):
    # Iteruj przez wszystkie procesy
    for proc in psutil.process_iter():
        try:
            # Sprawdź, czy niepełna nazwa procesu znajduje się w pełnej nazwie procesu
            process_name = proc.name()
            print(process_name)
            if partial_name.lower() in process_name.lower():
                print(f"to ten{process_name}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("error")

    return False


def get_application_processes():
    visible_apps = []

    for proc in psutil.process_iter(['pid', 'name']):
        print(proc)