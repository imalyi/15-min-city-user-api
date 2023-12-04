import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

import logging

logger = logging.getLogger(f"{__name__}_Database")

MONGO_CONNECT = "mongodb://gmaps:gmaps@bed:28017/"
MONGO_DB_NAME = "15min"
MONGO_DB_HOST = 123


class MongoDatabase():
    def __init__(self):
        self.__connect()

    def __connect(self):
        try:
            self.client = MongoClient(MONGO_CONNECT, serverSelectionTimeoutMS=2000)
            self.db = self.client.get_database(MONGO_DB_NAME)
        except ServerSelectionTimeoutError:
            logger.error("Failed to connect to MongoDB server")

    def search_by_partial_name(self, address: str):
        queries = [{"full": {"$regex": re.compile(f'.*{part}.*', re.IGNORECASE)}} for part in address.split()]
        try:
            result = self.db['address'].find({"$and": queries}).limit(5)
        except Exception as e:
            logger.error(f"Error executing MongoDB query: {e}")
            return []

        return [{"address": doc.get('full'), "id": str(doc.get('_id'))} for doc in result]

    def search_by_coordinates(self, lon: float, lat: float):
        query = {
            "location": {
                "$geoWithin": {
                    "$centerSphere": [[lon, lat], 0.013 / 6371]
                }
            }
        }
        result = self.db['address'].find(query).limit(5)
        return [{"address": doc.get('full'), "id": str(doc.get('_id'))} for doc in result]