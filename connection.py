import socket
import requests

class Connection:

    def __init__(self, host, port):
        self.xml_file = None
        self.xml_path = None
        #self.__init_variables()
        self.__open_connection(host, port)


    def __init_variables(self):
        self._api_url = "http://127.0.0.1:8080/api/v2/"#import-scan/"
        self._headers = {
            "Authorization": f"Token 0d81ac178a3c768ae72ae69978fadc41b694c966"
        }
        self._data = {
            "minimum_severity": "Info",
            "active": None,
            "verified": None,
            "scan_type": "OpenVAS Parser",
            "environment": "Development",
            "service": "script test",
            "close_old_findings": True,
            "close_old_findings_product_scope": True,
            "product_name": "Ativos de Rede",
            "engagement_name": self.xml_path.replace(".xml", "").replace(".csv", ""),
            "auto_create_context": True,
            #"deduplication_on_engagement": True
        }



    def __open_connection(self, host, port):
        self._serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serversocket.bind((host, port))
        self._serversocket.listen(5) #Tem 5 na fila aqui, mas o ideial é fazer paralelismo de pelo menos 3
        self.is_open = True
        print(f"Conexao aberta na porta {port}")


    def close_connection(self):
        print("Desligando Servidor")
        self._serversocket.close()
        self.is_open = False


    def verify_file_type(self, connection: socket):
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


    def receive_file_data(self):

        file_data_string = b""
        connection, address = self._serversocket.accept()
        print(f"IP {address} conectado.")

        with connection:

            file_type = self.verify_file_type(connection)

            # 2 = XML / 3 = CSV
            if file_type == 2 or file_type == 3:
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break
                    file_data_string += data
                    #if file_data_string.decode().strip().find("<target id=") != -1 and file_type == 2:
                    #    break
                print("Arquivo recebido com sucesso!")

                # Envia acknowledgment ao cliente
                connection.send(b"ACK")
            elif file_type == 0:
                print("Arquivo do tipo inválido")

        return file_data_string, file_type


    # def send_file_data(self, file_buffered_reader):
    #     print(file_buffered_reader)
    #     files = {"file": file_buffered_reader}
    #     response = requests.post(self._api_url, headers=self._headers, data=self._data, files=files)

    #     # Imprime resposta da API.
    #     if response.status_code == 201:
    #         print("Arquivo enviado com sucesso!")
    #     else:
    #         print(f"Erro ao enviar o arquivo: {response.status_code} - {response.text}")


    def post_engagement_data(self, file_buffered_reader):
        self.xml_path = file_buffered_reader.name
        self.__init_variables()
        files = {"file": file_buffered_reader}
        import_scan_path = "import-scan/"
        response = requests.post(self._api_url+import_scan_path, headers=self._headers, data=self._data, files=files)

        # Imprime resposta da API.
        if response.status_code == 201:
            print("Arquivo enviado com sucesso!")
        else:
            print(f"Erro ao enviar o arquivo: {response.status_code} - {response.text}")
