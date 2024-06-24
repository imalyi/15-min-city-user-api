from report_generator.address_to_coordinates import AddressToGeoCoordinates
from report_generator.report_generator import ReportGenerator

class Report:
    def __init__(self, address: str, max_distance: int) -> None:
        self._address_to_cordinates = AddressToGeoCoordinates(address)
        
        lat = self._address_to_cordinates.latitude
        lon = self._address_to_cordinates.longitude
        self._report_generator = ReportGenerator(lat, lon, max_distance)
    
    @property
    def report(self):
        return self._report_generator.generate_report()
    

r = Report("Aleja Grunwaldzka 195/197", 555)
print(r.report)