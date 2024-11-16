from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.base_response import BaseResponse
from server.api.models.class_subclass_bases import ClassBase, SubclassBase


class ClassModel(ClassBase):
    """
    Represents a class entity.

    - `id`: Unique identifier of the class.
    - `name`: Name of the class.
    - `subclasses`: List of related subclass entities.
    """

    subclasses: list[SubclassBase] | None

    model_config = ConfigDict(from_attributes=True)


class ClassPostBase(BaseModel):
    """
    Schema for creating a new class.

    - `class_name`: Name of the class to be created, must be between 1 and 50 characters.
    """

    class_name: Annotated[str, Field(min_length=1, max_length=50)]


class ClassPutBase(BaseModel):
    """
    Schema for updating a class.

    - `class_name`: Name of the class to be created, must be between 1 and 50 characters.
    """

    class_name: Annotated[str, Field(min_length=1, max_length=50)]


class ClassResponse(BaseResponse):
    """
    Response model for creating or retrieving a class.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `cls`: The actual class data, represented by the `ClassModel`.
    """

    cls: ClassModel
