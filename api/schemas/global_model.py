from pydantic.alias_generators import to_camel
from pydantic import ConfigDict
from pydantic import BaseModel


class GlobalModelWithJSONAlias(BaseModel):
    """
    Used for every model
    """

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="allow"
    )
