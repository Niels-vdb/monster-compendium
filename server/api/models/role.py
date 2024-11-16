from typing import Annotated
from pydantic import BaseModel, Field

from server.api.models.base_response import BaseResponse
from server.api.models.user_relations import RoleBase
from server.api.routers.users import UserModel


class RoleModel(RoleBase):
    """
    Extension of the RoleBase entity.

    - `users`: List of all users that have this role.
    """

    users: list[UserModel] | None


class RolePostBase(BaseModel):
    """
    Schema for creating a new role.

    - `role_name`: Name of the role to be created, must be between 1 and 50 characters.
    """

    role_name: Annotated[str, Field(min_length=1, max_length=50)]


class RolePutBase(BaseModel):
    """
    Schema for updating an role.

    - `role_name`: Updated name of the role, must be between 1 and 50 characters.
    """

    role_name: Annotated[str, Field(min_length=1, max_length=50)]


class RoleResponse(BaseResponse):
    """
    Response model for creating or retrieving a role.

    - `message`: A descriptive message about the action performed.
    - `role`: The actual role data, represented by the `RoleModel`.
    """

    role: RoleModel
