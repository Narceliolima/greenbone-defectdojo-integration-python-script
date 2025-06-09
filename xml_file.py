import xml.etree.ElementTree as ET
import io


class XmlFile:
    
    def __init__(self, file_data: bytes):
        self._xml_file_path = "teste"
        self._xml_element_tree = ET.parse("base.xml")
        self.set_xml_data(file_data)


    def set_xml_data(self, file_data: bytes|ET.ElementTree):
        if isinstance(file_data, bytes):
            self.__create_xml_element_tree(file_data)
        else:
            self._xml_element_tree = file_data



    def get_xml_buffered_reader(self):
        return self.__create_xml_buffer()

    
    # Trocar???
    def get_xml_root(self):
        return self._xml_element_tree


    def save_xml_file(self):
        file_name = self._xml_file_path+".xml"
        self._xml_element_tree.write(file_name)
        print(f"O arquivo {file_name} foi salvo com sucesso!")
    

    def __create_xml_buffer(self):
        # Convertendo para bytes
        xml_stream = io.BytesIO(ET.tostring(self._xml_element_tree.getroot()))

        xml_stream.name = self._xml_file_path+".xml"
        xml_stream.seek(0)
        return xml_stream


    def __create_xml_element_tree(self, file_data: bytes|ET.Element) -> ET.ElementTree:
        
        xml_element_tree = ET.parse(io.BytesIO(file_data))
        self._xml_file_path = xml_element_tree.getroot().find("task").find("name").text
        self._xml_element_tree.getroot().set("id", xml_element_tree.getroot().get("id"))
        self._xml_element_tree.find("task").find("name").text = self._xml_file_path
        self._xml_element_tree.find("name").text = xml_element_tree.find("timestamp").text
        self._xml_element_tree.find("creation_time").text = xml_element_tree.find("timestamp").text
        self._xml_element_tree.find("modification_time").text = xml_element_tree.find("scan_end").text
        self._xml_element_tree.getroot().find("task").set("id", xml_element_tree.find("task").get("id"))
        self._xml_element_tree.getroot().append(xml_element_tree.getroot())
        


    # Unused code, remove later
    # def load_csv_file_string(self):
    #     with open(self._csv_file_path, mode='r', encoding='utf-8') as file:
    #         reader = csv.reader(file)
    #         csv_data = list(reader)
    #         print("Dado lido com sucesso!")
    #         return csv_data
        
    
    # # Debug
    # def load_file(self, file_name):
    #     xml_file = ET.parse(file_name)
    #     root = xml_file.getroot()
    #     self._xml_file_path = root[7][0].text
