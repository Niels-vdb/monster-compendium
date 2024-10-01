from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """
    Represents an user entity.

    - `id`: Unique identifier of the user.
    - `name`: Name of the user.
    - `username`: Username of the user.
    - `image`: The user's image. NOT IMPLEMENTED YET!
    """

    id: int | str
    name: str
    username: str
    image: bytes | None

    model_config = ConfigDict(from_attributes=True)


class PartyBase(BaseModel):
    """
    Represents a party entity.

    - `id`: Unique identifier of the party.
    - `name`: Name of the party.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    """
    Represents a role entity.

    - `id`: Unique identifier of the role.
    - `name`: Name of the role.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
