from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.attribute import PostAttribute, PutAttribute
from server.api.models.class_subclass_bases import ClassBase, SubclassBase
from server.api.models.damage_type import PostDamageType, PutDamageType
from server.api.models.race_subrace_bases import SubraceBase
from server.api.models.user_relations import RoleBase
from server.api.routers.attributes import AttributeModel
from server.api.routers.damage_types import DamageTypeModel
from server.api.routers.sizes import SizeModel
from server.api.routers.types import TypeModel


class CreatureBase(BaseModel):
    """
    Represents a creature entity.

    - `id`: Unique identifier of the creature.
    - `name`: Name of the creature
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CreatureModel(CreatureBase):
    """
    Extends the CreatureBase entity.
    - `id`: Unique identifier of the creature.
    - `name`: Name of the creature
    - `description`: Description of the creature.
    - `information`: Information about the creature.
    - `alive`: Boolean if creature is alive.
    - `active`: Boolean if creature is active.
    - `armour_class`: The armour class of the creature.
    - `walking_speed`: The walking speed of the creature.
    - `swimming_speed`: The swimming speed of the creature.
    - `flying_speed`: The flying speed of the creature.
    - `climbing_speed`: The climbing speed of the creature.
    - `image`: An image of the creature.
    - `race`: The race of the creature.
    - `subrace`: The subrace of the creature.
    - `size`: The size of the creature.
    - `type`: The type of creature.
    - `classes`: The classes of the creature.
    - `subclasses`: The subclasses of the creature.
    - `immunities`: The damage types the creature is immune to.
    - `resistances`: The damage types the creature is resistant to.
    - `vulnerabilities`: The damage types the creature is vulnerable to.
    - `advantages`: The attributes the creature has advantage on.
    - `disadvantages`:The attributes the creature has disadvantage on.
    """

    description: str | None
    information: str | None
    alive: bool | None
    active: bool | None
    armour_class: int | None
    walking_speed: int | None
    swimming_speed: int | None
    flying_speed: int | None
    climbing_speed: int | None
    image: bytes | None

    race: RoleBase | None
    subrace: SubraceBase | None
    size: SizeModel | None
    creature_type: TypeModel | None

    classes: list[ClassBase] | None
    subclasses: list[SubclassBase] | None
    immunities: list[DamageTypeModel] | None
    resistances: list[DamageTypeModel] | None
    vulnerabilities: list[DamageTypeModel] | None
    advantages: list[AttributeModel] | None
    disadvantages: list[AttributeModel] | None


class CreaturePostBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: str | None = None
    information: str | None = None
    alive: bool | None = None
    active: bool | None = None
    armour_class: int | None = None
    walking_speed: int | None = None
    swimming_speed: int | None = None
    flying_speed: int | None = None
    climbing_speed: int | None = None
    image: bytes | None = None

    race_id: int | None = None
    subrace_id: int | None = None
    size_id: int | None = None
    type_id: int | None = None

    parties: list[int] | None = None
    classes: list[int] | None = None
    subclasses: list[int] | None = None
    immunities: list[PostDamageType] | None = None
    resistances: list[PostDamageType] | None = None
    vulnerabilities: list[PostDamageType] | None = None
    advantages: list[PostAttribute] | None = None
    disadvantages: list[PostAttribute] | None = None


class PutClass(BaseModel):
    class_id: int
    add_class: bool


class PutSubclass(BaseModel):
    subclass_id: int
    add_subclass: bool


class PutParty(BaseModel):
    party_id: int
    add_party: bool


class CreaturePutBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    description: str | None = None
    information: str | None = None
    alive: bool | None = None
    active: bool | None = None
    armour_class: int | None = None
    walking_speed: int | None = None
    swimming_speed: int | None = None
    flying_speed: int | None = None
    climbing_speed: int | None = None
    image: bytes | None = None

    race_id: int | None = None
    subrace_id: int | None = None
    size_id: int | None = None
    type_id: int | None = None

    classes: list[PutClass] | None = None
    subclasses: list[PutSubclass] | None = None
    parties: list[PutParty] | None = None
    immunities: list[PutDamageType] | None = None
    resistances: list[PutDamageType] | None = None
    vulnerabilities: list[PutDamageType] | None = None
    advantages: list[PutAttribute] | None = None
    disadvantages: list[PutAttribute] | None = None
