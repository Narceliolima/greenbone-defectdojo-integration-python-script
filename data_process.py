class DataProcess:

    def __init__(self):
        pass

    @staticmethod
    def csv_convert_high_to_critical(csv_data: list[list[str]]):

        count = 0

        #Modifica a severidade em ordem decrescente (Se estiver em outra ordem modifique)
        for n, data in enumerate(csv_data):
            if n == 0:
                continue
            cvss = float(data[4].strip())
            severity = data[5].strip()
            if severity == "High" and cvss > 8.9:
                count += 1
                data[5] = "Critical"
                print(f"Linha {n}:{cvss}|{severity}")

        if count == 0:
            print(f"Não houve modificação")
        else:
            print(f"Foram modificados um total de {count} linhas")

        return csv_data