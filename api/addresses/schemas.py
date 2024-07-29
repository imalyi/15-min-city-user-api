from pydantic import ConfigDict, Field, field_validator
import re

from api.schemas.global_model import GlobalModelWithJSONAlias
from geojson_pydantic import MultiPolygon
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from api.addresses.models import Address as AddressModel


class CommonAddressAttributes(GlobalModelWithJSONAlias):
    street_name: str = Field(min_length=3, max_length=150)
    house_number: str = Field(min_length=1, max_length=150)
    city: str = Field(min_length=3, max_length=150)
    postcode: Optional[str] = None

    @field_validator("city")
    def city_validator(cls, v):
        pattern = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż ]+$")
        if bool(pattern.match(v)):
            return v
        raise ValueError("City can contain only polish letters, and '.'")

    @field_validator("postcode")
    def validate_postcode(cls, v):
        pattern = re.compile(r"^[0-9]{2}-[0-9]{3}$")
        if bool(pattern.match(v)):
            return v
        raise ValueError("Incorrect postcode format")


class Address(CommonAddressAttributes):
    id_: int = Field(alias="id")
    full_address: str


class AddressCreate(CommonAddressAttributes):
    model_config = ConfigDict(str_strip_whitespace=True)
    geometry: MultiPolygon


# TODO custom alias name generator
class AddressFilter(Filter, GlobalModelWithJSONAlias):
    lat: Optional[float] = None
    lon: Optional[float] = None
    street_name: Optional[str] = None
    street_type: Optional[str] = None
    house_number: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    order_by: list[str] = ["street_name"]
    full_address__ilike: Optional[str] = Field(
        default=None, alias="fullAdress__ilike"
    )
    street_name__ilike: Optional[str] = Field(
        default=None, alias="streetName__ilike"
    )
    city__ilike: Optional[str] = Field(default=None, alias="city__ilike")
    street_type__ilike: Optional[str] = Field(
        default=None, alias="streetType__ilike"
    )

    class Constants(Filter.Constants):
        model = AddressModel
