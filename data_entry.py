from parser.classes import Fort, Glonasssoft, get_wialin_host_units_users, get_wialin_local_units_users, Scout
from configurations import config
from database.crud import add_objects
import json
import time
from datetime import datetime
from utils.calculate import get_status, get_glonas_user, get_fort_user, get_fort_company, get_wialon_imei, get_wialon_agent, get_wialon_user

import emoji
"""
    API on vehicles, agents, and users.

    Returns:
    A list of dictionaries containing information on each vehicle. Each dictionary contains the following keys:
    - `id_in_system`: The ID of the vehicle in the Glonasssoft system.
    - `name`: The name of the vehicle.
    - `imei`: The IMEI number of the vehicle.
    - `owner_agent`: The name of the agent that owns the vehicle.
    - `created`: The date and time the vehicle was created.
    - `updated`: The date and time the vehicle was last updated.
    - `add_date`: The date and time the vehicle was added to the system.
    - `monitor_sys_id`: The ID of the monitoring system.
    - `object_status_id`: The status of the vehicle.
    - `user`: The user associated with the vehicle.
"""

def merge_glonasssoft_data():
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
    return result



def merge_fort_data():
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
    return result


def merge_wialon_host_data():
    wialon_data = get_wialin_host_units_users(str(config.WIALON_HOST_TOKEN))
    units = wialon_data[0]["items"]
    users = wialon_data[1]["items"]
    result = []
    for i in units:
        marge = {}
        marge["id_in_system"] = str(i["id"])
        marge["name"] = emoji.demojize(i["nm"])
        if get_wialon_imei(i["flds"]) != None:
            marge["imei"] = get_wialon_imei(i["flds"])
        else:
            marge["imei"] = None
        if get_wialon_agent(i["flds"]) != None:
            marge["owner_agent"] = get_wialon_agent(i["flds"])
        else:
            marge["owner_agent"] = None
        marge["created"] = None
        marge["updated"] = None
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(3)
        if i["act"] == 0:
            marge["object_status_id"] = int(7)
        else:
            marge["object_status_id"] = get_status(i["nm"])
        marge["user"] = get_wialon_user(i["crt"], users)
        result.append(marge)
    return result


def merge_wialon_local_data():
    wialon_data = get_wialin_local_units_users(str(config.WIALON_LOCAL_TOKEN))
    units = wialon_data[0]["items"]
    users = wialon_data[1]["items"]
    result = []
    for i in units:
        marge = {}
        marge["id_in_system"] = str(i["id"])
        marge["name"] = emoji.demojize(i["nm"])
        if get_wialon_imei(i["flds"]) != None:
            marge["imei"] = get_wialon_imei(i["flds"])
        else:
            marge["imei"] = None
        if get_wialon_agent(i["flds"]) != None:
            marge["owner_agent"] = get_wialon_agent(i["flds"])
        else:
            marge["owner_agent"] = None
        marge["created"] = None
        marge["updated"] = None
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(4)
        if i["act"] == 0:
            marge["object_status_id"] = int(7)
        else:
            marge["object_status_id"] = get_status(i["nm"])
        marge["user"] = get_wialon_user(i["crt"], users)
        result.append(marge)
    return result


def merge_scout_data():
    scout = Scout(str(config.SCOUT_LOGIN), str(config.SCOUT_PASSWORD))
    token = scout.token
    time.sleep(3)
    units = scout.get_scout_units(str(token))
    time.sleep(3)
    unit_groups = scout.get_scout_unit_groups(str(token))
    return unit_groups

with open("scout_unit_groups.json", "w") as f:
    json.dump(merge_scout_data(), f, indent=3, ensure_ascii=False)
