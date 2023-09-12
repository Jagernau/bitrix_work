from typing import Final

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT 

from utils.singleton import SingletonMeta

class Database(metaclass=SingletonMeta): 
    BASE: Final = declarative_base()

    def __init__(self):
        self.__engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        self.__session = session()

    @property 
    def session(self): 
        return self.__session

    @property
    def engine(self): 
        return self.__engine


