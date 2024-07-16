from pydantic import ConfigDict, Field

from api.schemas.global_model import GlobalModelWithJSONAlias
from geojson_pydantic import MultiPolygon


class CommonAddressAttributes(GlobalModelWithJSONAlias):
    street: str
    city: str
    postcode: str


class Address(CommonAddressAttributes):
    id_: int = Field(alias="id")
    full_address: str


class AddressCreate(CommonAddressAttributes):
    model_config = ConfigDict(str_strip_whitespace=True)
    geometry: MultiPolygon
