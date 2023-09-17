from .. import models, schemas
from ..database import Database
from sqlalchemy import and_, or_
from typing import List, Dict, Optional, Union
from datetime import datetime


data_glonass = Dict[str, Optional[Union[str, int, None]]]

def create_ca_objects(data: data_glonass):
    session = Database().session
    for i in data:
        ca_object = models.ca_objects(
            ca_object_name=i["number"],
            imei=i["imei"],
            ca_object_sm_object_id=i["id"],
            owner=i["owner"],
            ca_object_add_date=datetime.strptime(str(i["created"].split(".")[0]), "%Y-%m-%dT%H:%M:%S"),
            updated=datetime.strptime(str(i["updated"].split(".")[0]), "%Y-%m-%dT%H:%M:%S"),
            ca_object_sm_id=1,
        )
        session.add(ca_object)
    session.commit()
    session.close()
