from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.api import get_db
from server.logger.logger import logger
from server.api.models.base_response import BaseResponse
from server.api.models.class_subclass_bases import ClassBase, SubclassBase
from server.api.models.delete_response import DeleteResponse
from server.database.models.classes import Class
from server.database.models.subclasses import Subclass


router = APIRouter(
    prefix="/api/subclasses",
    tags=["Classes"],
    responses={404: {"description": "Not found."}},
)


class SubclassModel(SubclassBase):
    """
    Extends the SubclassBase entity.

    - `id`: Unique identifier of the subclass.
    - `name`: Name of the subclass.
    - `parent_class`: The parent class of the subclass.
    """

    parent_class: ClassBase


class SubclassPostBase(BaseModel):
    """
    Schema for creating a new subclass.

    - `subclass_name`: Name of the subclass to be created, must be between 1 and 100 characters.
    - `class_id`: Id of the parent class.
    """

    subclass_name: Annotated[str, Field(min_length=1, max_length=100)]
    class_id: int


class SubclassPutBase(BaseModel):
    """
    Schema for updating a subclass.

    - `subclass_name`: New name of the subclass, must be between 1 and 100 characters.
    - `class_id`: New id of the parent class.
    """

    subclass_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    class_id: int | None = None


class SubclassResponse(BaseResponse):
    """
    Response model for creating or retrieving a subclass.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `subclass`: The actual subclass data, represented by the `SubclassModel`.
    """

    subclass: SubclassModel


@router.get("/", response_model=list[SubclassModel])
def get_subclasses(db: Session = Depends(get_db)) -> list[SubclassModel]:
    """
    Queries the subclasses database table for all rows.

    - **Returns** list[SubclassModel]: All subclass instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Armourer",
            "parent_class": {"id": 1, "name": "Artificer"},
        },
        {
            "id": 2,
            "name": "Alchemist",
            "class_id": 1,
            "parent_class": {"id": 1, "name": "Artificer"},
        },
    ]
    """
    logger.info("Querying subclasses table for all results.")
    stmt = select(Subclass)
    subclasses = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(subclasses)} from the subclasses table.")
    return subclasses


@router.get("/{subclass_id}", response_model=SubclassModel)
def get_subclass(subclass_id: int, db: Session = Depends(get_db)) -> SubclassModel:
    """
    Queries the subclasses table in the database table for a specific row with the id of subclass_id.

    - **Returns** SubclassModel: The subclass instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried subclass does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Armourer",
        "parent_class": {"id": 1, "name": "Artificer"},
    },
    ```
    """
    logger.info(f"Querying subclasses table for row with id '{subclass_id}'.")
    stmt = select(Subclass).where(Subclass.id == subclass_id)
    subclass = db.execute(stmt).scalars().first()

    if not subclass:
        logger.error(f"No subclass with the id of '{subclass_id}'.")
        raise HTTPException(status_code=404, detail="Subclass not found.")

    logger.info(f"Returning subclass info with id of {subclass_id}.")
    return subclass


@router.post("/", response_model=SubclassResponse, status_code=201)
def post_subclass(
    subclass: SubclassPostBase, db: Session = Depends(get_db)
) -> SubclassResponse:
    """
    Creates a new row in the subclasses table.

    - **Returns** SubclassResponse: A dictionary holding a message and the new subclass.

    - **HTTPException**: If an subclass with this name already exists.

    **Request Body Example**:
    ```json
    {
        "subclass_name": "example_subclass",
        "class_id": id_int,
    }
    ```
    - `subclass_name`: A string between 1 and 100 characters long (inclusive).
    - `class_id`: An id linked to a class (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New subclass 'example_subclass' has been added to the database.",
        "subclass": {
            "id": 1,
            "name": "example_subclass",
            "parent_class": {"class": example_classname, "id": example_int,}
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new subclass with name '{subclass.subclass_name}'.")

        if not db.get(Class, subclass.class_id):
            logger.error(f"No class found with the following id: {subclass.class_id}")
            raise HTTPException(
                status_code=400,
                detail="The class you are trying to add a subclass to does not exists.",
            )

        new_subclass = Subclass(name=subclass.subclass_name, class_id=subclass.class_id)
        db.add(new_subclass)

        db.commit()
        db.refresh(new_subclass)
        logger.debug(
            f"Committed subclass with name '{new_subclass.name}' to the database."
        )

        return SubclassResponse(
            message=f"New subclass '{new_subclass.name}' has been added to the database.",
            subclass=new_subclass,
        )

    except IntegrityError as e:
        logger.error(
            f"Type with the name '{subclass.subclass_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Subclass already exists.")


@router.put("/{subclass_id}", response_model=SubclassResponse)
def put_subclass(
    subclass_id: int, subclass: SubclassPutBase, db: Session = Depends(get_db)
) -> SubclassResponse:
    """
    Updates a subclass in the database by its unique id.

    - **Returns** SubclassResponse: A message and the updated subclass.

    - **HTTPException**: When the subclass id does not exist.
    - **HTTPException**: When the name of the subclass already exists in the database.

    **Request Body Example**:
    ```json
    {
        "subclass_name": "example_subclass",
        "class_id": id_int,
    }
    ```
    - `subclass_name`: A string between 1 and 100 characters long (inclusive).
    - `class_id`: An id linked to a class (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Type 'updated_subclass' has been updated.",
        "subclass": {
            "id": 1,
            "name": "example_subclass",
            "parent_class": {"class": example_classname, "id": example_int,}
        }
    }
    ```
    """
    try:
        logger.info(f"Updating subclass with id '{subclass_id}'.")

        updated_subclass = db.get(Subclass, subclass_id)
        if not updated_subclass:
            logger.error(f"Subclass with id '{subclass_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The subclass you are trying to update does not exist.",
            )

        if subclass.subclass_name:
            logger.debug(
                f"Changing subclass with id '{subclass_id}' name to '{subclass.subclass_name}'."
            )
            updated_subclass.name = subclass.subclass_name
        if subclass.class_id:
            logger.debug(
                f"Changing subclass with id '{subclass_id}' class_id to '{subclass.class_id}'."
            )
            cls = db.get(Class, subclass.class_id)
            if not cls:
                logger.error(
                    f"No class found with the following id: {subclass.class_id}"
                )
                raise HTTPException(
                    status_code=404,
                    detail="The class you are trying to link to this subclass does not exist.",
                )
            updated_subclass.class_id = cls.id

        db.commit()
        logger.info(f"Committed changes to subclass with id '{subclass_id}'.")

        return SubclassResponse(
            message=f"Subclass '{updated_subclass.name}' has been updated.",
            subclass=updated_subclass,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{subclass.subclass_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{subclass_id}", response_model=DeleteResponse)
def delete_subclass(subclass_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a subclass from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Subclass has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting subclass with the id '{subclass_id}'.")
    subclass = db.get(Subclass, subclass_id)

    if not subclass:
        logger.error(f"Type with id '{subclass_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The subclass you are trying to delete does not exist.",
        )

    db.delete(subclass)
    db.commit()

    logger.info(f"Type with id '{subclass_id}' deleted.")
    return DeleteResponse(message="Subclass has been deleted.")
