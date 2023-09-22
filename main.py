from parser.classes import Fort, Glonasssoft
from configurations import config
from database.crud import add_objects
import json
import time
from datetime import datetime
from utils.calculate import get_status, get_user


def add_glonasssoft_data():
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(3)
    vehicles = glonasssoft.get_glonasssoft_vehicles(token=token)
    time.sleep(3)
    agents = glonasssoft.get_glonasssoft_agents(token=token)
    time.sleep(3)
    users = glonasssoft.get_glonasssoft_users(token=token)
    time.sleep(3)
    result = []
    for i in vehicles:
        marge = {}
        marge["id_in_system"] = i["id"]
        marge["name"] = i["number"]
        marge["imei"] = i["imei"]
        marge["owner_agent"] = [agent["name"] for agent in agents if i["owner"] in agent["id"]][0]
        marge["created"] = datetime.strptime(str(i["created"].split(".")[0]), "%Y-%m-%dT%H:%M:%S")
        marge["updated"] = datetime.strptime(str(i["updated"].split(".")[0]), "%Y-%m-%dT%H:%M:%S")
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(1)
        marge["object_status_id"] = get_status(i["number"])
        marge["user"] = get_user(i["owner"], users)
        result.append(marge)
    add_objects(result)

add_glonasssoft_data()

# fort = Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
# token = str(fort.token)
# time.sleep(2)
# objects_groups: dict = fort.get_fort_objectgroup(token=token)
# with open('fort_objects_groups.json', 'w') as f:
#     json.dump(objects_groups, f, indent=3, ensure_ascii=False)
#
