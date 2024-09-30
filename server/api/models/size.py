from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.base_response import BaseResponse


class SizeModel(BaseModel):
    """
    Represents a size entity.

    - `id`: Unique identifier of the size.
    - `name`: Name of the size.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SizePostBase(BaseModel):
    """
    Schema for creating a new size.

    - `size_name`: Name of the size to be created, must be between 1 and 50 characters.
    """

    size_name: Annotated[str, Field(min_length=1, max_length=50)]


class SizePutBase(BaseModel):
    """
    Schema for updating an size.

    - `size_name`: Updated name of the size, must be between 1 and 50 characters.
    """

    size_name: Annotated[str, Field(min_length=1, max_length=50)]


class SizeResponse(BaseResponse):
    """
    Response model for creating or retrieving a size.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `size`: The actual size data, represented by the `RoleModel`.
    """

    size: SizeModel
