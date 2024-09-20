from pydantic import BaseModel


class PostDamageType(BaseModel):
    damage_type_id: int
    condition: str


class PutDamageType(BaseModel):
    damage_type_id: int
    condition: str = None
    add_damage_type: bool
