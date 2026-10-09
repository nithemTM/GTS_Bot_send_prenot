import openpyxl
import pandas as pd
from openpyxl import load_workbook


class ExcelDataObject:
    def __init__(self, name_file, path_file, sheet_name=0, column_index=None, header_index=None):
        self.name_file = name_file
        self.path_file = path_file
        self.column_index = column_index
        self.header_index = header_index
        self.sheet_name = sheet_name
        self.path_file_execute = path_file+name_file
        self.first_line_data = None
        self.data_file_origin = None
        self.data_file_filter_query = None
        self.column_list = None
        self.header_row = None
        self.data_file_edit = None
        self.list_file_data = []
        self.index_skip = None
        if self.header_index is not None:
            self.index_skip = self.header_index - 1
            self.first_line_data = self.header_index + 1

        pd.set_option('display.max_rows', None)  # Wyświetli wszystkie wiersze
        pd.set_option('display.max_columns', None)  # Wyświetli wszystkie kolumny
        pd.set_option('display.expand_frame_repr', False) # Uniknie złamań wierszy

    def checking_file_form(self, header_to_check):
        # Funkcja ma zadanie sprawdzenia pliku wczytanego przez urzytkownika pod kontem:
        # - pozwolenia na zapis
        # - prawidłowej formy pliku oraz jego rozszeżenia
        wb_checking = None
        if '.xlsx' not in self.path_file_execute:
            return False, f"Plik [{self.path_file_execute}] ma nieprawidłowe rozszeżenie! Dozwolone tylko [.xlsx]!"
        try:
            wb_checking = openpyxl.load_workbook(self.path_file_execute)
            wb_checking.save(self.path_file_execute)
            header_row_df = pd.read_excel(self.path_file_execute, sheet_name=self.sheet_name, usecols=self.column_index,
                                          skiprows=self.index_skip, nrows=0, engine="openpyxl")
            self.header_row = header_row_df.columns.tolist()
            print(f"Wczytane_kolumny{self.header_row}")
            if header_to_check != self.header_row:
                return False, f"Plik [{self.path_file_execute}] ma nieprawidłową strukture! Niezgodność w nazwach kolumn bądź ich ułożeniu! Popraw plik"
        except PermissionError:
            # Jeśli plik jest zajęty, wyświetlamy komunikat
            print(f"Plik {self.path_file_execute} jest zajęty przez inny proces lub użytkownika.")
            return False, f"Plik [{self.path_file_execute}] jest otworzony przez innego urzytkownika badź proces! Nie możemy zapisać danych, zamknij plik!"
        except FileNotFoundError:
            # Plik nie istnieje
            print(f'Plik [{self.path_file_execute}] nie istnieje w tej ścieżce! Upewnij sie czy istnieje!')
            return False, f'Plik [{self.path_file_execute}] nie istnieje w tej ścieżce! Upewnij sie czy istnieje!'
        finally:
            if wb_checking:
                print("Zamykanie otwartego pliku!")
                wb_checking.close()

        return True, f'Plik [{self.path_file_execute}] jest prawidłowo udostępniony dla programu!'

    def load_data(self):
        self.data_file_origin = pd.read_excel(self.path_file_execute, sheet_name=self.sheet_name, usecols=self.column_index, skiprows=self.index_skip, engine="openpyxl")
        self.list_file_data = self.data_file_origin.values.tolist()
        self.data_file_origin = self.data_file_origin.astype(str)
        self.data_file_origin = self.data_file_origin.apply(lambda df_origin: df_origin.str.strip() if df_origin.dtype == "object" else df_origin)
        print(self.data_file_origin.dtypes)
        print(f'Plik [{self.path_file_execute}] -> Data Frame został załadowany do programu!')

    def save_data(self, output_path, index=False):
        if self.data_file_edit is not None:
            self.data_file_edit.to_excel(output_path, index=index)
        else:
            print("Brak edytowanych danych do zapisania!")

    def filter_data_query(self, query, sort=None):
        if self.data_file_origin is not None:
            try:
                self.data_file_filter_query = self.data_file_origin.query(query)
            except Exception as e:
                print(f'Wystąpił problem podczas pobierania danych z df -> {e}!')
                return None
            if sort is not None:
                if sort in self.header_row:
                    self.data_file_filter_query = self.data_file_filter_query.sort_values(by=sort)
                else:
                    print("Nie dokonano filtrowania ! Podana nazwa kolumny nie znajduje sie na liście!")
            return self.data_file_origin.query(query)
        else:
            print("Brak danych DF - być może pusty arkusz excel!")
            self.data_file_filter_query = None
            return None

    def save_data_single_line(self, index_edit_row, name_col_save):

        if self.data_file_filter_query is not None:
            # TODO: trzeba rzucić wyjątkiem
            try:
                wb = openpyxl.load_workbook(self.path_file_execute)
            except:
                print(f'Plik z podanej ścieżki nie istnieje: {self.path_file_execute}')

            sheet = wb['ilości Załadunków']
            print(f"index w DATAFRAME: -----> {index_edit_row}")
            print(f"index w DATAFRAME: -----> {self.data_file_filter_query.index[index_edit_row]}")
            index_row_data_filter = self.data_file_filter_query.index[index_edit_row]
            index_row_file = self.data_file_filter_query.index[index_edit_row] + self.first_line_data
            print(f"index_row_file: {index_row_file}")
            #edit_row = self.data_file_filter_query.iloc[index_edit_row_real]
            for column_name in name_col_save:
                #column_name = f'"{column_name}"'
                index_column_file = self.data_file_filter_query.columns.get_loc(column_name) + 1
                print(f"index_edit_column dla [{column_name}] to: {index_column_file}")
                sheet.cell(row=index_row_file, column=index_column_file).value = self.data_file_filter_query.at[index_row_data_filter, column_name]
                print(f"to co chcemy wpisać do excela = {self.data_file_filter_query.at[index_row_data_filter, column_name]}")
            # TODO: trzeba rzucić wyjątkiem
            try:
                wb.save(self.path_file_execute)
            except PermissionError:
                print("Żądany plki jest otworzony przez innego urzytkownika! Nie możemy zapisać danych, zamknij plik a później kliknij [Press]")
            finally:
                wb.close()
        else:
            print("Brak edytowanych danych do zapisania!")

#########################################
    def filter_data(self, column_name, condition):
        if self.data_file_origin is not None:
            return self.data_file_origin[self.data_file_origin[column_name] == condition]
        else:
            print("brak")