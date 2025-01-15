from dotenv import dotenv_values

config = dotenv_values(".env")

DB_USER = config["DB_USER"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_HOST = config["DB_HOST"]
DB_NAME = config["DB_NAME"]
DB_PORT = config["DB_PORT"]

SUNAPI_TOKEN = config["SUNAPI_TOKEN"]

ONE_C_TOKEN = config["ONE_C_TOKEN"]
ONEC_CLIENT_URL = config["ONEC_CLIENT_URL"]
ONEC_CONTRACT_URL = config["ONEC_CONTRACT_URL"]
ONEC_CONTACT_URL = config["ONEC_CONTACT_URL"]

ONE_C_LOGIN=config["ONE_C_LOGIN"]
ONE_C_PASSWORD=config["ONE_C_PASSWORD"]

