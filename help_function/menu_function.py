import os


def main_menu(app_status, description=None):
    if description is None:
        description = ''
    description_menu = ''
    while True:
        input_menu = -1
        #os.system('cls')
        print("[          SEND PRE-NOT GTS BOT         ]\n")
        print('__________________________')
        print(f'STATUS APLIKACJI GTS_DC78: [ {app_status} ]')
        print(f"[UWAGA: {description}]\n")
        print(f"{description_menu}\n")
        print("     [ MENU ]")
        print(f"[1] Start Programu (Aplikacja GTS {app_status.lower()})")
        print("[0] Exit")
        try:
            input_menu = int(input(">> "))
            #os.system('cls')
            if 0 > input_menu or input_menu > 1:
                description_menu = " [!] Błędny wpis przy wyborze menu!"
            elif input_menu == 0:
                return False
            else:
                return True
        except:
            #os.system('cls')
            description_menu = " [!] Błędny wpis przy wyborze menu!"
            print(" [!] Błędny wpis!")


def menu_continue(app_status, description=None):
    if description is None:
        description = ''
    description_menu = ''
    while True:
        input_menu = -1
        #os.system('cls')
        print('__________________________')
        print(f'STATUS APLIKACJI GTS_DC78: [ {app_status} ]')
        print(f"[UWAGA: {description}]\n")
        print(f"{description_menu}\n")
        print("________________________________________________")
        print(f"[1] Kontynuuj pracę programu! (Aplikacja GTS {app_status.lower()})")
        print(f"[2] Przerwij wrzucanie prenotów! ()")
        print("[0] Exit")
        try:
            input_menu = int(input(">> "))
            #os.system('cls')
            if 0 > input_menu or input_menu > 2:
                description_menu = " [!] Błędny wpis przy wyborze menu!"
            else:
                return input_menu
        except:
            #os.system('cls')
            description_menu = " [!] Błędny wpis przy wyborze menu!"
            print(" [!] Błędny wpis!")