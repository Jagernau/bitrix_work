from parser.classes import (
        Fort, 
        Glonasssoft, 
        get_wialin_host_units_users, 
        get_wialin_local_units_users, 
        Scout, 
        get_era_data,
        SunPostgres,
        create_wialon_host_user,
        create_wialon_host_unit,
        get_wialon_host_users,
        create_wialon_local_user,
        get_wialon_local_users,
        create_wialon_local_unit,
        OneC,
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
        generate_era_user,
        generate_client_from_user,
        get_fort_user_by_id,
)
from database.crud import get_db_users_from_sysem, get_db_contragents
from utils.help_utils import get_time_slice

import emoji
import json


############################
# GET FULL DATA FROM OBJECTS
############################

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
        marge["id_in_system"] = str(i["vehicleId"])
        marge["name"] = i["number"]
        marge["imei"] = i["imei"]
        marge["owner_agent"] = [agent["name"] for agent in agents if i["owner"] in agent["id"]][0]
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
        marge["monitor_sys_id"] = int(2)
        marge["object_status_id"] = get_status(i["name"])
        
        login = ""
        company_id = get_fort_company(
                i["groupId"],
                companies,
                groups_companies
                )
        login = get_fort_user_by_id(company_id, users, marge["owner_agent"])

        marge["user"] = login
        marge["parent_id"] = i["groupId"]
        result.append(marge)
    return result

def merge_wialon_host_data():
    
    wialon_host_db_users = get_db_users_from_sysem(3)
    
    wialon_data = get_wialin_host_units_users(str(config.TEST_IT_WHOST_TOKEN))
    units = wialon_data[0]["items"]
    users = wialon_data[1]["items"]
    result = []
    for i in units:
        marge = {}
        marge["id_in_system"] = str(i["id"])
        marge["name"] = emoji.demojize(i["nm"])
        marge["imei"] = str(i["uid"])
        marge["owner_agent"] = generate_client_from_user(
                get_wialon_user(i["crt"], users),
                wialon_host_db_users
                )
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
    
    wialon_local_db_users = get_db_users_from_sysem(4)

    wialon_data = get_wialin_local_units_users(str(config.WIALON_LOCAL_TOKEN))
    units = wialon_data[0]["items"]
    users = wialon_data[1]["items"]
    result = []
    for i in units:
        marge = {}
        marge["id_in_system"] = str(i["id"])
        marge["name"] = emoji.demojize(i["nm"])
        marge["imei"] = str(i["uid"])
        marge["owner_agent"] = generate_client_from_user(
                get_wialon_user(i["crt"], users),
                wialon_local_db_users
        )
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
        users = generate_scout_user(i["UnitId"], unit_groups)
        clear_users = []
        for z in users:
            if z == 'Все':
                pass
            elif z == 'Сатанов ИП':
                pass
            elif z == 'Сантел Навигация':
                pass
            else:
                clear_users.append(z)

        contragents_ids = []
        for user in clear_users:
            res = get_db_contragents(user)
            if res:
                contragents_ids.append(int(res))   
        marge = {}
        marge["id_in_system"] = str(i["UnitId"])
        marge["name"] = i["Name"]
        marge["imei"] = None
        marge["owner_agent"] = i["Description"]
        marge["monitor_sys_id"] = int(6)
        marge["object_status_id"] = get_status(i["Name"])
        marge["user"] = str(clear_users)
        marge["parent_id"] = i["CompanyId"]
        cont_id = contragents_ids[0] if len(contragents_ids) >= 1 else None
        if cont_id:
            marge["contragent_id"] = int(cont_id)

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
        marge["monitor_sys_id"] = int(5)
        marge["object_status_id"] = get_status(i.name)
        marge["user"] = generate_era_user(i.parentGroupId, users, groups)
        marge["parent_id"] = i.parentGroupId
        result.append(marge)
    return result

# Glonasssoft
def put_comand_to_glonasssoft(json_data):
    """"
    Добавить команду в систему мониторинга глонасс
    :param json_data:
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    comand  = glonasssoft.put_terminal_comands(
            token=token,
            sourceid = str(config.SOURCE_GLONASS_ID),
            destinationid = json_data["imei"],
            taskdata = json_data["command"],
            owner = str(config.GRAND_OWNER_GLONASS_ID),
            )
    return comand

def get_comands_glonasssoft(json_data):
    """"
    Получить отчёт по командам глонасс
    :param json_data:
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    comand  = glonasssoft.get_terminal_comands(
            token=token,
            imei = json_data["imei"],
            start = json_data["start"],
            end = json_data["end"],
            )
    return comand

def no_token_comand_put_get_glonasssoft(json_data):
    """"
    Объединить отчеты по командам глонасс
    :param json_data:
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(1)
    glonasssoft.put_terminal_comands(
            token=token,
            sourceid = str(config.SOURCE_GLONASS_ID),
            destinationid = json_data["imei"],
            taskdata = json_data["command"],
            owner = str(config.GRAND_OWNER_GLONASS_ID),
    )
    time.sleep(8)
    time_slice = get_time_slice()
    get_data = glonasssoft.get_terminal_comands(
            token=token,
            imei = json_data["imei"],
            start = time_slice[0],
            end = time_slice[1],
    )
    return get_data
            


def with_token_comand_put_get_glonasssoft(token_glonass, imei_glonas, command_glonass):
    """"
    Объединить отчеты по командам глонасс
    :param json_data:
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))    
    time.sleep(3)
    glonasssoft.put_terminal_comands(
            token=token_glonass,
            sourceid = str(config.SOURCE_GLONASS_ID),
            destinationid = imei_glonas,
            taskdata = command_glonass,
            owner = str(config.GRAND_OWNER_GLONASS_ID),
    )
    time.sleep(8)
    time_slice = get_time_slice()
    get_data = glonasssoft.get_terminal_comands(
            token=token_glonass,
            imei = imei_glonas,
            start = time_slice[0],
            end = time_slice[1],
    )
    return get_data

def get_onec_clients():
    "Отдаёт клиентов 1С"
    sun = OneC(token=str(config.ONE_C_TOKEN), url=str(config.ONEC_CLIENT_URL))
    clients = sun.get_clients()["Клиенты"]
    return clients

def get_onec_contracts():
    "Отдаёт контракты 1С"
    sun = OneC(token=str(config.ONE_C_TOKEN), url=str(config.ONEC_CONTRACT_URL))
    contracts = sun.get_clients()["Договоры"]
    return contracts

contracts = get_onec_contracts()
with open("contracts.json", "w") as file:
    json.dump(contracts, file, indent=3, ensure_ascii=False)
print(len(contracts))

