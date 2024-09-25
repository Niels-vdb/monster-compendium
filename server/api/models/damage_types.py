from pydantic import BaseModel


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
