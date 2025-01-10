from collections.abc import ItemsView

from sqlalchemy.util import EMPTY_DICT
import database.models as models
from database.database import Database
from sqlalchemy import and_, or_, update
from datetime import datetime
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

###############################################
# Объекты в бд
################################################

def add_objects(marge_data: list):
    """ 
    Добавляет все объекты в БД из списка
    Принимает список словарей вида:
            "id_in_system": "123",
            "name": "123",
            "imei": "123456789012345",
            "owner_agent": "abc"
            #"created": "2020-01-01",
            #"updated": "2020-01-01",
            #"add_date": "2020-01-01",
            "monitor_sys_id": 1
            "object_status_id": 1
            "user": "abc"
            "parent_id": "123"
    """
    session = Database().session
    for i in marge_data:
        ca_object = models.CaObject(
            sys_mon_object_id=i["id_in_system"],
            object_name=i["name"],
            imei=i["imei"],
            owner_contragent=i["owner_agent"],
            #object_created=i["created"],
            #updated=i["updated"],
            #object_add_date=i["add_date"],
            sys_mon_id=i["monitor_sys_id"],
            object_status=i["object_status_id"],
            owner_user=i["user"],
            parent_id_sys = i["parent_id"],
        )
        session.add(ca_object)
    session.commit()
    session.close()


def add_one_object(marge_data: list):
    """ 
    Рекрусивно проверяет бд, если нет такого объекта в бд как в системе мониторинга, добавляет его в базу данных.
    Сравнивает в бд:
    1. По системе мониторинга
    2. По id объекта в системе мониторинга
    Принимает словарь вида:
            "id_in_system": "123",
            "name": "123",
            "imei": "123456789012345",
            "owner_agent": "abc"
            "created": "2020-01-01",
            "updated": "2020-01-01",
            "add_date": "2020-01-01",
            "monitor_sys_id": 1
            "object_status_id": 1
            "user": "abc"
            "parent_id": "123"
    """
    sys_id = marge_data[10]["monitor_sys_id"]
    session = Database().session
    try:
        users_logins = session.query(models.LoginUser).filter(
            models.LoginUser.system_id == sys_id,
            models.LoginUser.contragent_id != None
        )
        objects_in_db = session.query(models.CaObject.sys_mon_object_id, models.CaObject.sys_mon_id).filter(
            models.CaObject.sys_mon_id == sys_id,
        )
        all_id_from_db = set()
        for i in objects_in_db:
            all_id_from_db.add(i[0])

        for item in marge_data:
            if item["id_in_system"] not in all_id_from_db:


                contragent_id = users_logins.filter(
                    models.LoginUser.login == item["user"],
                )
                result = contragent_id.first().contragent_id if contragent_id.first() else None

                ca_object = models.CaObject(
                    sys_mon_object_id=item["id_in_system"],
                    object_name=item["name"],
                    imei=item["imei"],
                    owner_contragent=item["owner_agent"],
                    sys_mon_id=item["monitor_sys_id"],
                    object_status=item["object_status_id"],
                    owner_user=item["user"],
                    parent_id_sys = item["parent_id"],
                    contragent_id = int(result) if result else None
                )
                session.add(ca_object)
                session.commit()

                log_global(
                    section_type="object",
                    edit_id=session.query(models.CaObject.id, models.CaObject.sys_mon_object_id, models.CaObject.sys_mon_id).filter(
                        models.CaObject.sys_mon_object_id == item["id_in_system"],
                        models.CaObject.sys_mon_id == sys_id
                    ).first()[0],
                    field="name",
                    old_value="0",
                    new_value=item["name"],
                    action="add",
                    sys_id=sys_id,
                    contragent_id=int(result) if result else None
                )
                session.commit()

    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при добавлении объектов по одному БД: {ex}")
    
    finally:
        session.close()  # Закрытие сессии после завершения работы


def delete_one_object(marge_data: list):
    """
    Удаляет один объект из БД, если его нет в системе мониторинга
    Сравнивает в бд:
    1. По системе мониторинга
    2. По id объекта в системе мониторинга
    Принимает словарь вида:
            "id_in_system": "123",
            "name": "123",
            "imei": "123456789012345",
            "owner_agent": "abc"
            "created": "2020-01-01",
            "updated": "2020-01-01",
            "add_date": "2020-01-01",
            "monitor_sys_id": 1
            "object_status_id": 1
            "user": "abc"
            "parent_id": "123"
    """
    sys_id = marge_data[10]["monitor_sys_id"]
    session = Database().session
    try:
        objects_in_db = session.query(
                models.CaObject.sys_mon_object_id, 
                models.CaObject.sys_mon_id,
                models.CaObject.object_status
                ).filter(
            models.CaObject.sys_mon_id == sys_id,
            models.CaObject.object_status != 9
        )
        all_id_from_db = set()
        for i in objects_in_db:
            all_id_from_db.add(i[0])
        all_id_from_sysmon = set()
        for item in marge_data:
            all_id_from_sysmon.add(item["id_in_system"])
        for id_ in all_id_from_db:
            if id_ not in all_id_from_sysmon:
                log_global(
                    section_type="object",
                    edit_id=session.query(models.CaObject.id, models.CaObject.sys_mon_object_id, models.CaObject.sys_mon_id).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).first()[0],
                    field="name",
                    old_value=session.query(models.CaObject).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).first().object_name,
                    new_value="9",
                    action="delete",
                    sys_id=sys_id,
                    contragent_id=session.query(models.CaObject).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).first().contragent_id
                )

                session.execute(
                        update(models.CaObject).where(
                            models.CaObject.sys_mon_object_id == id_,
                            models.CaObject.sys_mon_id == sys_id
                            ).values(
                                object_status = 9
                            )
                            )
        session.commit()

    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при удалении объектов по одному БД: {ex}")
    
    finally:
        session.close()  # Закрытие сессии после завершения работы


def update_one_object(marge_data: list):
    """
    Обновляет один объект в БД, если произошли изменения в системе мониторинга
    Сравнивает в бд:
    1. По системе мониторинга
    2. По id объекта в системе мониторинга
    Принимает словарь вида:
            "id_in_system": "123",
            "name": "123",
            "imei": "123456789012345",
            "owner_agent": "abc"
            "created": "2020-01-01",
            "updated": "2020-01-01",
            "add_date": "2020-01-01",
            "monitor_sys_id": 1
            "object_status_id": 1
            "user": "abc"
            "parent_id": "123"
    """
    sys_id = marge_data[10]["monitor_sys_id"]

    for i in marge_data:
        session = Database().session
        try:
            objects_in_db = session.query(models.CaObject).filter(
                models.CaObject.sys_mon_id == sys_id        
            )
            

            users_logins = session.query(models.LoginUser).filter(
                models.LoginUser.system_id == sys_id,
                models.LoginUser.contragent_id != None
            )

            for e in objects_in_db:
                if i["id_in_system"] == e.sys_mon_object_id:

                    contr_id = users_logins.filter(
                        models.LoginUser.login == i["user"],
                        )
                    result = contr_id.first().contragent_id if contr_id.first() else None

                    if i["name"] != e.object_name:
                        log_global(
                                section_type="object",
                                edit_id = e.id, 
                                field = "name", 
                                old_value = e.object_name,
                                new_value = i["name"], 
                                action = "update", 
                                sys_id = int(i["monitor_sys_id"]),
                                contragent_id = result
                                )
                        session.execute(
                                update(models.CaObject)
                                .where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"])
                                .values(object_name = i["name"]))
                        session.commit()


                    if str(i["imei"]) != str(e.imei):
                        log_global(section_type="object", edit_id = e.id, field = "imei", old_value = str(e.imei), new_value = str(i["imei"]), action = "update", sys_id = int(i["monitor_sys_id"]))
                        session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(imei = str(i["imei"])))
                        session.commit()


                    if i["owner_agent"] != e.owner_contragent:
                        log_global(section_type="object", edit_id = e.id, field = "owner_agent", old_value = e.owner_contragent, new_value = i["owner_agent"], action = "update", sys_id = int(i["monitor_sys_id"]))
                        session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(owner_contragent = i["owner_agent"]))
                        session.commit()


                    if i["object_status_id"] != e.object_status:
                        log_global(
                                section_type="object",
                                edit_id = e.id, 
                                field = "object_status_id",
                                old_value = e.object_status,
                                new_value = i["object_status_id"],
                                action = "update", 
                                sys_id = int(i["monitor_sys_id"]),
                                contragent_id = result,
                                )
                        session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_status = i["object_status_id"]))
                        session.commit()


                    if i["user"] != e.owner_user:
                        log_global(
                                section_type="object", 
                                edit_id = e.id, 
                                field = "owner_user",
                                old_value = e.owner_user,
                                new_value = i["user"],
                                action = "update",
                                sys_id = int(i["monitor_sys_id"])
                                )
                        session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(owner_user = i["user"]))
                        session.commit()


                    if str(i["parent_id"]) != str(e.parent_id_sys):
                        log_global(section_type="object", edit_id = e.id, field = "parent_id", old_value = e.parent_id_sys, new_value = i["parent_id"], action = "update", sys_id = int(i["monitor_sys_id"]))
                        session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(parent_id_sys = i["parent_id"]))
                        session.commit()


                    if result != e.contragent_id:
                        log_global(section_type="object", edit_id = e.id, field = "contragent_id", old_value = e.contragent_id, new_value = result, action = "update", sys_id = int(i["monitor_sys_id"]))
                        session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(contragent_id = result))
                        session.commit()

                    if "contragent_id" in i:
                        if int(i["contragent_id"]) != e.contragent_id:
                            log_global(section_type="object", edit_id = e.id, field = "contragent_id", old_value = e.contragent_id, new_value = int(i["contragent_id"]), action = "update", sys_id = int(i["monitor_sys_id"]))
                            session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(contragent_id = int(i["contragent_id"])))
                            session.commit()

        except Exception as ex:
            session.rollback()  # Откат транзакции в случае ошибки
            logger.error(f"Ошибка при Обновлении объектов по одному БД: {ex}")
        
        finally:
            session.close()  # Закрытие сессии после завершения работы


###################
# Клиенты
###################



def add_sys_mon_clients(clients):
    """
    Массово добавляет клиентов в БД из системы мониторинга
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["name"])
        marge["owner_id_sys_mon"] = str(i["owner"])
        marge["system_monitor_id"] = 1

    """
    session = Database().session
    try:
        for i in clients:
            client = models.ClientsInSystemMonitor(
                id_in_system_monitor=i["id_in_system_monitor"],
                name_in_system_monitor=i["name_in_system_monitor"],
                owner_id_sys_mon=i["owner_id_sys_mon"],
                system_monitor_id=i["system_monitor_id"]
            )
            session.add(client)
        session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Добавлении клиентов по одному БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы

def add_one_sys_mon_client(clients):
    """
    Рекрусивно проверяет и Добавляет клиентов в бд если их не было в соответствии с системой мониторинга
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["name"])
        marge["owner_id_sys_mon"] = str(i["owner"])
        marge["system_monitor_id"] = 1

    """
    sys_id = clients[10]["system_monitor_id"]
    session = Database().session
    try:
        clients_in_db = session.query(models.ClientsInSystemMonitor.id_in_system_monitor, models.ClientsInSystemMonitor.system_monitor_id).filter(
            models.ClientsInSystemMonitor.system_monitor_id == sys_id,
        )
        all_id_from_db = set()
        for i in clients_in_db:
            all_id_from_db.add(i[0])

        for item in clients:
            if item["id_in_system_monitor"] not in all_id_from_db:
                client = models.ClientsInSystemMonitor(
                    id_in_system_monitor=item["id_in_system_monitor"],
                    name_in_system_monitor=item["name_in_system_monitor"],
                    owner_id_sys_mon=item["owner_id_sys_mon"],
                    system_monitor_id=item["system_monitor_id"]
                )
                session.add(client)
        session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Добавлении клиентов по одному БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы


def update_one_sys_mon_client(clients):
    """
    Рекрусивно обновляет клиентов в бд в соответствии с системой мониторинга
    Сравнивает в бд:
    1. По системе мониторинга
    2. По id клиента в системе мониторинга
    Принимает словарь вида:
            "id_in_system_monitor": "123",
            "name_in_system_monitor": "123",
            "owner_id_sys_mon": "123",
            "system_monitor_id": 1
    """
    sys_id = clients[10]["system_monitor_id"]
    session = Database().session
    try:
        clients_in_db = session.query(models.ClientsInSystemMonitor).filter(
            models.ClientsInSystemMonitor.system_monitor_id == sys_id        
        )
        for i in clients:
            for e in clients_in_db:
                if i["id_in_system_monitor"] == e.id_in_system_monitor:
                    if i["name_in_system_monitor"] != e.name_in_system_monitor:
                        session.execute(update(models.ClientsInSystemMonitor).where(models.ClientsInSystemMonitor.id_in_system_monitor == i["id_in_system_monitor"]).values(name_in_system_monitor = i["name_in_system_monitor"]))
                    if i["owner_id_sys_mon"] != e.owner_id_sys_mon:
                        session.execute(update(models.ClientsInSystemMonitor).where(models.ClientsInSystemMonitor.id_in_system_monitor == i["id_in_system_monitor"]).values(owner_id_sys_mon = i["owner_id_sys_mon"]))
        session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Обновлении клиентов по одному БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы


def delete_one_sys_mon_client(clients):
    """
    Удаляет клиентов из бд в соответствии с системой мониторинга
    Сравнивает в бд:
    1. По системе мониторинга
    2. По id клиента в системе мониторинга
    Принимает словарь вида:
            "id_in_system_monitor": "123",
            "name_in_system_monitor": "123",
            "owner_id_sys_mon": "123",
            "system_monitor_id": 1
    """
    sys_id = clients[10]["system_monitor_id"]
    session = Database().session
    try:
        clients_in_db = session.query(models.ClientsInSystemMonitor.id_in_system_monitor, models.ClientsInSystemMonitor.system_monitor_id).filter(
            models.ClientsInSystemMonitor.system_monitor_id == sys_id        
        )
        all_id_from_db = set()
        for i in clients_in_db:
            all_id_from_db.add(i[0])
        all_id_from_sys_mon = set()
        for i in clients:
            all_id_from_sys_mon.add(i["id_in_system_monitor"])
        for id_ in all_id_from_db:
            if id_ not in all_id_from_sys_mon:
                session.query(models.ClientsInSystemMonitor).filter(models.ClientsInSystemMonitor.id_in_system_monitor == id_).filter(models.ClientsInSystemMonitor.system_monitor_id == sys_id).delete()
        session.commit()
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Удалении клиентов по одному БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы


###################
# Users in db 
###################

def get_db_users_from_sysem(system_id: int):
    session = Database().session
    try:
        users = session.query(models.LoginUser.system_id, models.LoginUser.login, models.LoginUser.client_name).filter(models.LoginUser.system_id == system_id).all()
        session.close()
        return users
    except Exception as ex:
        session.rollback()  # Откат транзакции в случае ошибки
        logger.error(f"Ошибка при Удалении клиентов по одному БД: {ex}")
    finally:
        session.close()  # Закрытие сессии после завершения работы


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
