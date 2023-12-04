import abc
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import logging
from abc import ABC

logger = logging.getLogger(f"{__name__}_Database")
MONGO_CONNECT = "mongodb://gmaps:gmaps@192.168.0.100:28017/"
MONGO_DB_NAME = "15min"
MONGO_DB_HOST = 123


class Database(ABC):
    @abc.abstractmethod
    def add_item(self, item):
        pass


class DummyDatabase(Database):
    def add_item(self, item):
        print(item)


class MongoDatabase(Database):
    def __init__(self):
        self.__connect()

    def __connect(self):
        self.client = MongoClient()
        self.client = MongoClient(MONGO_CONNECT)
        self.db = self.client.get_database(MONGO_DB_NAME)

    def add_item(self, data):
        try:
            logger.debug(f"Creating document {data}")
            self.db['address'].insert_one(data.copy())
            logger.debug(f"Document created")
        except DuplicateKeyError:
            logger.debug(f"Document exist in db")

    def search(self, address: str):
        queryes = []
        for part in address.split(" "):
            pattern = re.compile(f".*{part}.*", re.IGNORECASE)
            queryes.append({"properties.full_address": {"$regex": pattern}})

        result = self.db['gmaps'].find({
            "$and":
                queryes
        }).limit(4)
        return result or []


def get_database() -> Database:
    if MONGO_DB_HOST is None:
        return DummyDatabase()
    else:
        return MongoDatabase()