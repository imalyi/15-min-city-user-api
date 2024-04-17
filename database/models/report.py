from pydantic import BaseModel
from typing import List, Dict, Union
from pydantic import BaseModel



class AddressIn(BaseModel):
    name: str

class Category(BaseModel):
    sub_name: str
    main_name: str

class RequestedObject(BaseModel):
    name: str
    category: Category

class ReportIn(BaseModel):
    address: AddressIn
    categories: list[Category]
    requested_objects: list[RequestedObject]
    requested_address: list[AddressIn]


#---------------------------------------------


class AddressOut(BaseModel):
    city: str
    housenumber: str
    street: str
    full: str

class Location(BaseModel):
    lat: float
    lon: float

class PointOfInterest(BaseModel):
    name: str
    location: Location
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
    location: Location
    commute_time: CommuteTime


class ReportOut(BaseModel):
    address: AddressOut
    location: Location
    points_of_interest: Dict[str, Dict[str, List[PointOfInterest]]]



test_address = AddressOut(
    city="Gdańsk",
    housenumber="195/197",
    street="Aleja Grunwaldzka",
    full="Aleja Grunwaldzka 195/197, Gdańsk"
)

test_location = Location(lat=54.3869986856996, lon=18.592315953952824)

test_point_of_interest = PointOfInterest(
    name="Bar AKA",
    location=Location(lat=54.3808318, lon=18.6050847),
    address=AddressOut(city="Gdańsk", housenumber="", street="Klonowa 4", full="Klonowa 4, Gdańsk"),
    distance=1144.993
)

test_commute_time_unit = CommuteTimeUnit(distance=5.0, duration=10.0)

test_commute_time = CommuteTime(
    walk=test_commute_time_unit,
    drive=test_commute_time_unit,
    transit=test_commute_time_unit,
    bike=test_commute_time_unit
)

test_custom_address = CustomAddress(
    address=test_address,
    location=test_location,
    commute_time=test_commute_time
)

test_points_of_interest = {
    "Gastronomia": {
        "Fast Food": [test_point_of_interest]
    }
}

test_report_out = ReportOut(
    address=test_address,
    location=test_location,
    points_of_interest=test_points_of_interest
)

import json
print(test_report_out.model_dump()) 
