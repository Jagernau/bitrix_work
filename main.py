from parser.classes import Glonasssoft
from configurations import config
import json

clonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))

#save json file
sensors = clonasssoft.get_glonasssoft_sensors()
print(sensors)
# with open('devices.json', 'w') as f:
#     json.dump(devices, f, indent=3, ensure_ascii=False)
#

