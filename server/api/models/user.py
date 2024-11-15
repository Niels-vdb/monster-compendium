from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureBase
from server.api.models.user_relations import PartyBase, RoleBase, UserBase


class UserModel(UserBase):
    """
    Extension of the UserBase entity.

    - `id`: Unique identifier of the user.
    - `name`: Name of the user.
    - `username`: Username of the user.
    - `image`: The user's image. NOT IMPLEMENTED YET!
    - `parties`: The parties the user is in.
    - `characters`: The characters the user has.
    """

    parties: list[PartyBase] | None
    roles: list[RoleBase] | None
    characters: list[CreatureBase] | None

    model_config = ConfigDict(from_attributes=True)


class UserPostBase(BaseModel):
    """
    Schema for creating a new user.

    - `name`: Name of the user to be created, must be between 1 and 50 characters.
    - `username`: Username of the user, must be between 1 and 50 characters.
    - `image`: The user's image. NOT IMPLEMENTED YET!
    - `parties`: List of parties the user is in.
    - `roles`: List of the roles of the user.
    """

    name: Annotated[str, Field(min_length=1, max_length=50)]
    username: Annotated[str, Field(min_length=1, max_length=50)]
    image: bytes | None = None
    password: str | None = None
    parties: list[int] | None = None
    roles: list[int] | None = None


class PartyPut(BaseModel):
    """Creates model for updating the parties the user is in."""

    party_id: int
    add_party: bool


class RolePut(BaseModel):
    """Creates model for updating the roles the user is."""

    role_id: int
    add_role: bool


class CharacterPut(BaseModel):
    """Creates model for updating the characters a user has."""

    character_id: int
    add_character: bool


class UserPutBase(BaseModel):
    """
    Schema for updating a user.

    - `name`: Name of the user to be created, must be between 1 and 50 characters.
    - `username`: Username of the user, must be between 1 and 50 characters.
    - `image`: The user's image. NOT IMPLEMENTED YET!
    - `parties`: List of parties the user is in.
    - `roles`: List of the roles of the user.
    - `characters`: List of all characters of the user.
    """

    name: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    username: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    image: bytes | None = None
    password: str | None = None
    parties: list[PartyPut] | None = None
    roles: list[RolePut] | None = None
    characters: list[CharacterPut] | None = None

class UserInDB(UserBase):
    """
    Model used for user authentication.
    Inherits from UserBase.

    - `hashed_password`: The hashed password string of the user.
    """
    hashed_password: str

class UserResponse(BaseResponse):
    """
    Response model for creating or retrieving a user.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `user`: The actual user data, represented by the `UserModel`.
    """

    user: UserModel
