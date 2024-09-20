from typing import Annotated
from pydantic import BaseModel, Field

from server.api.models.attributes import PostAttribute, PutAttribute
from server.api.models.damage_types import PostDamageType, PutDamageType


class CreaturePostBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    armour_class: int = None
    walking_speed: int = None
    swimming_speed: int = None
    flying_speed: int = None
    climbing_speed: int = None
    image: bytes = None

    race: int = None
    subrace: int = None
    size_id: int = None
    type_id: int = None

    parties: list[int] = None
    classes: list[int] = None
    subclasses: list[int] = None
    immunities: list[PostDamageType] = None
    resistances: list[PostDamageType] = None
    vulnerabilities: list[PostDamageType] = None
    advantages: list[PostAttribute] = None
    disadvantages: list[PostAttribute] = None


class CreaturePutBase(BaseModel):
    name: str = None
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    armour_class: int = None
    walking_speed: int = None
    swimming_speed: int = None
    flying_speed: int = None
    climbing_speed: int = None
    image: bytes = None

    race: int = None
    subrace: int = None
    size_id: int = None
    type_id: int = None

    classes: list[int] = None
    add_class: bool = None
    subclasses: list[int] = None
    add_subclass: bool = None
    parties: list[int] = None
    add_parties: bool = None
    immunities: list[PutDamageType] = None
    resistances: list[PutDamageType] = None
    vulnerabilities: list[PutDamageType] = None
    advantages: list[PutAttribute] = None
    disadvantages: list[PutAttribute] = None
