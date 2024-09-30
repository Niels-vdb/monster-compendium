from pydantic import BaseModel, ConfigDict

from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureModel, CreaturePostBase
from server.api.models.user_relations import UserBase


class PCModel(CreatureModel):
    user: UserBase


class PCPostBase(CreaturePostBase):
    """
    Extension of the CreaturePostBase with extra user_id for
    pc to user connection.
    """

    user_id: int


class UserPublic(BaseModel):
    """Only allows specific data from the User table to show up."""

    name: str
    username: str
    image: bytes | None = None

    model_config = ConfigDict(from_attributes=True)


class PCResponse(BaseResponse):
    """
    Response model for creating or retrieving a player character.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `pc`: The actual pc data, represented by the `PCModel`.
    """

    pc: PCModel
