from pydantic import BaseModel
from pydantic_extra_types.coordinate import Longitude, Latitude


class AddressCreate(BaseModel):
    street: str
    city: str
    postcode: str
    lat: Latitude
    lng: Longitude


class Address(AddressCreate):
    id: int
