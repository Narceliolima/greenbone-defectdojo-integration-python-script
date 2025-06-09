import csv
import io

class CsvFile:
    
    def __init__(self, csv_data:bytes, csv_file_path: str):
        self._csv_file_path = csv_file_path+".csv"
        self._csv_string_list = [[""]]
        self.set_csv_data(csv_data)


    def set_csv_data(self, csv_data: list[list[str]]):
        if isinstance(csv_data, bytes):
            csv_data = CsvFile.__convert_csv_bytes_to_string_list(csv_data)
        self._csv_string_list = csv_data


    def get_csv_buffered_reader(self):
        return self.__create_csv_buffer()

    
    def get_csv_string_array(self):
        return self._csv_string_list


    def save_csv_file(self):
        with open(self._csv_file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self._csv_string_list)
            print(f"O arquivo {self._csv_file_path} foi salvo com sucesso!")


    # # Colocar para salvar no file_path
    # def save_csv_file(self):
    #     with open(self._csv_string_list.name, mode='wb') as file:
    #         file.write(self._csv_string_list.getvalue())
    #         print("Dado salvo com sucesso!")


    @staticmethod
    def __convert_csv_bytes_to_string_list(csv_data):
        reader = csv.reader(io.StringIO(io.BytesIO(csv_data).read().decode("utf-8")))
        csv_file = list(reader)
        return csv_file


    def __create_csv_buffer(self):
        csv_stream = io.StringIO()
        writer = csv.writer(csv_stream)
        writer.writerows(self._csv_string_list)
        csv_stream.seek(0)
        string_data = csv_stream.read()

        # Convertendo para bytes
        csv_stream = io.BytesIO(string_data.encode("utf-8"))

        csv_stream.name = self._csv_file_path
        csv_stream.seek(0)
        return csv_stream
    

    # Unused code, remove later
    # def load_csv_file_string(self, file_name):
    #     with open(file_name, mode='r', encoding='utf-8') as file:
    #         reader = csv.reader(file)
    #         csv_data = list(reader)
    #         print("Dado lido com sucesso!")
    #         self.set_csv_data(csv_data)
        
    
    # # Debug
    # def load_csv_file(self, file_name):
    #     with open(file_name, mode='rb') as file:
    #         print("Dado lido com sucesso!")
    #         self.set_csv_data(file.read())
    #         #return file.read()