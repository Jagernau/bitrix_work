import json
import requests
from wialon.sdk import WialonSdk
import datetime
import sys
sys.path.append('gen-py')

from thrift import Thrift
from thrift.transport import TSocket
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
            "district": "",
            "region": "",
            "city": "",
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
    def add_object(*ars, **kwargs):
        """ 
        Создание объекта под клиента
        parentId: str
        name: str
        imei: str
        deviceTypeId: str
        modelId: str
        unitId: str
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
                    "unitId": kwargs["unitId"],
                    "sim1": kwargs["sim1"],
                    }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to add object. Error:  {response.text}"





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

    url = "monitoring.aoglonass.ru"
    transport = TSocket.TSocket(url, 19990)
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


