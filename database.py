import re
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import logging
from bson import ObjectId

logger = logging.getLogger(f"{__name__}_Database")

MONGO_DB_HOST = os.environ.get("MONGO_DB_HOST", "bed")
MONGO_DB_PORT = os.environ.get("MONGO_DB_PORT", 28017)
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", '15min')
MONGO_DB_USERNAME = os.environ.get("MONGO_DB_USERNAME", 'gmaps')
MONGO_DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD", 'gmaps')
MONGO_CONNECT = os.environ.get("MONGO_CONNECT", f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}/")


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

        return [{"address": doc.get('address').get('full'), "id": str(doc.get('_id')), 'location': doc.get('location')} for doc in result]

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

    def get_name_by_id(self, category_id):
        try:
            category_id = int(category_id)
        except ValueError:
            return None
        for category in self.db['categories'].find({}, {"_id": 0}):
            for category_name, category_data in category.items():
                for row in category_data:
                    if row.get('id') == category_id:
                        return row.get('name').lower()

    def get_report_from_id(self, address_id: str, categories_ids: list):
        requested_categories = [self.get_name_by_id(category_id) for category_id in categories_ids]
        specified_id = ObjectId(address_id)
        address_document = self.db['address'].find_one({"_id": specified_id})
        result_dict = {
            'request': {
                'address': address_document.get('address', {}).get('full'),
                'location': address_document.get('location')
            },
            'osm': {
                'points_of_interest': {}
            }
        }

        if address_document:
            points_of_interests = address_document.get('points_of_interest', {})

            for amenity_name, amenities_list in points_of_interests.items():
                if amenity_name not in requested_categories:
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
                result_dict['osm']['points_of_interest'][amenity_name] = extracted_amenities
        return result_dict

    def get_all_categories(self):
        categories_cursor = self.db['categories'].find({}, {'_id': 0})
        categories_list = list(categories_cursor)
        return categories_list

    def _create_index_for_location(self):
        result = self.db['address'].create_index([("location", "2dsphere")])

