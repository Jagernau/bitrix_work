import re
from parser.classes import Glonasssoft
from configurations import config
from datetime import datetime
from data_entry import with_token_comand_put_get_glonasssoft
from database.database import Database
import database.models as models
from tqdm import tqdm
import sys

class GlonassComands:

    def __init__(self, glonass_login: str, glonass_password: str):
        self.glonass_login = glonass_login
        self.glonass_password = glonass_password
    
    @property
    def glonass_token(self) -> str:
        glonass = Glonasssoft(str(self.glonass_login), str(self.glonass_password))
        token = str(glonass.token)
        return token

    def get_glonass_imeis_from_pattern(self, pattern: str) -> list:
        session = Database().session
        objects = session.query(models.CaObject.imei).filter(
                models.CaObject.imei != None,
                models.CaObject.sys_mon_id == 1).all()
        session.close()
        imei_set = set([i for i in objects if re.search(pattern, str(i.imei))])
        return list(imei_set)

    def ask_glonasssoft_terminal(self, imei: str, command: str, token_glonass: str):
        """
        Опрашивает терминалы которые в базе данных на глонассофт
        imee - imei терминала
        command - команда которую он хочет выполнить
        token_glonass - токен глонассофта
        """
        data = with_token_comand_put_get_glonasssoft(
                token_glonass=token_glonass,
                command_glonass=command,
                imei_glonas=str(imei),
                )
        if data[0]["status"] == True:
            with open(f"call terminals_{command}.txt", "a") as file:
                file.write(f"{imei} {command} {datetime.now()}\n")
            return data
        else:
            return None

def job():
    glonass = GlonassComands(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    glonass_token = glonass.glonass_token
    pattern = r"86\d{13}" #navtelecom
    imeis = glonass.get_glonass_imeis_from_pattern(pattern)
    print(f"Всего терминалов по патерну {pattern}: {len(imeis)}")
    user_input = input("Выберите команду: 1 - Список терминалов с ip,\n 2 - На каких терминалах какие ICCID\n")
    user_file = input("Введите имя файла: ")
    if user_input == "1":
        command = "*!READ TRANS:SRV1,SRV2,SR3 (SMS/TCP)"
        for imei in tqdm(imeis):
            try:
                data = glonass.ask_glonasssoft_terminal(imei=imei, command=command, token_glonass=glonass_token)
                if data is not None:
                    answer = data[0]["answer"]
                    ip_addresses = '176.9.36.169'
                    if ip_addresses in answer:
                        with open(f"{user_file}.txt", "a") as file:
                            file.write(f"{imei};{ip_addresses};{datetime.now()}\n")
            except Exception as e:
                print("Ошибка: ", e)
                continue
    if user_input == "2":
        command = "*?ICCID"
        for imei in tqdm(imeis):
            try:
                data = glonass.ask_glonasssoft_terminal(imei=imei, command=command, token_glonass=glonass_token)
                if data is not None:
                    answer = data[0]["answer"]
                    with open(f"{user_file}.txt", "a") as file:
                        file.write(f"{imei};{answer};{datetime.now()}\n")
            except Exception as e:
                print("Ошибка: ", e)
                continue

    else:
        print("Такой команды нет")


if __name__ == "__main__":
    job()
    sys.exit()

