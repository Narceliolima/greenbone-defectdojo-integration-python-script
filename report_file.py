import xml.etree.ElementTree as ET
import csv
import io


class ReportFile:
    
    def __init__(self, csv_file_data: bytes, xml_file_data: bytes):
        self._file_path = self._get_file_path(xml_file_data)
        self._file_data = io.BytesIO(csv_file_data)


    def set_report_data(self, csv_file_data: list[list[str]]):
        self._file_data = self._convert_csv_string_list_to_bytes(csv_file_data)
            

    def get_report_string_array(self) -> list[list[str]]:
        return self._convert_csv_bytes_to_string_list(self._file_data)


    def get_report_buffered_reader(self):
        self._file_data.name = self._file_path
        return self._file_data


    def save_report_file(self):
        with open(self._file_path, mode='wb') as file:
            file.write(self._file_data.getvalue())
            print(f"O arquivo {self._file_path} foi salvo com sucesso!")


    def _convert_csv_string_list_to_bytes(self, csv_string_list: list[list[str]]):
        csv_bytes_buffer = io.StringIO()
        writer = csv.writer(csv_bytes_buffer)
        writer.writerows(csv_string_list)
        csv_bytes_buffer.seek(0)
        string_data = csv_bytes_buffer.read()

        # Convertendo para bytes
        csv_bytes_buffer = io.BytesIO(string_data.encode("utf-8"))

        csv_bytes_buffer.seek(0)
        return csv_bytes_buffer


    def _convert_csv_bytes_to_string_list(self, csv_data: io.BytesIO):
        reader = csv.reader(io.StringIO(csv_data.read().decode("utf-8")))
        csv_file = list(reader)
        return csv_file


    def _get_file_path(self, xml_data: bytes) -> str:
        xml_element_tree = ET.parse(io.BytesIO(xml_data))
        return xml_element_tree.getroot().find("task").find("name").text+".csv"
