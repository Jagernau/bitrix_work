from parser.classes import Fort, Glonasssoft
from configurations import config
from database.cruds import glonass_crud
import json
import time
from datetime import datetime
from utils.calculate import get_status


def add_glonasssoft_data():
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(1)
    vehicles = glonasssoft.get_glonasssoft_vehicles(token=token)
    time.sleep(1)
    agents = glonasssoft.get_glonasssoft_agents(token=token)
    time.sleep(1)
    users = glonasssoft.get_glonasssoft_users(token=token)
    result = []
    for i in vehicles:
        marge = {}
        marge["id"] = i["id"]
        marge["name"] = i["number"]
        marge["imei"] = i["imei"]
        marge["owner_agent"] = [agent["name"] for agent in agents if i["owner"] in agent["id"]][0]
        marge["created"] = datetime.strptime(str(i["created"].split(".")[0]), "%Y-%m-%dT%H:%M:%S")
        marge["updated"] = datetime.strptime(str(i["updated"].split(".")[0]), "%Y-%m-%dT%H:%M:%S")
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(1)
        marge["object_sys_id"] = get_status(i["number"])
        for x in users:
            if i["owner"] in x["agentGuid"]:
                marge["owner_user"] = x["name"]

        result.append(marge)
    return result
with open('merge_glonas.txt', 'w') as f:
    f.write(str(add_glonasssoft_data()))
    




# fort = Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
# token = str(fort.token)
# time.sleep(2)
# objects_groups: dict = fort.get_fort_objectgroup(token=token)
# with open('fort_objects_groups.json', 'w') as f:
#     json.dump(objects_groups, f, indent=3, ensure_ascii=False)
#
