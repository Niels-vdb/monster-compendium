from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.api import get_db
from config.logger_config import logger
from server.models import Class
from server.api.models.delete_response import DeleteResponse
from server.api.models.cls import ClassModel, ClassPostBase, ClassPutBase, ClassResponse


router = APIRouter(
    prefix="/api/classes",
    tags=["Classes"],
    responses={404: {"description": "Not found."}},
)


@router.get("/", response_model=list[ClassModel])
def get_classes(db: Session = Depends(get_db)) -> list[ClassModel]:
    """
    Queries the class database table for all rows.

    - **Returns** list[ClassModel]: All class instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Barbarian",
            "subclasses": [
                {
                    "id": 1,
                    "name": "Totem Warrior",
                    "class_id": 1
                },
            ],
        },
        {
            "id": 2,
            "name": "Bard",
            "subclasses": [
                {
                    "id": 4,
                    "name": "College of Creation",
                    "class_id": 2
                }
            ],
        },
    ]
    """
    logger.info("Querying classes table for all results.")
    stmt = select(Class)
    classes = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(classes)} from the classes table.")
    return classes


@router.get("/{class_id}", response_model=ClassModel)
def get_class(class_id: int, db: Session = Depends(get_db)) -> ClassModel:
    """
    Queries the classes table in the database table for a specific row with the id of class_id.

    - **Returns** ClassModel: The class instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried class does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Barbarian",
        "subclasses": [
            {
                "id": 1,
                "name": "Totem Warrior",
                "class_id": 1
            },
        ],
    }
    ```
    """
    logger.info(f"Querying class table for row with id '{class_id}'.")
    stmt = select(Class).where(Class.id == class_id)
    cls = db.execute(stmt).scalars().first()

    if not cls:
        logger.error(f"No class with the id of '{class_id}'.")
        raise HTTPException(status_code=404, detail="Class not found.")

    logger.info(f"Returning class info with id of {class_id}.")
    return cls


@router.post("/", response_model=ClassResponse, status_code=201)
def post_class(cls: ClassPostBase, db: Session = Depends(get_db)) -> ClassResponse:
    """
    Creates a new row in the classes table.

    - **Returns** ClassResponse: A dictionary holding a message and the new class.

    - **HTTPException**: If an class with this name already exists.

    **Request Body Example**:
    ```json
    {
        "class_name": "example_class"
    }
    ```
    - `class_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New class 'example_class' has been added to the database.",
        "cls": {
            "id": 1,
            "name": "example_class",
            "subclasses": [
                {
                    "id": 1,
                    "name": "example_subclass",
                    "class_id": 1,
                },
            ],
        },
    }
    ```
    """
    try:
        logger.info(f"Creating new class with name '{cls.class_name}'.")

        new_class = Class(name=cls.class_name)
        db.add(new_class)

        db.commit()
        db.refresh(new_class)
        logger.debug(f"Committed class with name '{new_class.name}' to the database.")

        return ClassResponse(
            message=f"New class '{new_class.name}' has been added to the database.",
            cls=new_class,
        )

    except IntegrityError as e:
        logger.error(
            f"Class with the name '{cls.class_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Class already exists.")


@router.put("/{class_id}", response_model=ClassResponse)
def put_class(
    class_id: int, cls: ClassPutBase, db: Session = Depends(get_db)
) -> ClassResponse:
    """
    Updates an class in the database by its unique id.

    - **Returns** ClassResponse: A message and the updated class.

    - **HTTPException**: When the class id does not exist or the name of the class already exists in the database.

    **Request Body Example**:
    ```json
    {
        "class_name": "updated_class"
    }
    ```
    - `class_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Class 'updated_class' has been updated.",
        "cls": {
            "id": 1,
            "name": "updated_class",
            "subclasses": [
                {
                    "id": 1,
                    "name": "example_subclass",
                    "class_id": 1,
                },
            ],
        }
    }
    ```
    """
    try:
        logger.info(f"Updating class with id '{class_id}'.")

        updated_class = db.get(Class, class_id)

        if not updated_class:
            logger.error(f"Class with id '{class_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The class you are trying to update does not exist.",
            )

        logger.debug(f"Changing class with id '{class_id}' name to '{cls.class_name}'.")
        updated_class.name = cls.class_name

        db.commit()
        logger.info(f"Committed changes to class with id '{class_id}'.")

        return ClassResponse(
            message=f"Class '{updated_class.name}' has been updated.",
            cls=updated_class,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{cls.class_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{class_id}", response_model=DeleteResponse)
def delete_race(class_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a class from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Class has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting class with the id '{class_id}'.")
    cls = db.get(Class, class_id)

    if not cls:
        logger.error(f"Class with id '{class_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The class you are trying to delete does not exist.",
        )

    db.delete(cls)
    db.commit()

    logger.info(f"Class with id '{class_id}' deleted.")
    return DeleteResponse(message="Class has been deleted.")
