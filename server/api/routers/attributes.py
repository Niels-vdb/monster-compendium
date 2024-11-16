from typing import Sequence, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from config.logger_config import logger
from server.api.auth.security import oauth2_scheme
from server.models import Attribute
from server.api.models.delete_response import DeleteResponse
from server.api.models.attribute import (
    AttributeModel,
    AttributePostBase,
    AttributePutBase,
    AttributeResponse,
)

router = APIRouter(
    prefix="/api/attributes",
    tags=["Attributes"],
    responses={404: {"description": "Not found."}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.get("/", response_model=list[AttributeModel])
def get_attributes(db: Session = Depends(get_db)) -> Sequence[Attribute]:
    """
    Queries the attributes database table for all rows.

    - **Returns** list[AttributeModel]: All attribute instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Charmed"
        },
        {
            "id": 2,
            "name": "Frightened"
        },
    ]
    """
    logger.info("Querying attributes table for all results.")
    stmt = select(Attribute)
    attributes = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(attributes)} from the attributes table.")
    return attributes


@router.get("/{attribute_id}", response_model=AttributeModel)
def get_attribute(attribute_id: int, db: Session = Depends(get_db)) -> Row[Any] | RowMapping:
    """
    Queries the attributes table in the database table for a specific row with the id of attribute_id.

    - **Returns** AttributeModel: The attribute instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried attribute does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Charmed"
    }
    ```
    """
    logger.info(f"Querying attributes table for row with id '{attribute_id}'.")
    stmt = select(Attribute).where(Attribute.id == attribute_id)
    attribute = db.execute(stmt).scalars().first()

    if not attribute:
        logger.error(f"No attribute with the id of '{attribute_id}'.")
        raise HTTPException(status_code=404, detail="Attribute not found.")

    logger.info(f"Returning attribute info with id of {attribute_id}.")
    return attribute


@router.post("/", response_model=AttributeResponse, status_code=201)
def post_attribute(
        attribute: AttributePostBase, db: Session = Depends(get_db)
) -> AttributeResponse:
    """
    Creates a new row in the attributes table.

    - **Returns** AttributeResponse: A dictionary holding a message and the new attribute.

    - **HTTPException**: If an attribute with this name already exists.

    **Request Body Example**:
    ```json
    {
        "attribute_name": "example_attribute"
    }
    ```
    - `attribute_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New attribute 'example_attribute' has been added to the database.",
        "attribute": {
            "id": 1,
            "name": "example_attribute"
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new attribute with name '{attribute.attribute_name}'.")

        new_attribute = Attribute(name=attribute.attribute_name)
        db.add(new_attribute)

        db.commit()
        db.refresh(new_attribute)
        logger.debug(
            f"Committed attribute with name '{new_attribute.name}' to the database."
        )

        return AttributeResponse(
            message=f"New attribute '{new_attribute.name}' has been added to the database.",
            attribute=new_attribute,
        )

    except IntegrityError as e:
        logger.error(
            f"Attribute with the name '{attribute.attribute_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Attribute already exists.")


@router.put("/{attribute_id}", response_model=AttributeResponse)
def put_attribute(
        attribute_id: int, attribute: AttributePutBase, db: Session = Depends(get_db)
) -> AttributeResponse:
    """
    Updates an attribute in the database by its unique id.

    - **Returns** AttributeResponse: A message and the updated attribute.

    - **HTTPException**: When the attribute id does not exist.
    - **HTTPException**: When the name of the attribute already exists in the database.

    **Request Body Example**:
    ```json
    {
        "attribute_name": "updated_attribute"
    }
    ```
    - `attribute_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Attribute 'updated_attribute' has been updated.",
        "attribute": {
            "id": 1,
            "name": "updated_attribute"
        }
    }
    ```
    """
    try:
        logger.info(f"Updating attribute with id '{attribute_id}'.")
        updated_attribute = db.get(Attribute, attribute_id)

        if not updated_attribute:
            logger.error(f"Attribute with id '{attribute_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The attribute you are trying to update does not exist.",
            )

        logger.debug(
            f"Changing attribute with id '{attribute_id}' name to '{attribute.attribute_name}'."
        )
        updated_attribute.name = attribute.attribute_name

        db.commit()
        logger.info(f"Committed changes to attribute with id '{attribute_id}'.")

        return AttributeResponse(
            message=f"Attribute '{updated_attribute.name}' has been updated.",
            attribute=updated_attribute,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{attribute.attribute_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{attribute_id}", response_model=DeleteResponse)
def delete_attribute(
        attribute_id: int, db: Session = Depends(get_db)
) -> DeleteResponse:
    """
    Deletes an attribute from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Attribute has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting attribute with the id '{attribute_id}'.")
    attribute = db.get(Attribute, attribute_id)

    if not attribute:
        logger.error(f"Attribute with id '{attribute_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The attribute you are trying to delete does not exist.",
        )

    db.delete(attribute)
    db.commit()

    logger.info(f"Attribute with id '{attribute_id}' deleted.")
    return DeleteResponse(message="Attribute has been deleted.")
