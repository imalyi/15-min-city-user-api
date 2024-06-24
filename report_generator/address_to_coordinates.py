from database.models import Location, ResidentialBuilding
from exceptions import AdressNotFoundException


class AddressToGeoCoordinates:
    def __init__(self, address: str) -> None:
        self.address = address
        self._coordinates = self._convert_address_to_coordinates()

    def _convert_address_to_coordinates(self) -> Location:
        residential_building = ResidentialBuilding.objects(address__street=self.address).first()
        if not residential_building:
            raise AdressNotFoundException(f"{self.address} not found in database")
        return residential_building.location.latitude, residential_building.location.longitude

    @property
    def latitude(self):
        return self._coordinates[0]

    @property
    def longitude(self):
        return self._coordinates[1]
