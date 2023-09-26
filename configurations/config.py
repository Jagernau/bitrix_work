from dotenv import dotenv_values

config = dotenv_values(".env")

# Define the bot token
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
