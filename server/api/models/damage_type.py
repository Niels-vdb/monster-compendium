from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.base_response import BaseResponse


class DamageTypeModel(BaseModel):
    """
    Represents an damage type entity.

    - `id`: Unique identifier of the damage type.
    - `name`: Name of the damage type.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DamageTypePostBase(BaseModel):
    """
    Schema for creating a new damage type.

    - `damage_type_name`: Name of the damage type to be created, must be between 1 and 50 characters.
    """

    damage_type_name: Annotated[str, Field(min_length=1, max_length=50)]


class DamageTypePutBase(BaseModel):
    """
    Schema for updating an damage type.

    - `damage_type_name`: Name of the damage type to be created, must be between 1 and 50 characters.
    """

    damage_type_name: Annotated[str, Field(min_length=1, max_length=50)]


class DamageTypeResponse(BaseResponse):
    """
    Response model for creating or retrieving an damage type.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `damage_type`: The actual damage type data, represented by the `AttributeModel`.
    """

    damage_type: DamageTypeModel


class PostDamageType(BaseModel):
    """
    Schema used for adding a damage type to a newly created creature, race or subrace.

    - `damage_type_id`: The id of the damage type.
    - `condition`: Optional information for when this damage type is active.
    """

    damage_type_id: int
    condition: str | None = None


class PutDamageType(BaseModel):
    """
    Schema used for updating a damage type to a creature, race or subrace.

    - `damage_type_id`: The id of the damage type.
    - `add_damage_type`: Boolean for adding (True) or deleting (False) the damage type.
    - `condition`: Optional information for when this damage type is active.
    """

    damage_type_id: int
    add_damage_type: bool
    condition: str | None = None
