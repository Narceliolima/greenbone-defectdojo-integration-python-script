import os
from csv_file import CsvFile
from csv_process import CsvProcess
from connection import Connection
from xml_file import XmlFile
from dotenv import load_dotenv

def main():

    load_dotenv("dojointegrationconfig.env")

    server_ip = os.getenv("SERVER_IP")
    green_port = int(os.getenv("GREENBONE_REPORT_SEND_PORT"))
    dojo_port = int(os.getenv("DEFECTDOJO_PORT"))
    api_import_path = os.getenv("DEFECTDOJO_API_IMPORT_PATH")
    api_token = os.getenv("DEFECTDOJO_API_TOKEN")
    product_name = os.getenv("DEFECTDOJO_PRODUCT_NAME")
    enviroment = os.getenv("DEFECTDOJO_ENVIROMENT")
    service_tag = os.getenv("DEFECTDOJO_SERVICE_TAG")

    connection = Connection(server_ip, green_port, dojo_port, api_import_path, api_token, product_name, enviroment, service_tag)

    try:
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
    except Exception as e:
        print(e)
    finally:
        try:
            connection.close_connection()
        except Exception as e:
            print(e)
    

    # xml_file = XmlFile(connection.receive_file_data()[0])
    # xml_file.set_xml_data(CsvProcess.xml_convert_high_to_critical(xml_file.get_xml_root()))
    # xml_file.save_xml_file()
    # connection.post_engagement_data(xml_file.get_xml_buffered_reader())


    
    # csv_file = CsvFile(connection.receive_file_data()[0], "LastReport")
    # csv_file.set_csv_data(CsvProcess.csv_convert_high_to_critical(csv_file.get_csv_string_array()))
    # csv_file.save_csv_file()
    # connection.post_engagement_data(csv_file.get_csv_buffered_reader())
    # connection.close_connection()
    
    
if __name__ == "__main__":
    main()