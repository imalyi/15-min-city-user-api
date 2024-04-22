import os

import requests
import datetime


url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': os.getenv("GOOGLE_API_KEY"),
    'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
}


class GoogleMapsDistanceCalculatorGeneric:
    def calc(self):
        res = requests.post(url, headers=headers, json=self.data)
        print(res.text)
        duration = (int(res.json().get('routes')[0].get('duration').replace('s', '')))
        distance = (int(res.json().get('routes')[0].get('distanceMeters')))
        return {'distance': distance, 'duration': duration}


class GoogleMapsDistanceCalculatorWalk(GoogleMapsDistanceCalculatorGeneric):
    def __init__(self, from_, to):
        formatted_datetime = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.data = {
            "origin": {
                "address": from_
            },
            "destination": {
                "address": to
            },
            "travelMode": "WALK",
            "departureTime": formatted_datetime,
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "IMPERIAL"
        }


class GoogleMapsDistanceCalculatorBike(GoogleMapsDistanceCalculatorGeneric):
    def __init__(self, from_, to):
        formatted_datetime = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        self.data = {
            "origin": {
                "address": from_
            },
            "destination": {
                "address": to
            },
            "travelMode": "BICYCLE",
            "departureTime": formatted_datetime,
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "IMPERIAL"
        }


class GoogleMapsDistanceCalculatorCar(GoogleMapsDistanceCalculatorGeneric):
    def __init__(self, from_, to):
        formatted_datetime = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        self.data = {
            "origin": {
                "address": from_
            },
            "destination": {
                "address": to
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",
            "departureTime": formatted_datetime,
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "IMPERIAL"
        }


class GoogleMapsDistanceCalculatorPublicTransport(GoogleMapsDistanceCalculatorGeneric):
    def __init__(self, from_, to):
        formatted_datetime = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        self.data = {
            "origin": {
                "address": from_
            },
            "destination": {
                "address": to
            },
            "travelMode": "TRANSIT",
            "departureTime": formatted_datetime,
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "IMPERIAL"
        }


class GoogleMapsDistanceCalculator:
    def __init__(self, from_: str):
        self._from = from_
        self.calculators = {
            'walk': GoogleMapsDistanceCalculatorWalk,
            'drive': GoogleMapsDistanceCalculatorCar,
            'transit': GoogleMapsDistanceCalculatorPublicTransport,
            'bike': GoogleMapsDistanceCalculatorBike
        }

    def calc(self, to):
        res = {}
        for type, calculator in self.calculators.items():
            res[type] = calculator(from_=self._from, to=to).calc()
        return res

# Example usage
#g = GoogleMapsDistanceCalculator("al. Grunwaldzka 14, Gdansk")
#res = g.calc("al. Grunwaldzka 144, Gdansk")
#print(res)
