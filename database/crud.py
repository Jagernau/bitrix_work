from collections.abc import ItemsView

from sqlalchemy.util import EMPTY_DICT
import database.models as models
from database.database import Database
from sqlalchemy import and_, or_, update
from datetime import datetime
from database.logging_crud import log_global


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
                #object_created=item["created"],
                #updated=item["updated"],
                #object_add_date=item["add_date"],
                sys_mon_id=item["monitor_sys_id"],
                object_status=item["object_status_id"],
                owner_user=item["user"],
                parent_id_sys = item["parent_id"],
                contragent_id = int(result) if result else None
            )
            session.add(ca_object)
            session.commit()
            session.close()

# Логгирование добавления
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
            log_global(
                section_type="object",
                edit_id=session.query(models.CaObject.id, models.CaObject.sys_mon_object_id, models.CaObject.sys_mon_id).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).first()[0],
                field="name",
                old_value=session.query(models.CaObject).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).first().object_name,
                new_value="0",
                action="delete",
                sys_id=sys_id,
                contragent_id=session.query(models.CaObject).filter(models.CaObject.sys_mon_object_id == id_, models.CaObject.sys_mon_id == sys_id).first().contragent_id
            )
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
    

    users_logins = session.query(models.LoginUser).filter(
        models.LoginUser.system_id == sys_id,
        models.LoginUser.contragent_id != None
    )

    for i in marge_data:
      
        for e in objects_in_db:
            if i["id_in_system"] == e.sys_mon_object_id:
                if i["name"] != e.object_name:
                    log_global(section_type="object", edit_id = e.id, field = "name", old_value = e.object_name, new_value = i["name"], action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_name = i["name"]))

                if str(i["imei"]) != str(e.imei):
                    log_global(section_type="object", edit_id = e.id, field = "imei", old_value = str(e.imei), new_value = str(i["imei"]), action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(imei = str(i["imei"])))

                if i["owner_agent"] != e.owner_contragent:
                    log_global(section_type="object", edit_id = e.id, field = "owner_agent", old_value = e.owner_contragent, new_value = i["owner_agent"], action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(owner_contragent = i["owner_agent"]))

                #if i["created"] != e.object_created:
                    #log_objects(object_id = e.sys_mon_object_id, field = "created", old_value = e.object_created, new_value = i["created"], action = "update")
                   # session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_created = i["created"]))
                #if i["updated"] != e.updated:
                   # session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(updated = i["updated"]))
                #if i["add_date"] != e.object_add_date:
                    #session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"]).values(object_add_date = i["add_date"]))
                #if i["monitor_sys_id"] != e.sys_mon_id:
                    #session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"]).values(sys_mon_id = i["monitor_sys_id"]))
                if i["object_status_id"] != e.object_status:
                    log_global(section_type="object", edit_id = e.id, field = "object_status_id", old_value = e.object_status, new_value = i["object_status_id"], action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(object_status = i["object_status_id"]))

                if i["user"] != e.owner_user:
                    log_global(section_type="object", edit_id = e.id, field = "owner_user", old_value = e.owner_user, new_value = i["user"], action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(owner_user = i["user"]))

                if str(i["parent_id"]) != str(e.parent_id_sys):
                    log_global(section_type="object", edit_id = e.id, field = "parent_id", old_value = e.parent_id_sys, new_value = i["parent_id"], action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(parent_id_sys = i["parent_id"]))


                contr_id = users_logins.filter(
                    models.LoginUser.login == i["user"],
                    )
                result = contr_id.first().contragent_id if contr_id.first() else None
                if result != e.contragent_id:
                    log_global(section_type="object", edit_id = e.id, field = "contragent_id", old_value = e.contragent_id, new_value = result, action = "update", sys_id = int(i["monitor_sys_id"]))
                    session.execute(update(models.CaObject).where(models.CaObject.sys_mon_object_id == i["id_in_system"], models.CaObject.sys_mon_id == i["monitor_sys_id"]).values(contragent_id = result))

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
    session.close()


def add_one_oneC_clients(clients):
    """ 
    Запись в БД_2 конрагентов полученных из 1С
    """
    session = Database().session
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
                ca_name_contragent = item["НаименованиеКонтрагент"]

            )
            session.add(one_client)
            session.commit()
            session.close()
            
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
            session.close()
 
    
def delete_one_oneC_client(clients):
    session = Database().session
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
    session.close()


def update_one_oneC_client(clients):
    
    for i in clients:
        session = Database().session
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



        
        session.close()
