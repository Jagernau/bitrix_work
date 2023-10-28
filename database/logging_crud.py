import database.models as models
from database.database import Database


def log_clients(*args, **kwargs):
    """ 
    Записывает в базу данных изменения в 1С клиентов
           contragent_id=kwargs["contragent_id"],
           field=kwargs["field"],
           old_value=kwargs["old_value"],
           new_value=kwargs["new_value"],
    """
    session = Database().session
    changes = models.ClientsLog(
           contragent_id=kwargs["contragent_id"],
           field=kwargs["field"],
           old_value=kwargs["old_value"],
           new_value=kwargs["new_value"],
           )
    session.add(changes)

    session.commit()
    session.close()

def log_objects(*args, **kwargs):
    """ 
    Записывает в базу данных изменения в 1С объектов
           object_id=kwargs["object_id"],
           field=kwargs["field"],
           old_value=kwargs["old_value"],
           new_value=kwargs["new_value"],
           action=kwargs["action"],
    """
    session = Database().session
    changes = models.ObjectsLog(
           object_id=kwargs["object_id"],
           field=kwargs["field"],
           old_value=kwargs["old_value"],
           new_value=kwargs["new_value"],
           action=kwargs["action"],
           sys_id=kwargs["sys_id"],
           )
    session.add(changes)

    session.commit()
    session.close()
