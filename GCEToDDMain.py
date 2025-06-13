import os
import sys
import signal
import traceback
from connection import Connection
from report_file import ReportFile
from data_process import DataProcess
from dotenv import load_dotenv

running = True
sys.stdout.reconfigure(line_buffering=True)

def handle_sigterm(signum, frame):
    global running
    running = False

    if not load_dotenv("dojointegrationconfigtest.env"):
        load_dotenv("dojointegrationconfig.env")

    server_ip = os.getenv("SERVER_IP")
    green_port = int(os.getenv("GREENBONE_REPORT_SEND_PORT"))
    Connection.send_file_data(server_ip, green_port, b"kill")
    print("Sinal de parada gerado pelo usuário...")

signal.signal(signal.SIGTERM, handle_sigterm)

def main():

    if not load_dotenv("dojointegrationconfigtest.env"):
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

    while running:
        try:
            file1, file_type1 = connection.receive_file_data()
            file2, file_type2 = connection.receive_file_data()

            if not connection.is_open:
                break

            if file_type1 == 2 and file_type2 == 3:
                report_file = ReportFile(file2, file1)
                report_file.set_report_data(DataProcess.csv_convert_high_to_critical(report_file.get_report_string_array()))
                report_file.save_report_file()
                connection.post_engagement_data(report_file.get_report_buffered_reader())
            elif file_type2 == 2 and file_type1 == 3:
                report_file = ReportFile(file1, file2)
                report_file.set_report_data(DataProcess.csv_convert_high_to_critical(report_file.get_report_string_array()))
                report_file.save_report_file()
                connection.post_engagement_data(report_file.get_report_buffered_reader())
            else: 
                print("Formato inválido")
        except:
            traceback.print_exc()


    try:
        if(connection.is_open):
            connection.close_connection()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()