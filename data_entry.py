from parser.classes import (
        OneC,
        )
from configurations import config

def get_onec_clients():
    "Отдаёт клиентов 1С"
    sun = OneC(login=str(config.ONE_C_LOGIN), password=str(config.ONE_C_PASSWORD), url=str(config.ONEC_CLIENT_URL))
    clients = sun.get_clients()["Клиенты"]
    return clients

def get_onec_contracts():
    "Отдаёт контракты 1С"
    sun = OneC(login=str(config.ONE_C_LOGIN), password=str(config.ONE_C_PASSWORD), url=str(config.ONEC_CONTRACT_URL))
    contracts = sun.get_clients()["Договоры"]
    return contracts


def get_onec_contacts():
    "Отдаёт контракты 1С"
    sun = OneC(login=str(config.ONE_C_LOGIN), password=str(config.ONE_C_PASSWORD), url=str(config.ONEC_CONTACT_URL))
    contracts = sun.get_clients()["КонтактныеЛица"]
    return contracts

# def save_json_contacts():
#     "Сохраняет json контакты"
#     sun = OneC(login=str(config.ONE_C_LOGIN), password=str(config.ONE_C_PASSWORD), url=str(config.ONEC_CONTACT_URL))
#     contracts = sun.get_clients()
#     with open('contacts_10_01_2025.json', 'w', encoding="utf-8") as f:
#         json.dump(contracts, f, ensure_ascii=False, indent=2)
#
# save_json_contacts()
    
