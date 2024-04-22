from pydantic import BaseModel
from typing import List, Dict, Union
from pydantic import BaseModel, RootModel
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, field_serializer, Field, ConfigDict


class AddressIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str

class Category(BaseModel):
    model_config = ConfigDict(extra="forbid")
    main_category: str
    category: str

class RequestedObject(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    category: Category

class ReportIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: AddressIn
    categories: list[Category]
    requested_objects: list[RequestedObject]
    requested_address: list[AddressIn]


#---------------------------------------------


class AddressOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    city: str
    housenumber: str
    street: str
    full: str


class Location(BaseModel):
    model_config = ConfigDict(extra="forbid")
    location: list[float]

class PointOfInterest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    location: list[float]
    address: AddressOut
    distance: float


class CommuteTimeUnit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    distance: float
    duration: float


class CommuteTime(BaseModel):
    model_config = ConfigDict(extra="forbid")
    walk: CommuteTimeUnit
    drive: CommuteTimeUnit
    transit: CommuteTimeUnit
    bike: CommuteTimeUnit


class CustomAddress(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: AddressOut
    location: List[float]
    commute_time: CommuteTime


class ReportOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: AddressOut
    location: list[float]
    points_of_interest: Dict[str, Dict[str, List[PointOfInterest]]] | None
    custom_addresses: List[CustomAddress] | None
    custom_objects: Dict[str, Dict[str, list[PointOfInterest]]] | None


class ReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: str
    categories: List[Category]
    requested_objects: Optional[List[Dict]]
    requested_addresses: Optional[List]



class Object_(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    category: str
    sub_category: str

class Objects(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objects: List[Object_]
    addresses: List[str]

class Language(Enum):
    pl = "pl"
    en = "en"
    de = "de"

class UserDataIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    secret: str
    language: Language
    addresses: List[str] = []
    requested_objects: Optional[List[Dict]] = []
    requested_addresses: Optional[List] = []
    categories: List[Dict]

    @field_serializer("language")
    def serialize_language(self, value):
        return value.value