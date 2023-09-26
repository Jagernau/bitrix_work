from parser.classes import Fort, Glonasssoft, get_wialin_host_units_users 
from configurations import config
from database.crud import add_objects
import json
import time
from datetime import datetime
from utils.calculate import get_status, get_glonas_user, get_fort_user, get_fort_company


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
        marge["user"] = get_glonas_user(i["owner"], users)
        result.append(marge)
    add_objects(result)



def add_fort_data():
    fort = Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
    token = str(fort.token)
    time.sleep(3)
    groups_companies = fort.get_fort_objectgroup(token=token)["groups"]
    time.sleep(3)
    companies = fort.get_fort_companies(token=token)["companies"]
    time.sleep(3)
    users = fort.get_fort_users(token=token)["users"]
    time.sleep(3)
    objects = fort.get_fort_objects(token=token)["objects"]
    time.sleep(3)
    groups_users = fort.get_fort_group_users(token=token)["userGroups"]
    result = []
    for i in objects:
        marge = {}
        marge["id_in_system"] = str(i["id"])
        marge["name"] = i["name"]
        marge["imei"] = i["IMEI"]
        marge["owner_agent"] = get_fort_company(i["groupId"], companies, groups_companies)
        marge["created"] = None
        marge["updated"] = None
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(2)
        marge["object_status_id"] = get_status(i["name"])
        marge["user"] = str(get_fort_user(marge["owner_agent"], users, companies))      
        result.append(marge)
    add_objects(result)


def add_wialon_host_data():
    wialon_data = get_wialin_host_units_users(str(config.WIALON_HOST_TOKEN))
    units = wialon_data[0]
    users = wialon_data[1]

    with open('wialon_units_2.json', 'w') as f:
        json.dump(units, f, indent=3, ensure_ascii=False)

    with open('wialon_users.json', 'w') as f:
        json.dump(users, f, indent=3, ensure_ascii=False)

add_wialon_host_data()
