from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.base_response import BaseResponse


class AttributeModel(BaseModel):
    """
    Represents an attribute entity.

    - `id`: Unique identifier of the attribute.
    - `name`: Name of the attribute.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AttributePostBase(BaseModel):
    """
    Schema for creating a new attribute.

    - `attribute_name`: Name of the attribute to be created, must be between 1 and 50 characters.
    """

    attribute_name: Annotated[str, Field(min_length=1, max_length=50)]


class AttributePutBase(BaseModel):
    """
    Schema for updating an attribute.

    - `attribute_name`: Updated name of the attribute, must be between 1 and 50 characters.
    """

    attribute_name: Annotated[str, Field(min_length=1, max_length=50)]


class AttributeResponse(BaseResponse):
    """
    Response model for creating or retrieving an attribute.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `attribute`: The actual attribute data, represented by the `AttributeModel`.
    """

    attribute: AttributeModel


class PostAttribute(BaseModel):
    """
    Schema used for adding an attribute to a newly created creature, race or subrace.

    - `attribute_id`: The id of the attribute.
    - `condition`: Optional information for when this attribute is active.
    """

    attribute_id: int
    condition: str | None = None


class PutAttribute(BaseModel):
    """
    Schema used for updating an attribute to a creature, race or subrace.

    - `attribute_id`: The id of the attribute.
    - `add_attribute`: Boolean for adding (True) or deleting (False) the attribute.
    - `condition`: Optional information for when this attribute is active.
    """

    attribute_id: int
    add_attribute: bool
    condition: str | None = None
