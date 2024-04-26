from .model import UserDataIn, UserDataIn, ReportRequest, ReportOut, SavedReportsOut
from pydantic import ValidationError
from .googlemaps_distance_calculator import GoogleMapsDistanceCalculator
from typing import List
from .mongo_database import MongoDatabase 

class ReportModel:
    def __init__(self):
        self._db = MongoDatabase().db

    def save_report(self, report: UserDataIn):
        print(report)
        self._db['user_data'].delete_one({"secret": report.get('secret')})
        self._db['user_data'].insert_one(report)

    def load_report_by_id(self, secret: str):
        user_request = self._db['user_data'].find_one({"secret": secret}, {"_id": 0})
        data = []
        for address in user_request.get('addresses'):
            report_request = ReportRequest(
                address=address,
                categories=user_request.get('categories'),
                requested_objects=user_request.get("requested_objects"),
                requested_addresses=user_request.get("requested_addresses")
            )
            data.append(self.get_report(report_request.model_dump()))
        return SavedReportsOut(language=user_request.get('language'), secret=user_request.get("secret"), reports=data)

    def get_report(self, requested_report: ReportRequest) -> dict:
        filter_ = self.__generate_filters_for_report(requested_report.get('categories'))
        document = self._db['address'].find_one({"address.full": requested_report.get('address')}, filter_)
        document['custom_objects'] = self.__fetch_custom_objects_for_report(requested_report.get('address'), requested_report.get('requested_objects'))
        document['custom_addresses'] = self.__fetch_custom_addresses_for_report(requested_report.get('address'), requested_report.get('requested_addresses'))
        return document

    def __generate_filters_for_report(self, requested_categories: list[dict]):
        res = {'_id': 0, 'address': 1, 'location': 1, 'source': 1}
        for requested_category in requested_categories:
            res[f"points_of_interest.{requested_category.get('main_category')}.{requested_category.get('category')}"] = 1
        return res

    def __fetch_custom_objects_for_report(self, address, requested_objects: list[dict]):
        custom_objects = {}
        full_document = self._db['address'].find_one({"address.full": address}, {'_id': 0})
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

    def __fetch_custom_addresses_for_report(self, my_address: str, requested_addresses: list[dict]):
        custom_addresses = []
        for address in requested_addresses:
            address_document = self._db['address'].find_one({"address.full": address}, {'_id': 0, 'points_of_interest': 0})         
            address_document['commute_time'] = GoogleMapsDistanceCalculator(from_=my_address).calc(address)
            custom_addresses.append(address_document)
        return custom_addresses

    def __fetch_custom_addresses_commute_timne(self, address, requested_address):
        return GoogleMapsDistanceCalculator(address).calc(requested_address)

class ReportGenerator:
    def __init__(self) -> None:
        self._model = ReportModel()

    def generate(self, requested_report: ReportRequest) -> ReportOut:
        return self._model.get_report(requested_report)

    def save(self, user_data: UserDataIn) -> None:
        UserDataIn.model_validate(user_data)
        self._model.save_report(user_data)
    
    def load(self, secret: str) -> SavedReportsOut:
        data = self._model.load_report_by_id(secret)
        return data
