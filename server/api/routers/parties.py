from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureModel
from server.api.models.delete_response import DeleteResponse
from server.api.models.user_relations import PartyBase, UserBase
from server.logger.logger import logger
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/parties",
    tags=["Parties"],
    responses={404: {"description": "Not found."}},
)


class PartyModel(PartyBase):
    """
    Extension on the PartyBase entity.

    - `users`: List holding all users in a party.
    - `creatures`: List holing all creatures the party has encountered.
    """

    users: list[UserBase] | None
    creatures: list[CreatureModel] | None


class PartyPostBase(BaseModel):
    """
    Schema for creating a new party.

    - `party_name`: Name of the party to be created, must be between 1 and 50 characters.
    """

    party_name: Annotated[str, Field(min_length=1, max_length=50)]


class PartyPutBase(BaseModel):
    """
    Schema for updating an party.

    - `party_name`: Name of the party to be created, must be between 1 and 50 characters.
    """

    party_name: Annotated[str, Field(min_length=1, max_length=50)]


class PartyResponse(BaseResponse):
    """
    Party model for creating or retrieving an party.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `party`: The actual party data, represented by the `AttributeModel`.
    """

    party: PartyModel


@router.get("/", response_model=list[PartyModel])
def get_parties(db: Session = Depends(get_db)) -> list[PartyModel]:
    """
    Queries the parties database table for all rows.

    - **Returns** list[PartyModel]: All party instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Murder Hobo Party"
            "users": [],
            "creatures": [],
        },
        {
            "id": 2,
            "name": "Children of Truth"
            "users": [],
            "creatures": [],
        },
    ]
    """
    logger.info("Querying parties table for all results.")
    stmt = select(Party)
    parties = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(parties)} from the parties table.")
    return parties


@router.get("/{party_id}", response_model=PartyModel)
def get_party(party_id: int, db: Session = Depends(get_db)) -> PartyModel:
    """
    Queries the parties table in the database table for a specific row with the id of party_id.

    - **Returns** PartyModel: The party instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried party does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Charmed"
        "users": [],
        "creatures": [],
    }
    ```
    """
    logger.info(f"Querying parties table for row with id '{party_id}'.")
    stmt = select(Party).where(Party.id == party_id)
    party = db.execute(stmt).scalars().first()

    if not party:
        logger.error(f"No party with the id of '{party_id}'.")
        raise HTTPException(status_code=404, detail="Party not found.")

    logger.info(f"Returning party info with id of {party_id}.")
    return party


@router.post("/", response_model=PartyResponse, status_code=201)
def post_party(party: PartyPostBase, db: Session = Depends(get_db)) -> PartyResponse:
    """
    Creates a new row in the parties table.

    - **Returns** PartyResponse: A dictionary holding a message and the new party.

    - **HTTPException**: If an party with this name already exists.

    **Request Body Example**:
    ```json
    {
        "party_name": "example_party"
    }
    ```
    - `party_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "New party 'example_party' has been added to the database.",
        "party": {
            "id": 1,
            "name": "example_party"
            "users": [],
            "creatures": [],
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new party with name '{party.party_name}'.")

        new_party = Party(name=party.party_name)
        db.add(new_party)

        db.commit()
        db.refresh(new_party)

        logger.debug(f"Committed party with name '{new_party.name}' to the database.")
        return PartyResponse(
            message=f"New party '{new_party.name}' has been added to the database.",
            party=new_party,
        )

    except IntegrityError as e:
        logger.error(
            f"Party with the name '{party.party_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Party already exists.")


@router.put("/{party_id}", response_model=PartyResponse)
def put_party(
    party_id: int, party: PartyPutBase, db: Session = Depends(get_db)
) -> PartyResponse:
    """
    Updates an party in the database by its unique id.

    - **Returns** PartyResponse: A message and the updated party.

    - **HTTPException**: When the party id does not exist or the name of the party already exists in the database.

    **Request Body Example**:
    ```json
    {
        "party_name": "updated_party"
    }
    ```
    - `party_name`: A string between 1 and 50 characters long (inclusive).

    **Response Example**:
    ```json
    {
        "message": "Party 'updated_party' has been updated.",
        "party": {
            "id": 1,
            "name": "updated_party",
            "users": [],
            "creatures": [],
        }
    }
    ```
    """
    updated_party = db.get(Party, party_id)

    if not updated_party:
        logger.error(f"Party with id '{party_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The party you are trying to update does not exist.",
        )

    logger.debug(f"Changing party with id '{party_id}' name to '{party.party_name}'.")
    updated_party.name = party.party_name

    db.commit()
    logger.info(f"Committed changes to party with id '{party_id}'.")

    return PartyResponse(
        message=f"Party '{updated_party.name}' has been updated.",
        party=updated_party,
    )


@router.delete("/{party_id}", response_model=DeleteResponse)
def delete_party(party_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes an party from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Party has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting party with the id '{party_id}'.")
    party = db.get(Party, party_id)

    if not party:
        logger.error(f"Party with id '{party_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The party you are trying to delete does not exist.",
        )

    db.delete(party)
    db.commit()

    logger.info(f"Party with id '{party_id}' deleted.")
    return DeleteResponse(message="Party has been deleted.")
