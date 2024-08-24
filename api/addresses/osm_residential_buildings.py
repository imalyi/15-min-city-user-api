import logging
import json
from pyrosm import OSM, get_data

import json


class AddressDTO:
    street_name: str
    house_number: str
    postcode: str
    city: str
    geometry_raw: list

    def __init__(
        self,
        *,
        street_name,
        house_number,
        city: str,
        postcode: str,
        geometry_raw,
    ) -> None:
        self.street_name = street_name
        self.house_number = house_number
        self.city = city
        self.geometry_raw = geometry_raw
        self.postcode = postcode

        self.required_attributes = [
            self.street_name,
            self.house_number,
            self.city,
        ]

        if not self._check_is_required_attributes_not_empty():
            raise InvalidDTOException

    def _check_is_required_attributes_not_empty(self):
        return all(self.required_attributes)

    @property
    def geometry(self):
        return {"type": "MultiPolygon", "coordinates": [self.geometry_raw]}

    def to_dict(self):
        res = {
            "streetName": self.street_name,
            "houseNumber": self.house_number,
            "city": self.city,
            "geometry": self.geometry,
        }
        if self.postcode:
            res["postcode"] = self.postcode
        return res

    def __repr__(self):
        return f"{self.street_name} {self.house_number}, {self.city} {self.postcode}"

    def __str__(self):
        return f"{self.street_name} {self.house_number}, {self.city} {self.postcode}"

    def __hash__(self) -> int:
        return hash(self.street_name + self.house_number + self.city)

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return (
            value.street_name == self.street_name
            and value.house_number == self.house_number
            and value.city == self.city
        )


class Report:
    def __init__(self) -> None:
        self.address_exists = []
        self.address_bad = []
        self.address_ok = []
        self.address_new = []

    def mark_address_ok(self, address: AddressDTO):
        "Use when address has geometry and valid street name, house number or city"
        self.address_ok.append(address)

    def mark_address_as_bad(self, address: AddressDTO):
        "Use when address has invalid geometry or invalid street name, house number or city"
        self.address_bad.append(address)

    def mark_address_exists(self, address: AddressDTO):
        "Use when address succesfully sent to API and receive 409"
        self.address_exists.append(address)

    def mark_address_new(self, address: AddressDTO):
        "Use when address unsuccesfully sent to API and receive HTTP CREATED"
        self.address_new.append(address)

    @property
    def mark_address_exists_count(self):
        return len(self.address_exists)

    @property
    def address_bad_count(self):
        return len(self.address_bad)

    @property
    def address_new_count(self):
        return len(self.address_new)

    @property
    def address_ok_count(self):
        return len(self.address_ok)

    @property
    def stats(self):
        return {
            "exists": {
                "count": self.mark_address_exists,
            },
            "ok": {"count": self.address_ok_count},
            "bad": {
                "count": self.address_bad_count,
                # "addresses": self.address_bad,
            },
        }


class BadGeometryException(Exception):
    pass


class NoGeometryException(Exception):
    pass


class InvalidDTOException(Exception):
    pass


class Geometry:
    def __init__(self, geometry) -> None:
        self.geometry = geometry

    @property
    def coords(self):
        """Extract coordinates from the building geometry."""
        if self.geometry.geom_type == "Polygon":
            return [list(self.geometry.exterior.coords)]
        elif self.geometry.geom_type == "MultiPolygon":
            coords = []
            for poly in self.geometry.geoms:
                coords.extend(list(poly.exterior.coords))
            return [coords]
        raise NoGeometryException

    def to_list(self):
        return self.coords

    def __str__(self):
        if hasattr(self.geometry, "exterior"):
            return str(len(self.geometry.exterior.coords))
        elif hasattr(self.geometry, "geoms"):
            return str(
                sum(len(poly.exterior.coords) for poly in self.geometry.geoms)
            )
        elif hasattr(self.geometry, "coords"):
            return str(len(self.geometry.coords))
        else:
            return "0"


class OSMResidentialBuildings:
    def __init__(self, *, osm, report: Report):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.osm = osm
        self.report = report
        self._data = self.get_buildings()
        self.buildings_iterator = iter(self._data)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.buildings_iterator)
        except StopIteration:
            self.buildings_iterator = iter(self._data)
            raise StopIteration

    def _create_address_dto(self, building):
        street_name = building["addr:street"]
        house_number = building.get("addr:housenumber", "")
        city = building.get("addr:city")
        postcode = building.get("addr:postcode", None)

        try:
            geometry = Geometry(building.geometry)
            geometry_raw = geometry.to_list()

        except NoGeometryException:
            geometry_raw = None

        address_dto = AddressDTO(
            street_name=street_name,
            house_number=house_number,
            city=city,
            postcode=postcode,
            geometry_raw=geometry_raw,
        )
        if geometry_raw:
            return address_dto
        else:
            self.report.mark_address_as_bad(address_dto)
            raise InvalidDTOException

    def get_buildings(self) -> set:
        logging.info("Start loading residential buildings info..")
        buildings = self.osm.get_buildings()
        buildings_set = set()
        building_count = 0
        for index, building in buildings.iterrows():
            try:
                address_dto = self._create_address_dto(building)
                buildings_set.add(address_dto)
                building_count += 1
                self.report.mark_address_ok(address_dto)
            except InvalidDTOException:
                continue
        return buildings_set

    def __len__(self):
        return len(self._data)
