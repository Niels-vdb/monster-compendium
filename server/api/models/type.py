from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.base_response import BaseResponse


class TypeModel(BaseModel):
    """
    Represents a type entity.

    - `id`: Unique identifier of the type.
    - `name`: Name of the type.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TypePostBase(BaseModel):
    """
    Schema for creating a new type.

    - `type_name`: Name of the type to be created, must be between 1 and 50 characters.
    """

    type_name: Annotated[str, Field(min_length=1, max_length=50)]


class TypePutBase(BaseModel):
    """
    Schema for updating an type.

    - `type_name`: Updated name of the type, must be between 1 and 50 characters.
    """

    type_name: Annotated[str, Field(min_length=1, max_length=50)]


class TypeResponse(BaseResponse):
    """
    Response model for creating or retrieving an type.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `type`: The actual type data, represented by the `TypeModel`.
    """

    type: TypeModel
