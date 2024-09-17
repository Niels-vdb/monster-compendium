from typing import Annotated
from pydantic import BaseModel, Field


class PostEffect(BaseModel):
    effect_id: int
    condition: str


class PutEffect(BaseModel):
    effect_id: int
    condition: str = None
    add_effect: bool


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
    image: bytes = None

    race: int = None
    subrace: int = None
    size_id: int = None
    type_id: int = None

    parties: list[int] = None
    classes: list[int] = None
    subclasses: list[int] = None
    immunities: list[PostEffect] = None
    resistances: list[PostEffect] = None
    vulnerabilities: list[PostEffect] = None


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
    immunities: list[PutEffect] = None
    resistances: list[PutEffect] = None
    vulnerabilities: list[PutEffect] = None
