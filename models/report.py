from pydantic import BaseModel
from typing import List, Dict, Union
from pydantic import BaseModel, RootModel


class AddressIn(BaseModel):
    name: str

class Categories(RootModel):
    root: Dict[str, List[str]]

class RequestedObject(BaseModel):
    name: str
#    category: Category

class ReportIn(BaseModel):
    address: AddressIn
#    categories: list[Category]
    requested_objects: list[RequestedObject]
    requested_address: list[AddressIn]


#---------------------------------------------


class AddressOut(BaseModel):
    city: str
    housenumber: str
    street: str
    full: str


class Location(BaseModel):
    location: list[float]

class PointOfInterest(BaseModel):
    name: str
    location: list[float]
    address: AddressOut
    distance: float


class CommuteTimeUnit(BaseModel):
    distance: float
    duration: float


class CommuteTime(BaseModel):
    walk: CommuteTimeUnit
    drive: CommuteTimeUnit
    transit: CommuteTimeUnit
    bike: CommuteTimeUnit


class CustomAddress(BaseModel):
    address: AddressOut
    location: list[float]
    commute_time: CommuteTime


class ReportOut(BaseModel):
    address: AddressOut
    location: list[float]
    points_of_interest: Dict[str, Dict[str, List[PointOfInterest]]]
    custom_addresses: dict[str, CustomAddress]


