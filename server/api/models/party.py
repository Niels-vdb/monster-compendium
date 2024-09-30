from typing import Annotated

from pydantic import BaseModel, Field

from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureModel
from server.api.models.user_relations import PartyBase, UserBase


class PartyModel(PartyBase):
    """
    Extension on the PartyBase entity.

    - `users`: List holding all users in a party.
    - `creatures`: List holing all creatures the party has encountered.
    """

    users: list[UserBase] | None
    creatures: list[CreatureModel] | None


class PartyPostBase(BaseModel):
    """
    Schema for creating a new party.

    - `party_name`: Name of the party to be created, must be between 1 and 100 characters.
    """

    party_name: Annotated[str, Field(min_length=1, max_length=100)]


class PartyPutBase(BaseModel):
    """
    Schema for updating an party.

    - `party_name`: Name of the party to be created, must be between 1 and 100 characters.
    """

    party_name: Annotated[str, Field(min_length=1, max_length=100)]


class PartyResponse(BaseResponse):
    """
    Party model for creating or retrieving an party.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `party`: The actual party data, represented by the `AttributeModel`.
    """

    party: PartyModel
