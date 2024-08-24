import requests
from api.pois.stop import Stop

STOPS_URL = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json"


class Stops:
    def __init__(self, *, city: str, stop_type: str) -> None:
        self._data = set()
        self._city = city
        self._stop_type = stop_type
        self._parse()

    def _parse(self) -> None:
        page = requests.get(STOPS_URL).json()
        stops = page[list(page.keys())[0]]["stops"]
        self._data = set(
            Stop(
                name=f"{stop['stopDesc']} {stop['stopCode']}",
                lat=stop["stopLat"],
                lon=stop["stopLon"],
            )
            for stop in stops
            if stop["nonpassenger"] is not None
            and self._check_stop_type(stop["type"])
        )

    def _check_stop_type(self, stop_type):
        return self._stop_type == stop_type

    def __iter__(self):
        return iter(self._data)
