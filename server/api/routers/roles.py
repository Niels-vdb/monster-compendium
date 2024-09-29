from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.logger.logger import logger
from server.api.models.base_response import BaseResponse
from server.api.models.user_relations import RoleBase
from server.api.models.delete_response import DeleteResponse
from server.api.routers.users import UserModel
from server.database.models.roles import Role

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found."}},
)


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


@router.get("/", response_model=list[RoleModel])
def get_roles(db: Session = Depends(get_db)) -> list[RoleModel]:
    """
    Queries the roles database table for all rows.

    - **Returns** list[RoleModel]: All role instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Admin",
            "users": [],
        },
        {
            "id": 2,
            "name": "Player",
            "users": [],
        },
    ]
    """
    logger.info("Querying roles table for all results.")
    stmt = select(Role)
    roles = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(roles)} from the roles table.")
    return roles


@router.get("/{role_id}", response_model=RoleModel)
def get_role(role_id: int, db: Session = Depends(get_db)) -> RoleModel:
    """
    Queries the roles table in the database table for a specific row with the id of role_id.

    - **Returns** RoleModel: The role instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried role does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Admin",
        "users": [],
    }
    ```
    """
    logger.info(f"Querying roles table for row with id '{role_id}'.")
    stmt = select(Role).where(Role.id == role_id)
    role = db.execute(stmt).scalars().first()

    if not role:
        logger.error(f"No role with the id of '{role_id}'.")
        raise HTTPException(status_code=404, detail="Role not found.")

    logger.info(f"Returning role info with id of {role_id}.")
    return role


@router.post("/", response_model=RoleResponse, status_code=201)
def post_role(role: RolePostBase, db: Session = Depends(get_db)) -> RoleResponse:
    """
    Creates a new row in the roles table.

    - **Returns** RoleResponse: A dictionary holding a message and the new role.

    - **HTTPException**: If a role with this name already exists.

    **Request Body Example**:
    ```json
    {
        "role_name": "example_role"
    }
    ```
    - `role_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New role 'example_role' has been added to the database.",
        "role": {
            "id": 1,
            "name": "example_role",
            "users": [],
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new role with name '{role.role_name}'.")

        new_role = Role(name=role.role_name)
        db.add(new_role)

        logger.debug(f"Committed role with name '{new_role.name}' to the database.")
        db.commit()
        db.refresh(new_role)

        return RoleResponse(
            message=f"New role '{new_role.name}' has been added to the database.",
            role=new_role,
        )

    except IntegrityError as e:
        logger.error(
            f"Role with the name '{role.role_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Role already exists.")


@router.put("/{role_id}", response_model=RoleResponse)
def put_role(
    role_id: int, role: RolePutBase, db: Session = Depends(get_db)
) -> RoleResponse:
    """
    Updates a role in the database by its unique id.

    - **Returns** RoleResponse: A message and the updated role.

    - **HTTPException**: When the role id does not exist
    - **HTTPException**: When the name of the role already exists in the database.

    **Request Body Example**:
    ```json
    {
        "role_name": "updated_role"
    }
    ```
    - `role_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Role 'updated_role' has been updated.",
        "role": {
            "id": 1,
            "name": "updated_role",
            "users": [],
        }
    }
    ```
    """
    try:
        logger.info(f"Updating role with id '{role_id}'.")
        updated_role = db.get(Role, role_id)

        if not updated_role:
            logger.error(f"Role with id '{role_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The role you are trying to update does not exist.",
            )

        logger.debug(f"Changing role with id '{role_id}' name to '{role.role_name}'.")
        updated_role.name = role.role_name

        db.commit()
        logger.info(f"Committed changes to role with id '{role_id}'.")

        return RoleResponse(
            message=f"Role '{updated_role.name}' has been updated.",
            role=updated_role,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{role.role_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{role_id}", response_model=DeleteResponse)
def delete_role(role_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a role from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Role has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting role with the id '{role_id}'.")
    role = db.get(Role, role_id)

    if not role:
        logger.error(f"Role with id '{role_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The role you are trying to delete does not exist.",
        )

    db.delete(role)
    db.commit()

    logger.info(f"Role with id '{role_id}' deleted.")
    return DeleteResponse(message=f"Role has been deleted.")
