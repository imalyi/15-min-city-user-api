from database.models import POI
from distance import DistanceCalculator
import geojson
from address_to_coordinates import AddressToGeoCoordinates


class ReportGenerator:
    def __init__(self, latitude: float, longitude: float, max_distance) -> None:
        self._distance_calculator = DistanceCalculator()
        self._max_distance = max_distance
        self.longitude = longitude
        self.latitude = latitude

    def _find_pois_in_box(self):
        distance_deg = self._max_distance / 111.0 / 1000
        lower_left = (self.longitude - distance_deg,  self.longitude - distance_deg)
        upper_right = (self.latitude + distance_deg, self.latitude + distance_deg)
        pois = POI.objects(__raw__={"location": {"$geoWithin": {"$box": [upper_right, lower_left]}}})
        return pois

    def _validate_distance(self):
        result = []
        for poi in self._find_pois_in_box():
            try:
                distance= self._distance_calculator.calc_distance([(self.longitude, self.latitude), (poi.location.longitude, poi.location.latitude)])
            except: 
                pass
            if distance < self._max_distance:
                result.append(poi)
        return result

    def generate_report(self):
        features = []
        
        for poi in self._find_pois_in_box():
            feature = geojson.Feature(
                geometry=geojson.Point((poi.location.longitude, poi.location.latitude)),
                properties={
                    "name": poi.name,
                    "categories": {
                        "main": poi.categories.main,
                        "sub": poi.categories.sub
                    },
                    "address": {
                        "city": poi.address.city,
                        "postcode": poi.address.postcode,
                        "street": poi.address.street
                    }
                }
            )
            features.append(feature)        
        return geojson.FeatureCollection(features) 


class Report:
    def __init__(self, address: str, max_distance: int) -> None:
        self._address_to_cordinates = AddressToGeoCoordinates(address)
        
        lat = self._address_to_cordinates.latitude
        lon = self._address_to_cordinates.longitude
        self._report_generator = ReportGenerator(lat, lon, max_distance)
    
    @property
    def report(self):
        return self._report_generator.generate_report()
    