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
from database.crud import get_db_users_from_sysem
from utils.help_utils import get_time_slice
from sim_api.classes import  BiLine


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
        marge["id_in_system"] = str(i["UnitId"])
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
        marge["user"] = generate_era_user(i.parentGroupId, users, groups)
        marge["parent_id"] = i.parentGroupId
        result.append(marge)
    return result


def get_postgre_clients():
    sun = SunPostgres(str(config.SUNAPI_TOKEN))
    clients = sun.get_clients()
    return clients


def get_onec_clients():
    sun = OneC(token=str(config.ONE_C_TOKEN), url=str(config.ONE_C_URL))
    clients = sun.get_clients()["Клиенты"]
    return clients

##########################################################
# CREATE, UPDATE, DEL OBJECT
##########################################################

def create_glonass_model_object(json_data):
    """" 
    Добавить объект в систему мониторинга глонасс
    :param json_data:
          --"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "parentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "name": "string",
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    object_model = glonasssoft.add_model_object(
            token=token,
            #id=json_data["id"],
            parentId=json_data["parentId"],
            name=json_data["name"],
    )
    return object_model


def create_glonass_object(json_data):
    """" 
    Добавить объект в систему мониторинга глонасс
    :param json_data:
        "parentId": "" ,  // ID клиента
        "name": "" ,  // имя ТС
        "imei": "" ,  // IMEI
        "deviceTypeId": "" ,  // ID типа устройства
        "modelId": "" , // ID модели
        ---"unitId": "" ,  // ID подразделения
        "sim1": "" ,  // Номер SIM 1
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    object_ = glonasssoft.add_object(
            token=token,
            parentId=json_data["parentId"],
            name=json_data["name"],
            imei=json_data["imei"],
            deviceTypeId=int(json_data["deviceTypeId"]),
            modelId=json_data["modelId"],
            #unitId=json_data["unitId"],
            sim1=json_data["sim1"]
    )
    return object_


def update_glonass_object(json_data):
    """ 
    Обновить объект в системе мониторинга глонасс
    :param json_data:
           "vehicleId": , // ID объекта
            "parentId": "" ,  // ID клиента
            "name": "" ,  // имя ТС
            "imei": "" ,  // IMEI
            "deviceTypeId": "" ,  // ID типа устройства
            --"modelId": "" , // ID модели
            --"unitId": "" ,  // ID подразделения
            "sim1": "" ,  // Номер SIM 1
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    object_ = glonasssoft.update_object(
            token=token,
            vehicleId=json_data["vehicleId"],
            parentId=json_data["parentId"],
            name=json_data["name"],
            imei=json_data["imei"],
            deviceTypeId=int(json_data["deviceTypeId"]),
            modelId=json_data["modelId"],
            sim1=json_data["sim1"]
    )
    return object_


# Whost

def create_whost_object(json_data):
    """"
    Добавить объект в систему мониторинга wialon hosting
    :param json_data:
    :return:
    """
    token = str(config.TEST_IT_WHOST_TOKEN)
    client = create_wialon_host_unit(
            token=token, 
            creatorId=json_data["creatorId"],
            name=json_data["name"],
            hwTypeId=json_data["hwTypeId"],
            )
    return client


# Wlocal

def create_wlocal_object(json_data):
    """"
    Добавить объект в систему мониторинга wialon local
    :param json_data:
    :return:
    """
    token = str(config.TEST_API_WLOCAL_TOKEN)
    client = create_wialon_local_unit(
            token=token, 
            creatorId=json_data["creatorId"],
            name=json_data["name"],
            hwTypeId=json_data["hwTypeId"],
            )
    return client


###############################################
# CREATE, UPDATE, DELETE CLIENTS
###############################################


# Glonass
def create_glonass_client(json_data):
    """"
    Добавить клиента в систему мониторинга глонасс
    :param json_data:
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    client = glonasssoft.add_client(
            token=token, 
            parentId=json_data["parentId"],
            name=json_data["name"],
            fullName=json_data["fullName"],
            inn=json_data["inn"],
            kpp=json_data["kpp"],
            )
    return client


def generate_glonass_client():
    """"
    Массовое получение всех клиентов из системы мониторинга глонасс
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    client = glonasssoft.get_glonasssoft_agents(token=token)
    result = []
    for i in client:
        marge = {}
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["name"])
        marge["owner_id_sys_mon"] = str(i["owner"])
        marge["system_monitor_id"] = 1
        result.append(marge)
    return result


def update_glonass_client(json_data):
    """"
    Обновление клиента в системе мониторинга глонасс
    :param json_data:
    :return:
    """
    glonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(glonasssoft.token)
    time.sleep(2)
    client = glonasssoft.update_client(
            token=token, 
            agentId=json_data["agentId"],
            parentId=json_data["parentId"],
            name=json_data["name"],
            fullName=json_data["fullName"],
            #inn=json_data["inn"],
            #kpp=json_data["kpp"],
            )

    return client


# Fort

def generate_fort_companys():
    """"
    Массовое получение всех клиентов из системы мониторинга форт
    :return:
    """
    fort = Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
    token = str(fort.token)
    time.sleep(2)
    client = fort.get_fort_companies(token=token)["companies"]
    result = []
    for i in client:
        marge = {}
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["name"])
        marge["owner_id_sys_mon"] = None
        marge["system_monitor_id"] = 2
        result.append(marge)
    return result


def create_fort_client(json_data):
    """"
    Добавить клиента в систему мониторинга глонасс
    :param json_data:
    :return:
    """
    fort = Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
    token = str(fort.token)
    time.sleep(2)
    client = fort.create_company(
            token=token, 
            id=json_data["id"],
            name=json_data["name"],
            description=json_data["description"],
            )
    return client


# Wialon host

def create_wialon_host_users(json_data):
    """"
    Добавить клиента в систему мониторинга глонасс
    :param json_data:
    :return:
    """
    token = str(config.TEST_IT_WHOST_TOKEN)
    time.sleep(2)
    client = create_wialon_host_user(
            token=token, 
            creatorId=json_data["creatorId"],
            name=json_data["name"],
            password=json_data["password"],
            )
    return client

def generate_wialon_host_users():
    """"
    Массовое получение всех клиентов из системы мониторинга whosting
    :return:
    """
    token = str(config.TEST_IT_WHOST_TOKEN)
    time.sleep(2)
    client = get_wialon_host_users(token=token)["items"]
    result = []
    for i in client:
        marge = {}
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["nm"])
        marge["owner_id_sys_mon"] = str(i["crt"])
        marge["system_monitor_id"] = 3
        result.append(marge)
    return result


# Wialon local 

def generate_wialon_local_users():
    """"
    Массовое получение всех клиентов из системы мониторинга whosting
    :return:
    """
    token = str(config.WIALON_LOCAL_TOKEN)
    time.sleep(2)
    client = get_wialon_local_users(token=token)["items"]
    result = []
    for i in client:
        marge = {}
        marge["id_in_system_monitor"] = str(i["id"])
        marge["name_in_system_monitor"] = str(i["nm"])
        marge["owner_id_sys_mon"] = str(i["crt"])
        marge["system_monitor_id"] = 4
        result.append(marge)
    return result


def create_wialon_local_users(json_data):
    """"
    Добавить клиента в систему мониторинга глонасс
    :param json_data:
    :return:
    """
    token = str(config.TEST_API_WLOCAL_TOKEN)
    time.sleep(2)
    client = create_wialon_local_user(
            token=token, 
            creatorId=json_data["creatorId"],
            name=json_data["name"],
            password=json_data["password"],
            )
    return client


################################################
# Utils objects
################################################
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

# def get_new_onec_clients():
#     onec = OneC(token=str(config.ONE_C_TOKEN), url=str(config.ONE_C_URL))
#     data = onec.get_clients()
#     return data
#
# clients = get_new_onec_clients()
# with open("actual_clients.json", "w") as file:
#     json.dump(clients, file, indent=3, ensure_ascii=False)
# print("GOOD")

################################################
# SimApi
################################################
def get_token_beeline():
    bi_line = BiLine(
            username=str(config.BILINE_USERNAME),
            password=str(config.BILINE_PASSWORD),
            client_id=str(config.BILINE_CLIENT_ID), 
            client_secret=str(config.BILINE_CLIENT_SECRET)
            )
    token = bi_line.token
    return token

print(get_token_beeline())
