import sys
from csv_file import CsvFile
from csv_process import CsvProcess
from connection import Connection
from xml_file import XmlFile
from send_xml_dojo import SendXmlDojo as sxd

def main():

    # API_KEY = "a30c6d080fa0a93d2527e285c250723f8a813da4"
    # API_URL = "http://127.0.0.1:8080/api/v2/import-scan/"
    connection = Connection("0.0.0.0", 5000)

    file1, file_type1 = connection.receive_file_data()
    file2, file_type2 = connection.receive_file_data()

    if file_type1 == 2 and file_type2 == 3:
        xml_file = XmlFile(file1)
        csv_file = CsvFile(file2, xml_file._xml_file_path)
        csv_file.set_csv_data(CsvProcess.csv_convert_high_to_critical(csv_file.get_csv_string_array()))
        csv_file.save_csv_file()
        connection.post_engagement_data(csv_file.get_csv_buffered_reader())
    elif file_type2 == 2 and file_type1 == 3:
        xml_file = XmlFile(file2)
        csv_file = CsvFile(file1, xml_file._xml_file_path)
        csv_file.set_csv_data(CsvProcess.csv_convert_high_to_critical(csv_file.get_csv_string_array()))
        csv_file.save_csv_file()
        connection.post_engagement_data(csv_file.get_csv_buffered_reader())


    # xml_file = XmlFile(connection.receive_file_data()[0])
    # xml_file.set_xml_data(CsvProcess.xml_convert_high_to_critical(xml_file.get_xml_root()))
    # xml_file.save_xml_file()
    # connection.post_engagement_data(xml_file.get_xml_buffered_reader())


    
    # csv_file = CsvFile(connection.receive_file_data()[0], "LastReport")
    # csv_file.set_csv_data(CsvProcess.csv_convert_high_to_critical(csv_file.get_csv_string_array()))
    # csv_file.save_csv_file()
    # connection.post_engagement_data(csv_file.get_csv_buffered_reader())
    # connection.close_connection()


    # try:
    #     file_path = sys.argv[1]
    #     print(f"Nome do path:{file_path}")
    # except (FileNotFoundError, IndexError) as e:
    #     print(f"Nenhum arquivo foi passado por parametro.")
    
    
    
if __name__ == "__main__":
    main()