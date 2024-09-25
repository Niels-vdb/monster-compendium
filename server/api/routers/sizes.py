from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.logger.logger import logger
from server.api.models.delete_response import DeleteResponse
from server.database.models.characteristics import Size

router = APIRouter(
    prefix="/api/sizes",
    tags=["Sizes"],
    responses={404: {"description": "Not found."}},
)


class SizeModel(BaseModel):
    """
    Represents a size entity.

    - `id`: Unique identifier of the size.
    - `name`: Name of the size.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SizePostBase(BaseModel):
    """
    Schema for creating a new size.

    - `size_name`: Name of the size to be created, must be between 1 and 50 characters.
    """

    size_name: Annotated[str, Field(min_length=1, max_length=50)]


class SizePutBase(BaseModel):
    """
    Schema for updating an size.

    - `size_name`: Updated name of the size, must be between 1 and 50 characters.
    """

    size_name: Annotated[str, Field(min_length=1, max_length=50)]


class SizeResponse(BaseModel):
    """
    Response model for creating or retrieving a size.

    - `message`: A descriptive message about the action performed.
    - `size`: The actual size data, represented by the `RoleModel`.
    """

    message: str
    size: SizeModel

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[SizeModel])
def get_sizes(db: Session = Depends(get_db)) -> list[SizeModel]:
    """
    Queries the sizes database table for all rows.

    - **Returns** list[SizeModel]: All size instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Tiny"
        },
        {
            "id": 2,
            "name": "Small"
        },
    ]
    """
    logger.info("Querying sizes table for all results.")
    stmt = select(Size)
    sizes = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(sizes)} from the sizes table.")
    return sizes


@router.get("/{size_id}", response_model=SizeModel)
def get_size(size_id: int, db: Session = Depends(get_db)) -> SizeModel:
    """
    Queries the sizes table in the database table for a specific row with the id of size_id.

    - **Returns** SizeModel: The size instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried size does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Tiny"
    }
    ```
    """
    logger.info(f"Querying sizes table for row with id '{size_id}'.")
    stmt = select(Size).where(Size.id == size_id)
    size = db.execute(stmt).scalars().first()

    if not size:
        logger.error(f"No size with the id of '{size_id}'.")
        raise HTTPException(status_code=404, detail="Size not found.")

    logger.info(f"Returning size info with id of {size_id}.")
    return size


@router.post("/", response_model=SizeResponse, status_code=201)
def post_size(size: SizePostBase, db: Session = Depends(get_db)) -> SizeResponse:
    """
    Creates a new row in the sizes table.

    - **Returns** SizeResponse: A dictionary holding a message and the new size.

    - **HTTPException**: If a size with this name already exists.

    **Request Body Example**:
    ```json
    {
        "size_name": "example_size"
    }
    ```
    - `size_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New size 'example_size' has been added to the database.",
        "size": {
            "id": 1,
            "name": "example_size"
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new size with name '{size.size_name}'.")

        new_size = Size(name=size.size_name)
        db.add(new_size)

        db.commit()
        db.refresh(new_size)
        logger.debug(f"Committed size with name '{new_size.name}' to the database.")

        return SizeResponse(
            message=f"New size '{new_size.name}' has been added to the database.",
            size=new_size,
        )

    except IntegrityError as e:
        logger.error(
            f"Size with the name '{size.size_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Size already exists.")


@router.put("/{size_id}", response_model=SizeResponse)
def put_size(
    size_id: int, size: SizePutBase, db: Session = Depends(get_db)
) -> SizeResponse:
    """
    Updates a size in the database by its unique id.

    - **Returns** SizeResponse: A message and the updated size.

    - **HTTPException**: When the size id does not exist
    - **HTTPException**: When the name of the size already exists in the database.

    **Request Body Example**:
    ```json
    {
        "size_name": "updated_size"
    }
    ```
    - `size_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Attribute 'updated_size' has been updated.",
        "size": {
            "id": 1,
            "name": "updated_size"
        }
    }
    ```
    """
    try:
        logger.info(f"Updating size with id '{size_id}'.")
        updated_size = db.get(Size, size_id)

        if not updated_size:
            logger.error(f"Size with id '{size_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The size you are trying to update does not exist.",
            )

        logger.debug(f"Changing size with id '{size_id}' name to '{size.size_name}'.")
        updated_size.name = size.size_name

        db.commit()
        logger.info(f"Committed changes to size with id '{size_id}'.")

        return SizeResponse(
            message=f"Size '{updated_size.name}' has been updated.",
            size=updated_size,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{size.size_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{size_id}", response_model=DeleteResponse)
def delete_size(size_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a size from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Size has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting size with the id '{size_id}'.")
    size = db.get(Size, size_id)

    if not size:
        logger.error(f"Attribute with id '{size_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The size you are trying to delete does not exist.",
        )

    db.delete(size)
    db.commit()

    logger.info(f"Attribute with id '{size_id}' deleted.")
    return DeleteResponse(message=f"Size has been deleted.")
