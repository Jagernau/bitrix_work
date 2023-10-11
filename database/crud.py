import database.models as models
from database.database import Database
from sqlalchemy import and_, or_, update
from datetime import datetime




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
            owner_user=i["user"]
        )
        session.add(ca_object)
    session.commit()
    session.close()


def add_one_object(marge_data: list):
    """ 
    Добавляет один объект в БД
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
                owner_user=item["user"]
            )
            session.add(ca_object)
    session.commit()
    session.close()


def delete_one_object(marge_data: list):
    """
    Удаляет один объект из БД
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
            session.query(models.CaObject).filter(models.CaObject.sys_mon_object_id == id_).delete()
    session.commit()
    session.close()

def update_one_object(marge_data: list):
    """
    Обновляет один объект в БД
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

    session.commit()
    session.close()



def add_clients_postgre(clients):
    """
    Добавляет клиентов в БД
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
