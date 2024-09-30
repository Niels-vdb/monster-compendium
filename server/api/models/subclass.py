from typing import Annotated
from pydantic import BaseModel, Field

from server.api.models.base_response import BaseResponse
from server.api.models.class_subclass_bases import ClassBase, SubclassBase


class SubclassModel(SubclassBase):
    """
    Extends the SubclassBase entity.

    - `id`: Unique identifier of the subclass.
    - `name`: Name of the subclass.
    - `parent_class`: The parent class of the subclass.
    """

    parent_class: ClassBase


class SubclassPostBase(BaseModel):
    """
    Schema for creating a new subclass.

    - `subclass_name`: Name of the subclass to be created, must be between 1 and 100 characters.
    - `class_id`: Id of the parent class.
    """

    subclass_name: Annotated[str, Field(min_length=1, max_length=100)]
    class_id: int


class SubclassPutBase(BaseModel):
    """
    Schema for updating a subclass.

    - `subclass_name`: New name of the subclass, must be between 1 and 100 characters.
    - `class_id`: New id of the parent class.
    """

    subclass_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    class_id: int | None = None


class SubclassResponse(BaseResponse):
    """
    Response model for creating or retrieving a subclass.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `subclass`: The actual subclass data, represented by the `SubclassModel`.
    """

    subclass: SubclassModel
