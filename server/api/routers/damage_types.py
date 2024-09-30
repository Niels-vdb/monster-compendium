from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.logger.logger import logger
from server.database.models.damage_types import DamageType
from server.api.models.delete_response import DeleteResponse
from server.api.models.damage_type import (
    DamageTypeModel,
    DamageTypePostBase,
    DamageTypePutBase,
    DamageTypeResponse,
)

router = APIRouter(
    prefix="/api/damage_types",
    tags=["Damage Types"],
    responses={404: {"description": "Not found."}},
)


@router.get("/", response_model=list[DamageTypeModel])
def get_damage_types(db: Session = Depends(get_db)) -> list[DamageTypeModel]:
    """
    Queries the damage_types database table for all rows.

    - **Returns** list[DamageTypeModel]: All damage type instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Fire"
        },
        {
            "id": 2,
            "name": "Slashing"
        },
    ]
    """
    logger.info("Querying damage types table for all results.")
    stmt = select(DamageType)
    damage_types = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(damage_types)} from the damage types table.")
    return damage_types


@router.get("/{damage_type_id}", response_model=DamageTypeModel)
def get_damage_type(
    damage_type_id: int, db: Session = Depends(get_db)
) -> DamageTypeModel:
    """
    Queries the damage types table in the database table for a specific row with the id of damage_type_id.

    - **Returns** DamageTypeModel: The damage type instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried damage type does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Fire"
    }
    ```
    """
    logger.info(f"Querying damage types table for row with id '{damage_type_id}'.")
    stmt = select(DamageType).where(DamageType.id == damage_type_id)
    damage_type = db.execute(stmt).scalars().first()

    if not damage_type:
        logger.error(f"No damage type with the id of '{damage_type_id}'.")
        raise HTTPException(status_code=404, detail="Damage type not found.")

    logger.info(f"Returning damage type info with id of {damage_type_id}.")
    return damage_type


@router.post("/", response_model=DamageTypeResponse, status_code=201)
def post_damage_type(
    damage_type: DamageTypePostBase, db: Session = Depends(get_db)
) -> DamageTypeResponse:
    """
    Creates a new row in the damage_types table.

    - **Returns** DamageTypeResponse: A dictionary holding a message and the new damage type.

    - **HTTPException**: If an damage type with this name already exists.

    **Request Body Example**:
    ```json
    {
        "damage_type_name": "example_damage_type"
    }
    ```
    - `damage_type_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New damage type 'example_damage_type' has been added to the database.",
        "damage_type": {
            "id": 1,
            "name": "example_damage_type"
        }
    }
    ```
    """
    try:
        logger.info(
            f"Creating new damage type with name '{damage_type.damage_type_name}'."
        )

        new_damage_type = DamageType(name=damage_type.damage_type_name)
        db.add(new_damage_type)

        db.commit()
        db.refresh(new_damage_type)
        logger.debug(
            f"Committed damage type with name '{new_damage_type.name}' to the database."
        )

        return DamageTypeResponse(
            message=f"New damage type '{new_damage_type.name}' has been added to the database.",
            damage_type=new_damage_type,
        )

    except IntegrityError as e:
        logger.error(
            f"Damage type with the name '{damage_type.damage_type_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Damage type already exists.")


@router.put("/{damage_type_id}", response_model=DamageTypeResponse)
def put_damage_type(
    damage_type_id: int, damage_type: DamageTypePutBase, db: Session = Depends(get_db)
) -> DamageTypeResponse:
    """
    Updates a damage type in the database by its unique id.

    - **Returns** DamageTypeResponse: A message and the updated damage type.

    - **HTTPException**: When the damage type id does not exist or the name of the damage type already exists in the database.

    **Request Body Example**:
    ```json
    {
        "damage_type_name": "updated_damage_type"
    }
    ```
    - `damage_type_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Damage type 'updated_damage_type' has been updated.",
        "damage_type": {
            "id": 1,
            "name": "updated_damage_type"
        }
    }
    ```
    """
    try:
        logger.info(f"Updating damage type with id '{damage_type_id}'.")
        updated_damage_type = db.get(DamageType, damage_type_id)

        if not updated_damage_type:
            logger.error(f"Damage type with id '{damage_type_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The damage type you are trying to update does not exist.",
            )

        logger.debug(
            f"Changing damage type with id '{damage_type_id}' name to '{damage_type.damage_type_name}'."
        )
        updated_damage_type.name = damage_type.damage_type_name

        db.commit()
        logger.info(f"Committed changes to damage type with id '{damage_type_id}'.")

        return DamageTypeResponse(
            message=f"Damage type '{updated_damage_type.name}' has been updated.",
            damage_type=updated_damage_type,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{damage_type.damage_type_name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{damage_type_id}", response_model=DeleteResponse)
def delete_damage_type(
    damage_type_id: int, db: Session = Depends(get_db)
) -> DeleteResponse:
    """
    Deletes an damage type from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Damage type has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting damage type with the id '{damage_type_id}'.")
    damage_type = db.get(DamageType, damage_type_id)

    if not damage_type:
        logger.error(f"Damage type with id '{damage_type_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The damage type you are trying to delete does not exist.",
        )

    db.delete(damage_type)
    db.commit()

    logger.info(f"Damage type with id '{damage_type_id}' deleted.")
    return DeleteResponse(message="Damage type has been deleted.")
