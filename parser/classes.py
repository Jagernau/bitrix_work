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

    def get_glonasssoft_agents(self):
        url = f"https://hosting.glonasssoft.ru/api/agents/"
        headers = {"X-Auth": self.token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_glonasssoft_users(self):
        url = f"https://hosting.glonasssoft.ru/api/users/"
        headers = {"X-Auth": self.token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_glonasssoft_vehicles(self):
        url = f"https://hosting.glonasssoft.ru/api/vehicles/"
        headers = {"X-Auth": self.token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None
    def get_glonasssoft_detail_vehicle(self, id: str):
        url = f"https://hosting.glonasssoft.ru/api/vehicles/{id}"
        headers = {"X-Auth": self.token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_glonasssoft_devices(self):
        url = "https://hosting.glonasssoft.ru/api/devices/"
        headers = {"X-Auth": self.token, 'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers,)
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
        url = f'https://suntel_fm/api/integration/v1/connect'
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

    def get_fort_agents(self):
        """get json from frt api"""
        url = f'https://suntel_fm/api/integration/v1/agents'
        params = {
                'SessionId': str(self.token),
                'companyId': 0
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', "SessionId": self.token}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None           
