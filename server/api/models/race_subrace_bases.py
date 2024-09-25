from pydantic import BaseModel, ConfigDict

from server.api.routers.attributes import AttributeModel
from server.api.routers.damage_types import DamageTypeModel
from server.api.routers.sizes import SizeModel


class RaceBase(BaseModel):
    """
    Represents a race entity.

    - `id`: Unique identifier of the race.
    - `name`: Name of the race.
    - `sizes`: List of all sizes the race has.
    - `immunities`: The damage types the race is immune to.
    - `resistances`: The damage types the race is resistant to.
    - `vulnerabilities`: The damage types the race is vulnerable to.
    - `advantages`: The attributes the race has advantage on.
    - `disadvantages`:The attributes the race has disadvantage on.
    """

    id: int
    name: str
    sizes: list[SizeModel]
    resistances: list[DamageTypeModel] | None
    immunities: list[DamageTypeModel] | None
    vulnerabilities: list[DamageTypeModel] | None
    advantages: list[AttributeModel] | None
    disadvantages: list[AttributeModel] | None

    model_config = ConfigDict(from_attributes=True)


class SubraceBase(BaseModel):
    """
    Represents a subrace entity.

    - `id`: Unique identifier of the subrace.
    - `name`: Name of the subrace.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
