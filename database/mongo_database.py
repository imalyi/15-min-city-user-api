import re
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import logging

MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", '15min')
MONGO_CONNECT = os.environ.get("MONGO_CONNECT", "mongodb://root:example@node:27777/")

logger = logging.getLogger(f"{__name__}_Database")


class MongoDatabase:
    def __init__(self):
        self.__connect()
        self._create_index_for_location()

    def __connect(self):
        try:
            self.client = MongoClient(MONGO_CONNECT, serverSelectionTimeoutMS=2000)
            self.db = self.client.get_database(MONGO_DB_NAME)
        except ServerSelectionTimeoutError:
            logger.error("Failed to connect to MongoDB server")

    def search_by_partial_name(self, address: str):
        queries = [{"address.full": {"$regex": re.compile(f'.*{part}.*', re.IGNORECASE)}} for part in address.split()]
        try:
            result = self.db['address'].find({"$and": queries}).limit(5)
        except Exception as e:
            logger.error(f"Error executing MongoDB query: {e}")
            return []
        return [doc.get('address').get('full') for doc in result]

    def get_categories(self):
        data = self.db['categories'].find_one({}, {'_id': 0})
        return data

    def _create_index_for_location(self):
        self.db['address'].create_index([("location", "2dsphere")])

    def search_object_by_partial_name(self, name: str) -> list:
        queries = [{"name": {"$regex": re.compile(f'.*{part}.*', re.IGNORECASE)}} for part in name.split()]
        try:
            result = self.db['pois_names'].find({"$and": queries}).limit(5)
        except Exception as e:
            logger.error(f"Error executing MongoDB query: {e}")
            return []

        return [{'name': doc.get('name'), 'category': doc.get('category'), 'sub_category': doc.get('sub_category')} for doc in result]
