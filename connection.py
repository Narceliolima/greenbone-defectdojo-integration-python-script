import socket
import requests

class Connection:

    def __init__(self, host: str, green_port: int, dojo_port: int,  api_import_path: str, api_token: str, product_name: str, enviroment: str, service_tag: str):
        self._init_variables(host, dojo_port, api_import_path, api_token, product_name, enviroment, service_tag)
        self._open_connection(host, green_port)


    def close_connection(self):
        print("Desligando Servidor")
        self._serversocket.close()
        self.is_open = False


    def receive_file_data(self):

        if not self.is_open:
            return
        
        file_data_string = b""
        connection, address = self._serversocket.accept()
        print(f"IP {address} conectado.")

        with connection:

            file_type = self._verify_file_type(connection)

            # 2 = XML / 3 = CSV
            if file_type == 2 or file_type == 3:
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break
                    file_data_string += data
                print("Arquivo recebido com sucesso!")

                # Envia acknowledgment ao cliente
                connection.send(b"ACK")
            elif file_type == 0:
                print("Arquivo do tipo inválido")

        return file_data_string, file_type


    def post_engagement_data(self, file_buffered_reader):
        self._add_engagement_name(file_buffered_reader.name)
        files = {"file": file_buffered_reader}

        response = requests.post(self._api_url, headers=self._headers, data=self._data, files=files)

        # Imprime resposta da API.
        if response.status_code == 201:
            print("Arquivo enviado com sucesso!")
        else:
            print(f"Erro ao enviar o arquivo: {response.status_code} - {response.text}")


    @staticmethod
    def send_file_data(host_ip: str, host_port: int, file_data: bytes):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host_ip, host_port))
                s.sendall(file_data)
        except Exception as e:
            print(f"Erro ao enviar arquivo: {e}")


    def _init_variables(self, host: str, port: int, api_import_path: str, api_token: str, product_name: str, enviroment: str, service_tag: str):
        self._api_url = "http://"+host+":"+str(port)+api_import_path
        self._headers = {
            "Authorization": f"Token "+api_token
        }
        self._data = {
            "minimum_severity": "Info",
            "active": None,
            "verified": None,
            "scan_type": "OpenVAS Parser",
            "environment": enviroment,
            "service": service_tag,
            "close_old_findings": True,
            "close_old_findings_product_scope": True,
            "product_name": product_name,
            "auto_create_context": True,
            "deduplication_on_engagement": False
        }


    def _add_engagement_name(self, name: str):
        self._data["engagement_name"] = name.removesuffix(".csv")


    def _open_connection(self, host: str, port: int):
        self._serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serversocket.bind((host, port))
        self._serversocket.listen(3)
        self.is_open = True
        print(f"Conexao aberta na porta {port}")


    def _verify_file_type(self, connection: socket):
        data_flag = connection.recv(11, socket.MSG_PEEK)
        flag = data_flag.decode().strip()
        
        if flag == "kill":
            self.close_connection()
            return 1
        elif flag == "<report id=":
            print("Arquivo XML")
            return 2
        elif flag == "IP,Hostname":
            print("Arquivo CSV")
            return 3
        else:
            return 0