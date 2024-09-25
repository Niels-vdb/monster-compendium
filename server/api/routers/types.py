from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.logger.logger import logger
from server.api.models.delete_response import DeleteResponse
from server.database.models.characteristics import Type


router = APIRouter(
    prefix="/api/types",
    tags=["Types"],
    responses={404: {"description": "Not found."}},
)


class TypeModel(BaseModel):
    """
    Represents a type entity.

    - `id`: Unique identifier of the type.
    - `name`: Name of the type.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TypePostBase(BaseModel):
    """
    Schema for creating a new type.

    - `type_name`: Name of the type to be created, must be between 1 and 50 characters.
    """

    type_name: Annotated[str, Field(min_length=1, max_length=50)]


class TypePutBase(BaseModel):
    """
    Schema for updating an type.

    - `type_name`: Updated name of the type, must be between 1 and 50 characters.
    """

    type_name: Annotated[str, Field(min_length=1, max_length=50)]


class TypeResponse(BaseModel):
    """
    Response model for creating or retrieving an type.

    - `message`: A descriptive message about the action performed.
    - `type`: The actual type data, represented by the `TypeModel`.
    """

    message: str
    type: TypeModel

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[TypeModel])
def get_types(db: Session = Depends(get_db)) -> list[TypeModel]:
    """
    Queries the types database table for all rows.

    - **Returns** list[TypeModel]: All type instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Aberration"
        },
        {
            "id": 2,
            "name": "Humanoid"
        },
    ]
    """
    logger.info("Querying types table for all results.")
    stmt = select(Type)
    types = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(types)} from the types table.")
    return types


@router.get("/{type_id}", response_model=TypeModel)
def get_type(type_id: int, db: Session = Depends(get_db)) -> TypeModel:
    """
    Queries the types table in the database table for a specific row with the id of type_id.

    - **Returns** TypeModel: The type instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried type does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Aberration"
    }
    ```
    """
    logger.info(f"Querying types table for row with id '{type_id}'.")
    stmt = select(Type).where(Type.id == type_id)
    type = db.execute(stmt).scalars().first()

    if not type:
        logger.error(f"No type with the id of '{type_id}'.")
        raise HTTPException(status_code=404, detail="Type not found.")

    logger.info(f"Returning type info with id of {type_id}.")
    return type


@router.post("/", response_model=TypeResponse, status_code=201)
def post_type(type: TypePostBase, db: Session = Depends(get_db)) -> TypeResponse:
    """
    Creates a new row in the types table.

    - **Returns** TypeResponse: A dictionary holding a message and the new type.

    - **HTTPException**: If an type with this name already exists.

    **Request Body Example**:
    ```json
    {
        "type_name": "example_type",
    }
    ```
    - `type_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New type 'example_type' has been added to the database.",
        "type": {
            "id": 1,
            "name": "example_type",
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new type with name '{type.type_name}'.")

        new_type = Type(name=type.type_name)
        db.add(new_type)

        db.commit()
        db.refresh(new_type)
        logger.debug(f"Committed type with name '{new_type.name}' to the database.")

        return TypeResponse(
            message=f"New type '{new_type.name}' has been added to the database.",
            type=new_type,
        )

    except IntegrityError as e:
        logger.error(
            f"Type with the name '{type.type_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Type already exists.")


@router.put("/{type_id}", response_model=TypeResponse)
def put_type(
    type_id: int, type: TypePutBase, db: Session = Depends(get_db)
) -> TypeResponse:
    """
    Updates a type in the database by its unique id.

    - **Returns** TypeResponse: A message and the updated type.

    - **HTTPException**: When the type id does not exist.
    - **HTTPException**: When the name of the type already exists in the database.

    **Request Body Example**:
    ```json
    {
        "type_name": "updated_type"
    }
    ```
    - `type_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Type 'updated_type' has been updated.",
        "type": {
            "id": 1,
            "name": "updated_type"
        }
    }
    ```
    """
    try:
        logger.info(f"Updating type with id '{type_id}'.")

        updated_type = db.get(Type, type_id)
        if not updated_type:
            logger.error(f"Type with id '{type_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The type you are trying to update does not exist.",
            )

        logger.debug(f"Changing type with id '{type_id}' name to '{type.type_name}'.")
        updated_type.name = type.type_name

        db.commit()
        logger.info(f"Committed changes to type with id '{type_id}'.")

        return TypeResponse(
            message=f"type '{updated_type.name}' has been updated.",
            type=updated_type,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{type.type_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{type_id}", response_model=DeleteResponse)
def delete_type(type_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a type from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Type has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting type with the id '{type_id}'.")
    type = db.get(Type, type_id)

    if not type:
        logger.error(f"Type with id '{type_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The type you are trying to delete does not exist.",
        )

    db.delete(type)
    db.commit()

    logger.info(f"Type with id '{type_id}' deleted.")
    return DeleteResponse(message="Type has been deleted.")
