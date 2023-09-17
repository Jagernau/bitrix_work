from parser.classes import Fort
from configurations import config
from database.cruds import glonass_crud
import json
import time


fort = Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
token = str(fort.token)
time.sleep(2)
objects_groups: dict = fort.get_fort_objectgroup(token=token)
with open('fort_objects_groups.json', 'w') as f:
    json.dump(objects_groups, f, indent=3, ensure_ascii=False)

