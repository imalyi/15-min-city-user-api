import openrouteservice as ors

class DistanceCalculator:
    def __init__(self):

        self.client = ors.Client(base_url="http://node:8080/ors")


    def calc_distance(self, coords):
        routes = self.client.directions(coords)
        try:
            distance = routes['routes'][0]['summary']['distance']  # Distance in meters
        except KeyError:
            return 99999999
        return distance

# use example
#res = c.calc_distance([[18.487937326403967, 54.35130292823335], [18.584439363376403, 54.35428968560705]])