from parser.classes import Glonasssoft
from configurations import config
import json
import time

clonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))

token = str(clonasssoft.token)
#5 секунд ожидать

time.sleep(5)

#save json file
vehicles = clonasssoft.get_glonasssoft_vehicles(token=token)
with open('vehicles.json', 'w') as f:
    json.dump(vehicles, f, indent=3, ensure_ascii=False)


