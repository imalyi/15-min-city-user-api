from pydantic_extra_types.coordinate import Longitude, Latitude
from pydantic import ConfigDict, Field, computed_field
from typing import List

# from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude
from geojson_pydantic import MultiPolygon


class Coordinate(BaseModel):
    lng: Longitude
    lat: Latitude


class AddressCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    street: str
    city: str
    postcode: str
    geometry: MultiPolygon


class Address(AddressCreate):
    id_: int = Field(alias="id")
