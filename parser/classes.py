import json
import requests

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

    def get_glonasssoft_sensors(self):
        url = "https://hosting.glonasssoft.ru/api/v3/sensors/types"
        headers = {"X-Auth": self.token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None


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
