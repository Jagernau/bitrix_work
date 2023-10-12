from parser.classes import (
        Fort, 
        Glonasssoft, 
        get_wialin_host_units_users, 
        get_wialin_local_units_users, 
        Scout, 
        get_era_data,
        SunPostgres,


        )
from configurations import config
import time
from datetime import datetime
from utils.calculate import (
        get_status, 
        get_glonas_user, 
        get_fort_user, 
        get_fort_company,
        get_fort_company_group,
        get_wialon_imei, 
        get_wialon_agent, 
        get_wialon_user, 
        generate_scout_user, 
        generate_era_company,
        generate_era_user
        )

import emoji
import json
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
        marge["parent_id"] = i["owner"]
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
        marge["owner_agent"] = get_fort_company_group(i["groupId"], groups_companies)
        marge["created"] = None
        marge["updated"] = None
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(2)
        marge["object_status_id"] = get_status(i["name"])
        marge["user"] = str(get_fort_user(marge["owner_agent"], users, companies))  
        marge["parent_id"] = i["groupId"]
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
        marge["parent_id"] = i["crt"]
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
        marge["parent_id"] = i["crt"]
        result.append(marge)
    return result


def merge_scout_data():
    scout = Scout(str(config.SCOUT_LOGIN), str(config.SCOUT_PASSWORD))
    token = scout.token
    time.sleep(3)
    units = scout.get_scout_units(str(token))["Units"]
    time.sleep(3)
    unit_groups = scout.get_scout_unit_groups(str(token))["Groups"]
    result = []
    for i in units:
        marge = {}
        marge["id_in_system"] = i["UnitId"]
        marge["name"] = i["Name"]
        marge["imei"] = None
        marge["owner_agent"] = i["Description"]
        marge["created"] = None
        marge["updated"] = None
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(6)
        marge["object_status_id"] = get_status(i["Name"])
        marge["user"] = str(generate_scout_user(i["UnitId"], unit_groups))
        marge["parent_id"] = i["CompanyId"]
        result.append(marge)
    return result


def merge_era_data():
    from thrif.dispatch.server.thrif.backend.DispatchBackend import Client

    era = get_era_data(str(config.ERA_LOGIN), str(config.ERA_PASSWORD), Client)
    objects = era[0]
    groups = era[1]
    users = era[2]
    result = []
    for i in objects:
        marge = {}
        marge["id_in_system"] = str(i.id)
        marge["name"] = i.name
        marge["imei"] = i.tracker.identifier[0]
        marge["owner_agent"] = generate_era_company(i.parentGroupId, groups)
        marge["created"] = None
        marge["updated"] = None
        marge["add_date"] = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
        marge["monitor_sys_id"] = int(5)
        marge["object_status_id"] = get_status(i.name)
        marge["user"] = generate_era_user(i.parentGroupId, users)
        marge["parent_id"] = i.parentGroupId
        result.append(marge)
    return result


def get_postgre_clients():
    sun = SunPostgres(str(config.SUNAPI_TOKEN))
    clients = sun.get_clients()
    return clients


def create_glonass_client(json_data):
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    client = glonasssoft.add_client(token=token, name=json_data["name"], inn=json_data["inn"], kpp=json_data["kpp"])
    return client

print (create_glonass_client({
    "parentId": "123",
    "name": "test",
    "inn": "1234567890",
    "kpp": "123456789"
}))
