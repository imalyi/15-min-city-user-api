import json
import re
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import logging

logger = logging.getLogger(f"{__name__}_Database")

MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", '15min')
MONGO_CONNECT = os.environ.get("MONGO_CONNECT")


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

    def get_report(self, address: str, requested_categories: list[dict], requested_objects: list[dict], requested_addresses: list[dict]=[]):
        filter = self.__generate_filters_for_report(requested_categories)
        document = self.db['address'].find_one({"address.full": address}, filter)
        document['custom_objects'] = self.__fetch_custom_objects_for_report(address, requested_objects)
        document['custom_addresses'] = self.__fetch_custom_addresses_for_report(requested_addresses)
        return document

    def __generate_filters_for_report(self, requested_categories: list[dict]):
        res = {'_id': 0, 'address': 1, 'location': 1, 'source': 1}
        for requested_category in requested_categories:
            res[f"points_of_interest.{requested_category.get('main_category')}.{requested_category.get('category')}"] = 1
        return res

    def __fetch_custom_objects_for_report(self, address, requested_objects: list[dict]):
        custom_objects = {}
        full_document = self.db['address'].find_one({"address.full": address}, {'_id': 0})
        for requested_object in requested_objects:
            main_category = requested_object['main_category']
            category = requested_object['category']
            name = requested_object['name']

            if not custom_objects.get(main_category):
                custom_objects[main_category] = {}
                custom_objects[main_category][category] = []
            elif not custom_objects.get(main_category).get(category):
                custom_objects[main_category][category] = []

            for poi in full_document.get('points_of_interest', {}).get(main_category, {}).get(category, []):
                if poi.get('name') == name:
                    custom_objects[main_category][category].append(poi)
        return custom_objects

    def __fetch_custom_addresses_for_report(self, requested_addresses: list[dict]):
        custom_addresses = {}
        for address in requested_addresses:
            address_document = self.db['address'].find_one({"address.full": address}, {'_id': 0, 'points_of_interest': 0})
            custom_addresses[address] = address_document
        return custom_addresses

    def get_categories(self, partial_name: str=None):
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



