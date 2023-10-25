import database.models as models
from database.database import Database
from sqlalchemy import and_, or_, update
from datetime import datetime



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
            "created": "2020-01-01",
            "updated": "2020-01-01",
            "add_date": "2020-01-01",
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
            object_created=i["created"],
            updated=i["updated"],
            object_add_date=i["add_date"],
            sys_mon_id=i["monitor_sys_id"],
            object_status=i["object_status_id"],
            owner_user=i["user"],
            parent_id_sys = i["parent_id"]
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
    objects_in_db = session.query(models.CaObject.sys_mon_object_id, models.CaObject.sys_mon_id).filter(
        models.CaObject.sys_mon_id == sys_id,
    )
    all_id_from_db = set()
    for i in objects_in_db:
        all_id_from_db.add(i[0])

    for item in marge_data:
        if item["id_in_system"] not in all_id_from_db:
            ca_object = models.CaObject(
                sys_mon_object_id=item["id_in_system"],
                object_name=item["name"],
                imei=item["imei"],
                owner_contragent=item["owner_agent"],
                object_created=item["created"],
                updated=item["updated"],
                object_add_date=item["add_date"],
                sys_mon_id=item["monitor_sys_id"],
                object_status=item["object_status_id"],
                owner_user=item["user"],
                parent_id_sys = item["parent_id"]

            )
            session.add(ca_object)
    session.commit()
    session.close()


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
    objects_in_db = session.query(models.CaObject.sys_mon_object_id, models.CaObject.sys_mon_id).filter(
        models.CaObject.sys_mon_id == sys_id,
    )
    all_id_from_db = set()
    for i in objects_in_db:
        all_id_from_db.add(i[0])
    all_id_from_sysmon = set()
    for item in marge_data:
        all_id_from_sysmon.add(item["id_in_system"])
    for id_ in all_id_from_db:
        if id_ not in all_id_from_sysmon:
            session.query(models.CaObject).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).delete()
    session.commit()
    session.close()

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
    session = Database().session
    objects_in_db = session.query(models.CaObject).filter(
        models.CaObject.sys_mon_id == sys_id        
    )
    for i in marge_data:
      
        for e in objects_in_db:
            if i["id_in_system"] == e.sys_mon_object_id:
                if i["name"] != e.object_name:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_name = i["name"]))
                if i["imei"] != e.imei:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(imei = i["imei"]))
                if i["owner_agent"] != e.owner_contragent:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(owner_contragent = i["owner_agent"]))
                if i["created"] != e.object_created:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_created = i["created"]))
                if i["updated"] != e.updated:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(updated = i["updated"]))
                #if i["add_date"] != e.object_add_date:
                    #session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"]).values(object_add_date = i["add_date"]))
                #if i["monitor_sys_id"] != e.sys_mon_id:
                    #session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"]).values(sys_mon_id = i["monitor_sys_id"]))
                if i["object_status_id"] != e.object_status:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_status = i["object_status_id"]))
                if i["user"] != e.owner_user:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(owner_user = i["user"]))
                if i["parent_id"] != e.parent_id_sys:
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(parent_id_sys = i["parent_id"]))

    session.commit()
    session.close()


###################
# Клиенты
###################


def add_clients_postgre(clients):
    """
    Добавляет клиентов в БД из API на Postgre
      "name": "Венета ООО",
      "shortname": " ООО Венета",
      "type": "Юридическое лицо",
      "inn": "5258072217",
      "kpp": "525801001",
      "tarif": null
    """
    session = Database().session
    for i in clients:
       client = models.Contragent(
            ca_name=i["name"].replace('\xa0', ' '),
            ca_shortname=i["shortname"].replace('\xa0', ' '),
            ca_type=i["type"].replace('\xa0', ' '),
            ca_inn=i["inn"],
            ca_kpp=i["kpp"],
        )
       session.add(client)
    session.commit()
    session.close()


def add_sys_mon_clients(clients):
    """
    Массово добавляет клиентов в БД из системы мониторинга
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["name"])
        marge["owner_id_sys_mon"] = str(i["owner"])
        marge["system_monitor_id"] = 1

    """
    session = Database().session
    for i in clients:
        client = models.ClientsInSystemMonitor(
            id_in_system_monitor=i["id_in_system_monitor"],
            name_in_system_monitor=i["name_in_system_monitor"],
            owner_id_sys_mon=i["owner_id_sys_mon"],
            system_monitor_id=i["system_monitor_id"]
        )
        session.add(client)
    session.commit()
    session.close()

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
    session.close()

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
    session.close()

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
    session.close()


###################
# Users in db 
###################

def get_db_users_from_sysem(system_id: int):
    session = Database().session
    users = session.query(models.LoginUser.system_id, models.LoginUser.login, models.LoginUser.client_name).filter(models.LoginUser.system_id == system_id).all()
    session.close()
    return users
    


###################
# 1C
###################

def add_all_clients_oneC(clients):
    """
    Добавляет клиентов в БД из API на Postgre
      "name": "Венета ООО",
      "shortname": " ООО Венета",
      "type": "Юридическое лицо",
      "inn": "5258072217",
      "kpp": "525801001",
      "tarif": null
    """
    session = Database().session
    for i in clients:
       client = models.Contragent(
            ca_name=i["Наименование"].replace('\xa0', ' '),
            ca_shortname=i["НаименованиеПолное"].replace('\xa0', ' '),
            ca_type=i["ЮрФизЛицо"].replace('\xa0', ' '),
            ca_inn=i["ИНН"],
            ca_kpp=i["КПП"],
            ca_field_of_activity = i["НаправлениеБизнеса"],
            unique_onec_id = i["УникальныйИдентификаторКлиента"],
            registration_date = i["ДатаРегистрации"],
            key_manager = i["ОсновнойМенеджер"],
            actual_address = i["ФактическийАдрес1"],
            registered_office = i["ЮридическийАдрес1"],
            phone = i["Телефон"],
        )
       session.add(client)
    session.commit()
    session.close()
