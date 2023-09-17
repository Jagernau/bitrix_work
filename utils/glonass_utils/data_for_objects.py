from parser.classes import Glonasssoft
from configurations import config
from database.cruds import glonass_crud
import json
import time


def get_data_glonasssoft():
    clonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    token = str(clonasssoft.token)
    time.sleep(2)
    vehicles: dict = clonasssoft.get_glonasssoft_vehicles(token=token)
    return vehicles

vehicles = get_data_glonasssoft()
glonass_crud.create_ca_objects(vehicles)
