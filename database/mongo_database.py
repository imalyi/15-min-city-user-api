import re
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import logging

logger = logging.getLogger(f"{__name__}_Database")

MONGO_DB_HOST = os.environ.get("MONGO_DB_HOST", "cluster0.eof3k8h.mongodb.net")
MONGO_DB_PORT = os.environ.get("MONGO_DB_PORT", 28017)
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", '15min')
MONGO_DB_USERNAME = os.environ.get("MONGO_DB_USERNAME", '2wtarX4YfclfC4t3')
MONGO_DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD", 'Spx9X6Hb7tDWidVS')
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
        categories = self.db['categories'].find_one({}, {"_id": 0})
        categories_synonyms = []
        for category in requested_categories:
            for main_category, sub_categories in categories.items():
                if sub_categories.get(category):
                    categories_synonyms.extend(sub_categories.get(category))

        try:
            result_dict = {
                'request': {
                    'address': address_document.get('address', {}).get('full'),
                    'location': address_document.get('location')
                },
                'osm': {
                    'points_of_interest': {}
                }
            }
        except AttributeError:
            return {}
        if address_document:
            points_of_interests = address_document.get('points_of_interest', {})

            for amenity_name, amenities_list in points_of_interests.items():
                if amenity_name not in categories_synonyms:
                    continue
                extracted_amenities = [
                    {
                        'name': amenity.get('name', ''),
                        'location': amenity.get('location', []),
                        'distance': amenity.get('distance', -1),
                        'tags': amenity.get('tags', {}),
                        'source': amenity.get('source', 'unknown'),
                        'address': amenity.get('address', {})
                    }
                    for amenity in amenities_list
                ]
                extracted_amenities.sort(key=lambda x: x['distance'], reverse=False)
                result_dict['osm']['points_of_interest'][amenity_name.capitalize()] = extracted_amenities
        return result_dict

    def get_categories(self, partial_name: str=None):
        data = self.db['categories'].find_one({}, {'_id': 0})
        res = {}
        for main_key, sub_keys in data.items():
            for sub_key, _ in sub_keys.items():
                if not res.get(main_key):
                    res[main_key] = []
                res[main_key].append(sub_key)
        return res

    def _create_index_for_location(self):
        result = self.db['address'].create_index([("location", "2dsphere")])


