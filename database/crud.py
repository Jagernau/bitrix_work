import database.models as models
from database.database import Database
from sqlalchemy import and_, or_
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

