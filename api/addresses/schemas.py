from pydantic import ConfigDict, Field, validator
import re

from api.schemas.global_model import GlobalModelWithJSONAlias
from geojson_pydantic import MultiPolygon
from typing import Optional


class CommonAddressAttributes(GlobalModelWithJSONAlias):
    street_name: str = Field(min_length=5, max_length=150)
    house_number: str = Field(min_length=1, max_length=150)
    street_type: Optional[str] = None
    city: str = Field(min_length=3, max_length=150)
    postcode: Optional[str] = None

    #    @validator("street_name", "street_number")
    #    def street_validator(cls, v):
    #        pattern = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż. 0-9]+$")
    #        if bool(pattern.match(v)):
    #            return v
    #        raise ValueError("Street can contain only polish letters, and '.'")

    @validator("city")
    def city_validator(cls, v):
        pattern = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż ]+$")
        if bool(pattern.match(v)):
            return v
        raise ValueError("City can contain only polish letters, and '.'")

    @validator("postcode")
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
