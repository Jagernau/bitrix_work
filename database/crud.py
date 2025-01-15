import database.models as models
from database.database import Database
from sqlalchemy import update
from database.logging_crud import log_global

import logging

# Создание и настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создание обработчика для записи в файл
file_handler = logging.FileHandler('log_db.txt')
file_handler.setLevel(logging.INFO)

# Создание форматировщика
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)

###################
# 1C
###################

def add_all_clients_oneC(clients):
    """
    Добавляет клиентов в БД MySQL из 1С 
    "Наименование",
    "НаименованиеПолное",
    "ЮрФизЛицо",
    "ИНН",
    "КПП",
    "НаправлениеБизнеса",
    "УникальныйИдентификаторКлиента",
    "ДатаРегистрации",
    "ОсновнойМенеджер",
    "ФактическийАдрес1",
    "ЮридическийАдрес1",
    "Телефон"
    """
    session = Database().session
    try:
        for i in clients:
            client = models.Contragent(
                ca_name=i["НаименованиеПартнер"].replace('\xa0', ' '),
                ca_shortname=i["НаименованиеПолноеПартнер"].replace('\xa0', ' '),
                ca_type=i["ЮрФизЛицоПартнер"].replace('\xa0', ' '),
                ca_inn=i["ИНН"],
                ca_kpp=i["КПП"],
                ca_field_of_activity = i["НаправлениеБизнеса"],
                unique_onec_id = i["УникальныйИдентификаторПартнера"],
                registration_date = i["ДатаРегистрации"].split("T")[0],
                key_manager = i["ОсновнойМенеджер"],
                actual_address = i["ФактическийАдрес1"],
                registered_office = i["ЮридическийАдрес1"],
                phone = i["Телефон"],
                ca_uid_contragent = i["УникальныйИдентификаторКонтрагента"],
                ca_name_contragent = i["НаименованиеКонтрагент"]
            )
            session.add(client)
        session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Добавлении клиентов по БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы

def add_one_oneC_clients(clients):
    """ 
    Запись в БД_2 конрагентов полученных из 1С
    """
    session = Database().session
    try:
        clients_in_db = session.query(models.Contragent.ca_uid_contragent).filter(models.Contragent.ca_uid_contragent != None).all()
        all_id_from_db = set()
        for i in clients_in_db:
            all_id_from_db.add(i[0])
        for item in clients:
            if item["УникальныйИдентификаторКонтрагента"] not in all_id_from_db:
                one_client = models.Contragent(
                    ca_name=item["НаименованиеПартнер"].replace('\xa0', ' '),
                    ca_shortname=item["НаименованиеПолноеПартнер"].replace('\xa0', ' '),
                    ca_type=item["ЮрФизЛицоПартнер"].replace('\xa0', ' '),
                    ca_inn=item["ИНН"],
                    ca_kpp=item["КПП"],
                    ca_field_of_activity = item["НаправлениеБизнеса"],
                    unique_onec_id = item["УникальныйИдентификаторПартнера"],
                    registration_date = item["ДатаРегистрации"].split("T")[0],
                    key_manager = item["ОсновнойМенеджер"],
                    actual_address = item["ФактическийАдрес1"],
                    registered_office = item["ЮридическийАдрес1"],
                    phone = item["Телефон"],
                    ca_uid_contragent = item["УникальныйИдентификаторКонтрагента"],
                    ca_name_contragent = item["НаименованиеКонтрагент"],
                    service_manager = item["СервисныйМенеджер"]
                )
                session.add(one_client)
                session.commit()
                
                log_global(
                    section_type="1С_client",
                    edit_id=session.query(models.Contragent.ca_id, models.Contragent.ca_uid_contragent).filter(models.Contragent.ca_uid_contragent == item["УникальныйИдентификаторКонтрагента"]).first()[0],
                    field="ca_name",
                    old_value="0",
                    new_value=item["НаименованиеПартнер"].replace('\xa0', ' '),
                    action="add",
                    sys_id=0,
                )
                session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Добавлении клиентов по БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы
    
def delete_one_oneC_client(clients):
    session = Database().session
    try:
        db_clients = session.query(models.Contragent.unique_onec_id).all()
        all_id_db_clients = set()
        for i in db_clients:
            all_id_db_clients.add(i[0])
        all_id_oneC = set()
        for item in clients:
            all_id_oneC.add(item["УникальныйИдентификаторПартнера"])
        for id_ in all_id_db_clients:
            if id_ not in all_id_oneC:
                session.query(models.Contragent).filter(models.Contragent.unique_onec_id == id_).delete()

        session.commit()

    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Удалении клиентов по БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы

def update_one_oneC_client(clients):
    for i in clients:
        session = Database().session
        try:
            clients_in_db = session.query(models.Contragent)
            for e in clients_in_db:
                if i["УникальныйИдентификаторКонтрагента"] == e.ca_uid_contragent:

                    if str(e.ca_name).replace('\xa0', ' ') != i["НаименованиеПартнер"].replace('\xa0', ' '):
                        log_global(section_type="1С_client",
                                   edit_id=e.ca_id, 
                                   field='ca_name', 
                                   old_value=e.ca_name, 
                                   new_value=i["НаименованиеПартнер"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_name = i["НаименованиеПартнер"].replace('\xa0', ' ')))
                        session.commit()

                    if str(e.ca_shortname).replace('\xa0', ' ') != i["НаименованиеПолноеПартнер"].replace('\xa0', ' '):
                        log_global(section_type="1С_client",
                                   action="update", 
                                   sys_id=0, 
                                   edit_id=e.ca_id, 
                                   field='ca_shortname', 
                                   old_value=e.ca_shortname, 
                                   new_value=i["НаименованиеПолноеПартнер"].replace('\xa0', ' '))
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_shortname = i["НаименованиеПолноеПартнер"].replace('\xa0', ' ')))
                        session.commit()

                    if str(e.ca_type).replace('\xa0', ' ') != i["ЮрФизЛицоПартнер"].replace('\xa0', ' '):
                        log_global(
                                section_type="1С_client", 
                                action="update", 
                                sys_id=0,
                                edit_id=e.ca_id, 
                                field='ca_type', 
                                old_value=e.ca_type,
                                new_value=i["ЮрФизЛицоПартнер"].replace('\xa0', ' '))
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_type = i["ЮрФизЛицоПартнер"].replace('\xa0', ' ')))
                        session.commit()

                    if e.ca_inn != i["ИНН"]:
                        log_global(
                                section_type="1С_client",
                                action="update", 
                                sys_id=0, 
                                edit_id=e.ca_id,
                                field='ca_inn',
                                old_value=e.ca_inn,
                                new_value=i["ИНН"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_inn = i["ИНН"]))
                        session.commit()

                    if e.ca_kpp != i["КПП"]:
                        log_global(
                                section_type="1С_client",
                                action="update", 
                                sys_id=0, 
                                edit_id=e.ca_id,
                                field='ca_kpp',
                                old_value=e.ca_kpp,
                                new_value=i["КПП"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_kpp = i["КПП"]))
                        session.commit()

                    if e.ca_field_of_activity != i["НаправлениеБизнеса"]:
                        log_global(
                                section_type="1С_client",
                                action="update",
                                sys_id=0,
                                edit_id=e.ca_id,
                                field='ca_field_of_activity',
                                old_value=e.ca_field_of_activity,
                                new_value=i["НаправлениеБизнеса"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_field_of_activity = i["НаправлениеБизнеса"]))
                        session.commit()

                    if e.key_manager != i["ОсновнойМенеджер"]:
                        log_global(
                                section_type="1С_client", 
                                action="update",
                                sys_id=0, 
                                edit_id=e.ca_id, 
                                field='key_manager',
                                old_value=e.key_manager,
                                new_value=i["ОсновнойМенеджер"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(key_manager = i["ОсновнойМенеджер"]))
                        session.commit()

                    if e.actual_address != i["ФактическийАдрес1"]:
                        log_global(
                                section_type="1С_client",
                                action="update",
                                sys_id=0,
                                edit_id=e.ca_id,
                                field='actual_address',
                                old_value=e.actual_address,
                                new_value=i["ФактическийАдрес1"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(actual_address = i["ФактическийАдрес1"]))
                        session.commit()

                    if e.registered_office != i["ЮридическийАдрес1"]:
                        log_global(
                                section_type="1С_client",
                                action="update",
                                sys_id=0,
                                edit_id=e.ca_id,
                                field='registered_office',
                                old_value=e.registered_office,
                                new_value=i["ЮридическийАдрес1"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(registered_office = i["ЮридическийАдрес1"]))
                        session.commit()

                    if e.unique_onec_id != i["УникальныйИдентификаторПартнера"]:
                        log_global(
                                section_type="1C_client",
                                action="update",
                                sys_id=0,
                                edit_id=e.ca_id,
                                field='unique_onec_id',
                                old_value=e.unique_onec_id,
                                new_value=i["УникальныйИдентификаторПартнера"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(unique_onec_id = i["УникальныйИдентификаторПартнера"]))
                        session.commit()

                    if e.ca_name_contragent != i["НаименованиеКонтрагент"]:
                        log_global(
                                section_type="1C_client", 
                                action="update", 
                                sys_id=0, 
                                edit_id=e.ca_id,
                                field='ca_name_contragent', 
                                old_value=e.ca_name_contragent,
                                new_value=i["НаименованиеКонтрагент"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(ca_name_contragent = i["НаименованиеКонтрагент"]))
                        session.commit()

                    if e.service_manager != i["СервисныйМенеджер"]:
                        log_global(
                                section_type="1C_client", 
                                action="update", 
                                sys_id=0, 
                                edit_id=e.ca_id,
                                field='service_manager', 
                                old_value=e.service_manager,
                                new_value=i["СервисныйМенеджер"])
                        session.execute(
                                update(models.Contragent)
                                .where(models.Contragent.ca_uid_contragent == i["УникальныйИдентификаторКонтрагента"])
                                .values(service_manager = i["СервисныйМенеджер"]))
                        session.commit()

        except Exception as ex:
            session.rollback()  # Откат транзакции в случае ошибки
            logger.error(f"Ошибка при Обновлении клиентов по БД: {ex}")
        finally:
            session.close()  # Закрытие сессии после завершения работы


def get_db_contragents(str_name):
    session = Database().session
    try:
        result = session.query(models.Contragent).filter(models.Contragent.ca_name == str_name).first()
        if result:
            return result.ca_id
        else:
            return None
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Отдачи клиентов из БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы

#####################################
# КОНТРАКТЫ
#####################################

def add_all_contracts_oneC(clients):
    """
    Добавляет Контракты в БД MySQL из 1С 
    """
    session = Database().session
    try:
        for i in clients:
            client = models.OnecContract(
                name_contract = i["НаименованиеДоговора"],
                contract_number = i["НомерДоговора"],
                contract_date = i["ДатаДоговора"].split("T")[0],
                contract_status = i["Статус"],
                organization = i["Организация"].replace('\xa0', ' '),
                partner = i["Партнер"].replace('\xa0', ' '),
                counterparty = i["Контрагент"].replace('\xa0', ' '),
                contract_commencement_date = i["ДатаНачалаДействия"].split("T")[0],
                contract_expiration_date = i["ДатаОкончанияДействия"].split("T")[0],
                contract_purpose = i["Цель"],
                type_calculations = i["ВидРасчетов"],
                category = i["Категория"],
                manager = i["Менеджер"],
                subdivision = i["Подразделение"],
                contact_person = i["КонтактноеЛицо"],
                organization_bank_account = i["БанковскийСчетОрганизации"],
                counterparty_bank_account = i["БанковскийСчетКонтрагента"],
                detailed_calculations = i["ДетализацияРасчетов"],
                unique_partner_identifier = i["УникальныйИдентификаторПартнера"],
                unique_counterparty_identifier = i["УникальныйИдентификаторКонтрагента"],
                unique_contract_identifier = i["УникальныйИдентификаторДоговораКонтрагента"]
            )
            session.add(client)
            session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Создании контрактов в БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы

def add_one_oneC_contracts(contracts):
    """ 
    Запись в БД_2 договоров полученных из 1С
    """
    session = Database().session
    try:
        contract_in_db = session.query(models.OnecContract.unique_contract_identifier).filter(models.OnecContract.unique_contract_identifier != None).all()
        all_id_from_db = set()
        for i in contract_in_db:
            all_id_from_db.add(i[0])
        for item in contracts:
            if item["УникальныйИдентификаторДоговораКонтрагента"] not in all_id_from_db:
                one_contract = models.OnecContract(
                    name_contract = item["НаименованиеДоговора"],
                    contract_number = item["НомерДоговора"],
                    contract_date = item["ДатаДоговора"].split("T")[0],
                    contract_status = item["Статус"],
                    organization = item["Организация"].replace('\xa0', ' '),
                    partner = item["Партнер"].replace('\xa0', ' '),
                    counterparty = item["Контрагент"].replace('\xa0', ' '),
                    contract_commencement_date = item["ДатаНачалаДействия"].split("T")[0],
                    contract_expiration_date = item["ДатаОкончанияДействия"].split("T")[0],
                    contract_purpose = item["Цель"],
                    type_calculations = item["ВидРасчетов"],
                    category = item["Категория"],
                    manager = item["Менеджер"],
                    subdivision = item["Подразделение"],
                    contact_person = item["КонтактноеЛицо"],
                    organization_bank_account = item["БанковскийСчетОрганизации"],
                    counterparty_bank_account = item["БанковскийСчетКонтрагента"],
                    detailed_calculations = item["ДетализацияРасчетов"],
                    unique_partner_identifier = item["УникальныйИдентификаторПартнера"],
                    unique_counterparty_identifier = item["УникальныйИдентификаторКонтрагента"],
                    unique_contract_identifier = i["УникальныйИдентификаторДоговораКонтрагента"]
                )
                session.add(one_contract)
                session.commit()
                
                log_global(
                    section_type="1С_contract",
                    edit_id=session.query(models.OnecContract.contract_id, models.OnecContract.unique_contract_identifier).filter(models.OnecContract.unique_contract_identifier == item["УникальныйИдентификаторДоговораКонтрагента"]).first()[0],
                    field="name_contract",
                    old_value="0",
                    new_value=item["НаименованиеДоговора"].replace('\xa0', ' '),
                    action="add",
                    sys_id=0,
                )
                session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Создании контракта по одному в БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы

def update_one_oneC_contracts(contracts):
    
    for i in contracts:
        session = Database().session
        try:
            contracts_in_db = session.query(models.OnecContract)
            for e in contracts_in_db:
                if i["УникальныйИдентификаторДоговораКонтрагента"] == e.unique_contract_identifier:
                    # name_contract = item["НаименованиеДоговора"]

                    if str(e.name_contract).replace('\xa0', ' ') != i["НаименованиеДоговора"].replace('\xa0', ' '):
                        log_global(section_type="1С_contract",
                                   edit_id=e.contract_id, 
                                   field='name_contract', 
                                   old_value=e.name_contract, 
                                   new_value=i["НаименованиеДоговора"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(name_contract = i["НаименованиеДоговора"].replace('\xa0', ' ')))
                        session.commit()

                    # contract_number = item["НомерДоговора"]
                    if str(e.contract_number).replace('\xa0', ' ') != i["НомерДоговора"].replace('\xa0', ' '):
                        log_global(section_type="1С_contract",
                                   action="update", 
                                   sys_id=0, 
                                   edit_id=e.contract_id, 
                                   field='contract_number', 
                                   old_value=e.contract_number, 
                                   new_value=i["НомерДоговора"].replace('\xa0', ' '))
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(contract_number = i["НомерДоговора"].replace('\xa0', ' ')))
                        session.commit()

                    # contract_date = item["ДатаДоговора"].split("T")[0]
                    if str(e.contract_date).split("T")[0] != str(i["ДатаДоговора"]).split("T")[0]:
                        log_global(
                                section_type="1С_contract", 
                                action="update", 
                                sys_id=0,
                                edit_id=e.contract_id, 
                                field='contract_date', 
                                old_value=e.contract_date,
                                new_value=str(i["ДатаДоговора"]).split("T")[0])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(contract_date = str(i["ДатаДоговора"]).split("T")[0]))
                        session.commit()

                    # contract_status = item["Статус"]
                    if e.contract_status != i["Статус"]:
                        log_global(
                                section_type="1С_contract",
                                action="update", 
                                sys_id=0, 
                                edit_id=e.contract_id,
                                field='contract_status',
                                old_value=e.contract_status,
                                new_value=i["Статус"])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(contract_status = i["Статус"]))
                        session.commit()

                    # organization = item["Организация"].replace('\xa0', ' ')
                    if e.organization.replace('\xa0', ' ') != i["Организация"].replace('\xa0', ' '):
                        log_global(
                                section_type="1С_contract",
                                action="update", 
                                sys_id=0, 
                                edit_id=e.contract_id,
                                field='organization',
                                old_value=e.organization.replace('\xa0', ' '),
                                new_value=i["Организация"].replace('\xa0', ' '))
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(organization = i["Организация"].replace('\xa0', ' ')))
                        session.commit()

                    # partner = item["Партнер"].replace('\xa0', ' ')
                    if e.partner.replace('\xa0', ' ') != i["Партнер"].replace('\xa0', ' '):
                        log_global(
                                section_type="1С_contract",
                                action="update",
                                sys_id=0,
                                edit_id=e.contract_id,
                                field='partner',
                                old_value=e.partner.replace('\xa0', ' '),
                                new_value=i["Партнер"])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(partner = i["Партнер"].replace('\xa0', ' ')))
                        session.commit()

                    # counterparty = item["Контрагент"].replace('\xa0', ' ')
                    if e.counterparty.replace('\xa0', ' ') != i["Контрагент"].replace('\xa0', ' '):
                        log_global(
                                section_type="1С_contract", 
                                action="update",
                                sys_id=0, 
                                edit_id=e.contract_id, 
                                field='counterparty',
                                old_value=e.counterparty,
                                new_value=i["Контрагент"].replace('\xa0', ' '))
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(counterparty = i["Контрагент"].replace('\xa0', ' ')))
                        session.commit()

                    # contract_commencement_date = item["ДатаНачалаДействия"].split("T")[0]
                    if str(e.contract_commencement_date).split("T")[0] != str(i["ДатаНачалаДействия"]).split("T")[0]:
                        log_global(
                                section_type="1С_contract",
                                action="update",
                                sys_id=0,
                                edit_id=e.contract_id,
                                field='contract_commencement_date',
                                old_value=e.contract_commencement_date,
                                new_value=str(i["ДатаНачалаДействия"]).split("T")[0])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(contract_commencement_date = str(i["ДатаНачалаДействия"]).split("T")[0]))
                        session.commit()

                    # contract_expiration_date = item["ДатаОкончанияДействия"].split("T")[0]
                    if str(e.contract_expiration_date).split("T")[0] != str(i["ДатаОкончанияДействия"]).split("T")[0]:
                        log_global(
                                section_type="1С_contract",
                                action="update",
                                sys_id=0,
                                edit_id=e.contract_id,
                                field='contract_expiration_date',
                                old_value=e.contract_expiration_date,
                                new_value=str(i["ДатаОкончанияДействия"]).split("T")[0])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(contract_expiration_date = str(i["ДатаОкончанияДействия"]).split("T")[0]))
                        session.commit()

                    # contract_purpose = item["Цель"]
                    if e.contract_purpose != i["Цель"]:
                        log_global(
                                section_type="1C_contract",
                                action="update",
                                sys_id=0,
                                edit_id=e.contract_id,
                                field='contract_purpose',
                                old_value=e.contract_purpose,
                                new_value=i["Цель"])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(contract_purpose = i["Цель"]))
                        session.commit()

                    # type_calculations = item["ВидРасчетов"]
                    if e.type_calculations != i["ВидРасчетов"]:
                        log_global(
                                section_type="1C_contract", 
                                action="update", 
                                sys_id=0, 
                                edit_id=e.contract_id,
                                field='type_calculations', 
                                old_value=e.type_calculations,
                                new_value=i["ВидРасчетов"])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(type_calculations = i["ВидРасчетов"]))
                        session.commit()

                    # category = item["Категория"]
                    if e.category != i["Категория"]:
                        log_global(
                                section_type="1C_contract", 
                                action="update", 
                                sys_id=0, 
                                edit_id=e.contract_id,
                                field='category', 
                                old_value=e.category,
                                new_value=i["Категория"])
                        session.execute(
                                update(models.OnecContract)
                                .where(models.OnecContract.unique_contract_identifier == i["УникальныйИдентификаторДоговораКонтрагента"])
                                .values(category = i["Категория"]))
                        session.commit()

        except Exception as ex:
            session.rollback()  # Откат транзакции в случае ошибки
            logger.error(f"Ошибка при обновлении контрактов: {ex}")
        
        finally:
            session.close()  # Закрытие сессии после завершения работы

#####################################
# КОНТАКТЫ
#####################################

def add_all_contacts_oneC(clients):
    """
    Добавляет Контакты в БД MySQL из 1С 
    """
    session = Database().session
    try:
        for i in clients:
            contact = models.OnecContact(
                surname = i['Фамилия'],
                name = i['Имя'],
                patronymic = i['Отчество'],
                position = i['Должность'],
                phone = i['Телефон'],
                mobiletelephone = i['МобТелефон'],
                email = i['ЭлПочта'],
                unique_partner_identifier = i['УникальныйИдентификаторПартнера'],
                unique_contact_identifier = i['УникальныйИдентификаторКонтактногоЛица']
            )
            session.add(contact)
            session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Создании контактов в БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы


def add_one_oneC_contacts(contacts):
    """ 
    Запись в БД_2 контактов полученных из 1С
    """
    session = Database().session
    try:
        contact_in_db = session.query(models.OnecContact.unique_contact_identifier).filter(models.OnecContact.unique_contact_identifier != None).all()
        all_id_from_db = set()
        for i in contact_in_db:
            all_id_from_db.add(i[0])
        for item in contacts:
            if item["УникальныйИдентификаторКонтактногоЛица"] not in all_id_from_db:
                one_contact = models.OnecContact(
                    surname = item['Фамилия'],
                    name = item['Имя'],
                    patronymic = item['Отчество'],
                    position = item['Должность'],
                    phone = item['Телефон'],
                    mobiletelephone = item['МобТелефон'],
                    email = item['ЭлПочта'],
                    unique_partner_identifier = item['УникальныйИдентификаторПартнера'],
                    unique_contact_identifier = item['УникальныйИдентификаторКонтактногоЛица']
                )
                session.add(one_contact)
                session.commit()
                
                log_global(
                    section_type="1С_contact",
                    edit_id=session.query(models.OnecContact.contact_id, models.OnecContact.unique_contact_identifier).filter(models.OnecContact.unique_contact_identifier == item['УникальныйИдентификаторКонтактногоЛица']).first()[0],
                    field="surname",
                    old_value="0",
                    new_value=item["surname"].replace('\xa0', ' '),
                    action="add",
                    sys_id=0,
                )
                session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Создании контракта по одному в БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы


def update_one_oneC_contacts(contacts):
    "Обновление контактов по одному" 
    for i in contacts:
        session = Database().session
        try:
            contacts_in_db = session.query(models.OnecContact)
            for e in contacts_in_db:
                if i['УникальныйИдентификаторКонтактногоЛица'] == e.unique_contact_identifier:
                    # surname = item['Фамилия']

                    if str(e.surname).replace('\xa0', ' ') != i["Фамилия"].replace('\xa0', ' '):
                        log_global(section_type="1С_contact",
                                   edit_id=e.contact_id, 
                                   field='surname', 
                                   old_value=e.surname, 
                                   new_value=i["Фамилия"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContact)
                                .where(models.OnecContact.unique_contact_identifier == i["УникальныйИдентификаторКонтактногоЛица"])
                                .values(surname = i["Фамилия"].replace('\xa0', ' ')))
                        session.commit()

                    # name = item['Имя']
                    if str(e.name).replace('\xa0', ' ') != i["Имя"].replace('\xa0', ' '):
                        log_global(section_type="1С_contact",
                                   edit_id=e.contact_id, 
                                   field='name', 
                                   old_value=e.name, 
                                   new_value=i["Имя"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContact)
                                .where(models.OnecContact.unique_contact_identifier == i["УникальныйИдентификаторКонтактногоЛица"])
                                .values(name = i["Имя"].replace('\xa0', ' ')))
                        session.commit()

                    # patronymic = item['Отчество']
                    if str(e.patronymic).replace('\xa0', ' ') != i["Отчество"].replace('\xa0', ' '):
                        log_global(section_type="1С_contact",
                                   edit_id=e.contact_id, 
                                   field='patronymic', 
                                   old_value=e.patronymic, 
                                   new_value=i["Отчество"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContact)
                                .where(models.OnecContact.unique_contact_identifier == i["УникальныйИдентификаторКонтактногоЛица"])
                                .values(patronymic = i["Отчество"].replace('\xa0', ' ')))
                        session.commit()


                    # phone = item['Телефон']
                    if str(e.phone).replace('\xa0', ' ') != i["Телефон"].replace('\xa0', ' '):
                        log_global(section_type="1С_contact",
                                   edit_id=e.contact_id, 
                                   field='phone', 
                                   old_value=e.phone, 
                                   new_value=i["Телефон"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContact)
                                .where(models.OnecContact.unique_contact_identifier == i["УникальныйИдентификаторКонтактногоЛица"])
                                .values(phone = i["Телефон"].replace('\xa0', ' ')))
                        session.commit()


                    # mobiletelephone = item['МобТелефон']
                    if str(e.mobiletelephone).replace('\xa0', ' ') != i["МобТелефон"].replace('\xa0', ' '):
                        log_global(section_type="1С_contact",
                                   edit_id=e.contact_id, 
                                   field='mobiletelephone', 
                                   old_value=e.mobiletelephone, 
                                   new_value=i["МобТелефон"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContact)
                                .where(models.OnecContact.unique_contact_identifier == i["УникальныйИдентификаторКонтактногоЛица"])
                                .values(mobiletelephone = i["МобТелефон"].replace('\xa0', ' ')))
                        session.commit()


                    # email = item['ЭлПочта']
                    if str(e.email).replace('\xa0', ' ') != i["ЭлПочта"].replace('\xa0', ' '):
                        log_global(section_type="1С_contact",
                                   edit_id=e.contact_id, 
                                   field='email', 
                                   old_value=e.email, 
                                   new_value=i["ЭлПочта"].replace('\xa0', ' '),
                                   action="update", 
                                   sys_id=0) 
                        session.execute(
                                update(models.OnecContact)
                                .where(models.OnecContact.unique_contact_identifier == i["УникальныйИдентификаторКонтактногоЛица"])
                                .values(email = i["ЭлПочта"].replace('\xa0', ' ')))
                        session.commit()

        except Exception as ex:
            session.rollback()  # Откат транзакции в случае ошибки
            logger.error(f"Ошибка при обновлении контрактов: {ex}")
        
        finally:
            session.close()  # Закрытие сессии после завершения работы
