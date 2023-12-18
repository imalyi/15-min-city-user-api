import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
import os
import logging
from bson import ObjectId
import random

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
        result = self.db['address'].find(query).limit(50)
        return [{"address": doc.get('full'), "id": str(doc.get('_id'))} for doc in result]

    def get_report_from_id(self, address_id: str):
        specified_id = ObjectId(address_id)
        address_document = self.db['address'].find_one({"_id": specified_id})
        result_dict = {
            'request': {
                'address': address_document.get('address', {}).get('full'),
                'location': address_document.get('location')
            },
            'osm': {
                'points_of_interest': {}  # Initialize the 'points_of_interest' dictionary
            }
        }

        if address_document:
            points_of_interests = address_document.get('points_of_interest', {})

            for amenity_name, amenities_list in points_of_interests.items():
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
                result_dict['osm']['points_of_interest'][amenity_name] = extracted_amenities

        return result_dict
