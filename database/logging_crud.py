import database.models as models
from database.database import Database



def log_global(*args, **kwargs):
    """ 
    Записывает в базу данных изменения в 1С объектов
           object_id=kwargs["object_id"],
           field=kwargs["field"],
           old_value=kwargs["old_value"],
           new_value=kwargs["new_value"],
           action=kwargs["action"],
    """
    session = Database().session
    changes = models.GlobalLogging(
           section_type=kwargs["section_type"],
           edit_id=kwargs["edit_id"],
           field=kwargs["field"],
           old_value=kwargs["old_value"],
           new_value=kwargs["new_value"],
           action=kwargs["action"],
           sys_id=kwargs["sys_id"],
           )
    session.add(changes)
