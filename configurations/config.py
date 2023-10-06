from dotenv import dotenv_values

config = dotenv_values(".env")

DB_USER = config["DB_USER"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_HOST = config["DB_HOST"]
DB_NAME = config["DB_NAME"]
DB_PORT = config["DB_PORT"]

GLONASS_LOGIN = config["GLONASS_LOGIN"]
GLONASS_PASSWORD = config["GLONASS_PASSWORD"]

FORT_LOGIN = config["FORT_LOGIN"]
FORT_PASSWORD = config["FORT_PASSWORD"]

WIALON_HOST_TOKEN = config["WIALON_HOST_TOKEN"]
WIALON_LOCAL_TOKEN = config["WIALON_LOCAL_TOKEN"]

SCOUT_LOGIN = config["SCOUT_LOGIN"]
SCOUT_PASSWORD = config["SCOUT_PASSWORD"]

ERA_LOGIN = config["ERA_LOGIN"]
ERA_PASSWORD = config["ERA_PASSWORD"]
