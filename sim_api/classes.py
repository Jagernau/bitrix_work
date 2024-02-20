import json
import requests
import datetime
import sys


class BiLine:
    def __init__(self, username: str, password: str, client_id: str, client_secret: str) -> None:
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def token(self) -> str | None:
        url ='https://iot.beeline.ru/oauth/token'
        data = {
            "username": self.username,
            "password": self.password,
            "client_id": int(self.client_id),
            "client_secret": self.client_secret,
            "grant_type": "password",
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, data=data, headers=headers)
        return response.text


    @staticmethod
    def get_bi_line_sims(token: str, dashboard_id: str):
        url = f"https://iot.beeline.ru/api/v1/dashboard/{dashboard_id}/sim"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers,)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

