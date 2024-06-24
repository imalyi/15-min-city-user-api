import openrouteservice as ors
import os


class DistanceCalculator:
    def __init__(self):

        self.client = ors.Client(base_url=os.getenv("OSR_API_URL", 'http://192.168.0.105:8080/ors'))


    def calc_distance(self, coords):
        routes = self.client.directions(coords)
        try:
            distance = routes['routes'][0]['summary']['distance']  # Distance in meters
        except KeyError:
            return 99999999
        return distance