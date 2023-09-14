from parser.classes import Glonasssoft
from configurations import config
import json

clonasssoft = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))

#save json file
detail_vehicle = clonasssoft.get_glonasssoft_detail_vehicle("6d0dbffc-f503-49fa-b2ff-940bfa16b064")
with open('detail_vehicle.json', 'w') as f:
    json.dump(detail_vehicle, f, indent=3, ensure_ascii=False)


