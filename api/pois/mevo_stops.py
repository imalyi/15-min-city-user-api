import requests
from api.pois.stop import Stop

STOPS_URL = (
    "https://gbfs.urbansharing.com/rowermevo.pl/station_information.json"
)


CITY_CODES = {"Gdynia": "GDY", "Gdańsk": "GDA", "Sopot": "SOP"}


class City:
    def __init__(self, city: str) -> None:
        self.city = city

    @property
    def city_code(self):
        return CITY_CODES.get(self.city)

    def is_stopname_in_city(self, stopaname: str):
        return stopaname[:3] == self.city_code


class MevoStops:
    def __init__(self, city: str):
        self.stops = []
        self.city = City(city)
        self._parse()

    def _parse(self):
        page = requests.get(STOPS_URL).json()
        self.stops = set(
            Stop(**stop_data)
            for stop_data in page["data"]["stations"]
            if self.city.is_stopname_in_city(stop_data["name"])
        )

    def __iter__(self):
        return iter(self.stops)
