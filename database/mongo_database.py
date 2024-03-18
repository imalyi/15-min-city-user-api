import re
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import logging

logger = logging.getLogger(f"{__name__}_Database")

MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", '15min')
MONGO_CONNECT = os.environ.get("MONGO_CONNECT", f"mongodb+srv://2wtarX4YfclfC4t3:Spx9X6Hb7tDWidVS@cluster0.eof3k8h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


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

    def search_by_coordinates(self, lon: float, lat: float):
        query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "$maxDistance": 300
                }
            }
        }
        result = self.db['address'].find(query).limit(10)
        return [{"address": doc.get('address', {}).get('full'), "id": str(doc.get('_id'))} for doc in result]

    def get_report(self, address: str, requested_categories: list[str]):
        address_document = self.db['address'].find_one({"address.full": address})
        try:
            result = {
                'address': address_document['address']['full'],
                'location': address_document['location'],
                'points_of_interest': {
                }
            }

        except AttributeError:
            return {}
        for main_category, sub_categories in address_document.get('points_of_interest', {}).items():
            for requested_category in requested_categories:
                if requested_category in sub_categories:
                    if not result['points_of_interest'].get(main_category):
                        result['points_of_interest'][main_category] = {}
                    result['points_of_interest'][main_category][requested_category] = sub_categories[requested_category]
        return result

    def get_categories(self, partial_name: str=None):
        data = self.db['categories'].find_one({}, {'_id': 0})
        return data

    def _create_index_for_location(self):
        result = self.db['address'].create_index([("location", "2dsphere")])

