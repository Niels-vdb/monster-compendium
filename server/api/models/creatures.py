from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.attributes import PostAttribute, PutAttribute
from server.api.models.damage_types import PostDamageType, PutDamageType
from server.api.models.race_subrace_bases import SubraceBase
from server.api.models.user_relations import RoleBase
from server.api.routers.attributes import AttributeModel
from server.api.routers.classes import ClassModel
from server.api.routers.damage_types import DamageTypeModel
from server.api.routers.sizes import SizeModel
from server.api.routers.subclasses import SubclassModel
from server.api.routers.types import TypeModel


class CreatureModel(BaseModel):
    """
    Represents a creature entity.

    - `id`: Unique identifier of the user.
    - `name`: Name of the user.
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

    id: int
    name: str
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

    classes: list[ClassModel] | None
    subclasses: list[SubclassModel] | None
    immunities: list[DamageTypeModel] | None
    resistances: list[DamageTypeModel] | None
    vulnerabilities: list[DamageTypeModel] | None
    advantages: list[AttributeModel] | None
    disadvantages: list[AttributeModel] | None

    model_config = ConfigDict(from_attributes=True)


class PCBase(CreatureModel):
    """
    Represents a player character entity. Extends the CreatureModel.
    """

    pass


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

    race_id: int = None
    subrace_id: int = None
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

    race_id: int = None
    subrace_id: int = None
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
