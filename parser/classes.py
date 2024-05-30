import json
import requests
from wialon.sdk import WialonSdk
import datetime
import sys
sys.path.append('gen-py')

import ssl
from thrift import Thrift
from thrift.transport import TSocket, TSSLSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from thrif.dispatch.server.thrif.backend.DispatchBackend import Client

class Glonasssoft:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    @property
    def token(self) -> str | None:
        """Login to glonasssoft"""
        url = f'https://hosting.glonasssoft.ru/api/v3/auth/login'
        data = {'login': self.login, 'password': self.password}
        headers = {'Content-type': 'application/json', 'accept': 'json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.json()["AuthId"]
        else:
            return None

    @staticmethod
    def get_glonasssoft_agents(token: str):
        url = f"https://hosting.glonasssoft.ru/api/agents/"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    @staticmethod
    def get_glonasssoft_users(token: str):
        url = f"https://hosting.glonasssoft.ru/api/users/"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    @staticmethod
    def get_glonasssoft_vehicles(token: str):
        url = f"https://hosting.glonasssoft.ru/api/vehicles/"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    @staticmethod
    def get_glonasssoft_detail_vehicle(token: str, id: str):
        url = f"https://hosting.glonasssoft.ru/api/vehicles/{id}"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None
    
    @staticmethod
    def get_glonasssoft_devices(token: str):
        payload = ""
        url = "https://hosting.glonasssoft.ru/api/v3/devices/types"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    @staticmethod
    def get_glonasssoft_sensors(token: str):
        url = "https://hosting.glonasssoft.ru/api/v3/sensors/types"
        headers = {"X-Auth": token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None
    
    @staticmethod
    def add_client(*ars, **kwargs):
        url = "https://hosting.glonasssoft.ru/api/v3/agents"
        headers = {
            "X-Auth": kwargs["token"]
        }
        data = {
            "parentId": kwargs["parentId"],
            "name": kwargs["name"],
            "fullName": kwargs["fullName"],
            "agentInfoType": 0,
            "isForeign": False,
            "district": "Россия",
            "region": "Россия",
            "city": "Нижний Новгород",
            "inn": kwargs["inn"],
            "kpp": kwargs["kpp"],
            "address": "",
            "addressFact": "",
            "email": "",
            "director": "",
            "bankName": "",
            "bankBIK": "",
            "bankRS": "",
            "bankKS": ""
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to add client. Error:  {response.text}"



    @staticmethod
    def update_client(*ars, **kwargs):
        url = "https://hosting.glonasssoft.ru/api/v3/agents"
        headers = {
            "X-Auth": kwargs["token"]
        }
        data = {
            "agentId": kwargs["agentId"],
            "parentId": kwargs["parentId"],
            "name": kwargs["name"],
            "fullName": kwargs["fullName"],
            #"agentInfoType": 0,
            #"isForeign": False,
            #"district": "",
            #"region": "",
            #"city": "",
            #"inn": kwargs["inn"],
            #"kpp": kwargs["kpp"],
            #"address": "",
            #"addressFact": "",
            #"email": "",
            #"director": "",
            #"bankName": "",
            #"bankBIK": "",
            #"bankRS": "",
            #"bankKS": ""
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to update client. Error:  {response.text}"

    @staticmethod
    def add_model_object(*ars, **kwargs):
        """ 
        Создание модели объекта под клиента
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "parentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "deleted": true,
          "extId": "string",
          "name": "string",
          "picture": "string",
          "minspeed": 0,
          "maxspeed": 0,
          "width": 0,
          "imbeddedtrailer": true,
          "fueloutlay": 0,
          "hoppercapacity": 0,
          "hopperdischargespeed": 0,
          "modelType": 0
        """
        url = "https://hosting.glonasssoft.ru/api/v3/models"
        headers = {
            "X-Auth": kwargs["token"]
        }
        data = {
            #"id": kwargs["id"],
            "parentId": kwargs["parentId"],
            "deleted": True,
            "extId": "",
            "name": kwargs["name"],
            "picture": "",
            "minspeed": 3,
            "maxspeed": 150,
            "width": 5,
            "imbeddedtrailer": True,
            "fueloutlay": 0,
            "hoppercapacity": 0,
            "hopperdischargespeed": 0,
            "modelType": 0
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to add model object. Error:  {response.text}"

    @staticmethod
    def add_object(*ars, **kwargs):
        """ 
        Создание объекта под клиента
        parentId: str
        name: str
        imei: str
        deviceTypeId: str
        modelId: str
        --unitId: str
        sim1: str
        """
        url = "https://hosting.glonasssoft.ru/api/v3/vehicles"
        headers = {
            "X-Auth": kwargs["token"]
        }
        data = {
                    "parentId": kwargs["parentId"],
                    "name": kwargs["name"],
                    "imei": kwargs["imei"],
                    "deviceTypeId": kwargs["deviceTypeId"],
                    "modelId": kwargs["modelId"],
                    #"unitId": kwargs["unitId"],
                    "sim1": kwargs["sim1"],
                    }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to add object. Error:  {response.text}"


    @staticmethod
    def update_object(*ars, **kwargs):
        """ 
        Обновление объекта под клиента
           "vehicleId": , // ID объекта
            "parentId": "" ,  // ID клиента
            "name": "" ,  // имя ТС
            "imei": "" ,  // IMEI
            "deviceTypeId": "" ,  // ID типа устройства
            "modelId": "" , // ID модели
            --"unitId": "" ,  // ID подразделения
            "sim1": "" ,  // Номер SIM 1
        """
        url = "https://hosting.glonasssoft.ru/api/v3/vehicles"
        headers = {
            "X-Auth": kwargs["token"]
        }
        data = {
                    "vehicleId": int(kwargs["vehicleId"]),
                    "parentId": kwargs["parentId"],
                    "name": kwargs["name"],
                    "imei": kwargs["imei"],
                    "deviceTypeId": kwargs["deviceTypeId"],
                    "modelId": kwargs["modelId"],
                    "sim1": kwargs["sim1"],
                    }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to update object. Error:  {response.text}"

    @staticmethod
    def put_terminal_comands(*args, **kwargs):
        """ 
        Отправка команды в терминал
            "sourceid": "string",
            "destinationid": "string",
            "tasktype": 0,
            "taskdata": "string",
            "trycount": 0,
            "TryMax": "3",
            "answer": "",
            "owner": "string",
        """
        url = "https://hosting.glonasssoft.ru/api/commands/put"
        headers = {
            "X-Auth": kwargs["token"],
        }
        data = [{
            "sourceid": kwargs["sourceid"],
            "destinationid": kwargs["destinationid"],
            "tasktype": 0,
            "taskdata": kwargs["taskdata"],
            "trycount": 0,
            "TryMax": "3",
            "answer": "",
            "owner": kwargs["owner"],
        }]
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to connect terminal. Error: {response.status_code} {response.text}"

    @staticmethod
    def get_terminal_comands(*args, **kwargs):
        """
        Получение ответов от терминала
        "imei": "string",
        "start": "2022-01-18",
        """
        data = str({
            "imei": kwargs["imei"],
            "start": kwargs["start"],
            "end": kwargs["end"],
            })
        url = "https://hosting.glonasssoft.ru/api/commands"
        params = {
            "q": data,
            "sort": '[{"property":"createtime","direction":"DESC"}]'
        }
        headers = {
            "X-Auth": kwargs["token"],
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to connect terminal. Error: {response.status_code} {response.text}"


class Fort:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
    
    @property
    def token(self) -> str | None:
        url = f'https://fm.suntel-nn.ru/api/integration/v1/connect'
        params = {
                'login': self.login,
                'password': self.password,
                'lang': 'ru-ru',
                'timezone': '+3'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.headers['SessionId']
        else:
            return None

    @staticmethod
    def get_fort_companies(token: str):
        """get json from frt api"""
        url = f'https://fm.suntel-nn.ru/api/integration/v1/getcompanieslist'
        params = {
                'SessionId': str(token),
                'companyId': 0
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": token}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def get_fort_users(token: str):
        """get json from frt api"""
        url = f'https://fm.suntel-nn.ru/api/integration/v1/users'
        params = {
                'SessionId': str(token),
                'companyId': 0
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": token}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None


    @staticmethod
    def get_fort_objects(token: str):
        """get json from frt api"""
        url = f'https://fm.suntel-nn.ru/api/integration/v1/getobjectslist'
        params = {
                'SessionId': str(token),
                'companyId': 0
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": token}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def get_fort_objectgroup(token: str):
        """get json from frt api"""
        url = f'https://fm.suntel-nn.ru/api/integration/v1/getobjectgroupslist'
        params = {
                'SessionId': str(token),
                'companyId': 0
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": token}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def get_fort_group_users(token: str):
        """get json from frt api"""
        url = f'https://fm.suntel-nn.ru/api/integration/v1/usergroups'
        params = {
                'SessionId': str(token),
                'companyId': 0
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": token}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None


    @staticmethod
    def create_company(token, **kwargs):
        url = 'https://fm.suntel-nn.ru/api/integration/v1/companies'
        data = {
                'id': str(kwargs["id"]),
                'name': str(kwargs["name"]),
                "description": str(kwargs["description"]),
                "maxObjectsCount": int(10),
                "smsSenderName": "string",
                "addDataStoreMonths": int(3),
                "addDeletedStoreDays": int(20),
                "timezone": "Europe/Moscow",
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": token}
        response = requests.post(url, json=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to add object. Error:  {response.text}"



def get_wialin_host_units_users(token: str):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='hst-api.wialon.com',
      port=0,
      session_id='',
      extra_params=""
    )

    resp = sdk.login(str(token))
    parameters_unit = {
    'spec':{
      'itemsType': "avl_unit",
      'propName': "sys_name",
      'propValueMask': "*",
      'sortType': "sys_name",
    #  'propType': str,
      'or_logic': 0
    },
    'force': 1,
    'flags': 269,
    'from': 0,
    'to': 0
    }
    units = sdk.core_search_items(parameters_unit)
    parameters_user = {
    'spec':{
        "itemsType": "user",
        "propName": "sys_name",
        "propValueMask": "*",
        "sortType": "sys_name",
        "or_logic": 0
    },
    'force': 1,
    'flags': 269,
    'from': 0,
    'to': 0
    }
    users = sdk.core_search_items(parameters_user)
    sdk.logout()
    return [units, users]

def get_wialon_host_users(token: str):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='hst-api.wialon.com',
      port=0,
      session_id='',
      extra_params=""
    )
    resp = sdk.login(str(token))
    parameters_user = {
        'spec':{
            'itemsType': "user",
            'propName': "sys_name",
            'propValueMask': "*",
            'sortType': "sys_name",
            'or_logic': 0
        },
        'force': 1,
        'flags': 269,
        'from': 0,
        'to': 0
        }
    users = sdk.core_search_items(parameters_user)
    sdk.logout()
    return users



def create_wialon_host_user(token, **kwargs):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='hst-api.wialon.com',
      port=0,
      session_id='',
      extra_params=""
    )

    resp = sdk.login(str(token))
    parameters_user = {
            "creatorId": int(kwargs["creatorId"]),
            "name": str(kwargs["name"]),
            "password": str(kwargs["password"]),
            "dataFlags": 1,
    }
    user = sdk.core_create_user(parameters_user)
    sdk.logout()
    return user


def create_wialon_host_unit(token, **kwargs):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='hst-api.wialon.com',
      port=0,
      session_id='',
      extra_params=""
    )

    resp = sdk.login(str(token))
    parameters_unit = {
            "creatorId": int(kwargs["creatorId"]),
            "name": str(kwargs["name"]),
            "hwTypeId": int(kwargs["hwTypeId"]),
            "dataFlags": 1,
    }
    unit = sdk.core_create_unit(parameters_unit)
    sdk.logout()
    return unit




# Local
def get_wialin_local_units_users(token: str):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='suntel-wialon.ru',
      port=0,
      session_id='',
      extra_params=""
    )

    resp = sdk.login(str(token))
    parameters_unit = {
    'spec':{
      'itemsType': "avl_unit",
      'propName': "sys_name",
      'propValueMask': "*",
      'sortType': "sys_name",
    #  'propType': str,
      'or_logic': 0
    },
    'force': 1,
    'flags': 269,
    'from': 0,
    'to': 0
    }
    units = sdk.core_search_items(parameters_unit)
    parameters_user = {
    'spec':{
        "itemsType": "user",
        "propName": "sys_name",
        "propValueMask": "*",
        "sortType": "sys_name",
        "or_logic": 0
    },
    'force': 1,
    'flags': 269,
    'from': 0,
    'to': 0
    }
    users = sdk.core_search_items(parameters_user)
    sdk.logout()
    return [units, users]


def get_wialon_local_users(token: str):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='suntel-wialon.ru',
      port=0,
      session_id='',
      extra_params=""
    )
    resp = sdk.login(str(token))
    parameters_user = {
        'spec':{
            'itemsType': "user",
            'propName': "sys_name",
            'propValueMask': "*",
            'sortType': "sys_name",
            'or_logic': 0
        },
        'force': 1,
        'flags': 269,
        'from': 0,
        'to': 0
        }
    users = sdk.core_search_items(parameters_user)
    sdk.logout()
    return users

def create_wialon_local_user(token, **kwargs):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='suntel-wialon.ru',
      port=0,
      session_id='',
      extra_params=""
    )

    resp = sdk.login(str(token))
    parameters_user = {
            "creatorId": int(kwargs["creatorId"]),
            "name": str(kwargs["name"]),
            "password": str(kwargs["password"]),
            "dataFlags": 1,
    }
    user = sdk.core_create_user(parameters_user)
    sdk.logout()
    return user


def create_wialon_local_unit(token, **kwargs):
    sdk = WialonSdk(
      is_development=True,
      scheme='https',
      host='suntel-wialon.ru',
      port=0,
      session_id='',
      extra_params=""
    )

    resp = sdk.login(str(token))
    parameters_unit = {
            "creatorId": int(kwargs["creatorId"]),
            "name": str(kwargs["name"]),
            "hwTypeId": int(kwargs["hwTypeId"]),
            "dataFlags": 1,
    }
    unit = sdk.core_create_unit(parameters_unit)
    sdk.logout()
    return unit


class Scout:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password


    def __get_current_timestamp_utc(self) -> str:
        now = datetime.datetime.utcnow()
        timestamp = "/Date(" + str(int(now.timestamp() * 1000)) + ")/"
        return timestamp

    @property
    def token(self) -> str | None:
        url = "http://89.208.197.19:11501/spic/auth/rest/Login"
        payload = {
            "Login": f"{self.login}",
            "Password": f"{self.password}",
            "TimeStampUtc": f"{self.__get_current_timestamp_utc()}",
            "TimeZoneOlsonId": "Europe/Moscow",
            "CultureName": "ru-ru",
            "UiCultureName": "ru-ru"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            token = response.json()["SessionId"]
            return token
        else:
            return None


    @staticmethod
    def get_scout_units(token: str):
        url = "http://89.208.197.19:11501/spic/units/rest/getAllUnits"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "ScoutAuthorization": str(token)}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    @staticmethod
    def get_scout_unit_groups(token: str):
        url = "http://89.208.197.19:11501/spic/unitGroups/rest/"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "ScoutAuthorization": str(token)}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

def get_era_data(login: str, password: str, thrif_class_client):

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    url = "monitoring.aoglonass.ru"
    transport = TSSLSocket.TSSLSocket(url, 19991, ssl_context=ssl_context)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    open = transport.open()
    client: Client = thrif_class_client(protocol)
    session_id = client.login(login, password, True)
    parent_id = client.getCurrentUser(session_id)
    objects = client.getChildrenMonitoringObjects(session_id, parent_id.parentGroupId, True)
    groups = client.getChildrenGroups(session_id, parent_id.parentGroupId, True)
    users = client.getChildrenUsers(session_id, parent_id.parentGroupId, True)
    transport.close()
    return [objects, groups, users]


class SunPostgres:
    def __init__(self, token: str):
        self.token = token

    def get_clients(self):
        url = 'http://158.160.73.178:8000/api/tklient/'
        headers = {
            'Authorization': f'Token {self.token}',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            clients = response.json()
            return clients
        else:
            return None

class OneC:
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url

    def get_clients(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json'
        }
        response = requests.get(self.url, headers=headers)
        return response.json()

