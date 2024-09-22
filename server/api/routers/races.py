from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.api.models.delete_response import DeleteResponse
from server.api.routers.attributes import AttributeModel
from server.api.routers.damage_types import DamageTypeModel
from server.api.routers.sizes import SizeModel
from server.logger.logger import logger
from server.api.models.attributes import PostAttribute, PutAttribute
from server.api.models.damage_types import PostDamageType, PutDamageType
from server.api.routers.subraces import SubraceModel
from server.database.models.characteristics import Size
from server.database.models.damage_types import DamageType
from server.database.models.attributes import Attribute
from server.database.models.races import (
    Race,
    RaceAdvantages,
    RaceDisadvantages,
    RaceImmunities,
    RaceResistances,
    RaceVulnerabilities,
)

router = APIRouter(
    prefix="/api/races",
    tags=["Races"],
    responses={404: {"description": "Not found."}},
)


class RaceModel(BaseModel):
    """
    Represents a race entity.

    - `id`: Unique identifier of the race.
    - `name`: Name of the race.
    - `sizes`: List of all sizes the race has.
    - `subraces`: List of related subrace entities.
    - `immunities`: The damage types the race is immune to.
    - `resistances`: The damage types the race is resistant to.
    - `vulnerabilities`: The damage types the race is vulnerable to.
    - `advantages`: The attributes the race has advantage on.
    - `disadvantages`:The attributes the race has disadvantage on.
    """

    id: int
    name: str
    sizes: list[SizeModel]
    subraces: list[SubraceModel]
    resistances: list[DamageTypeModel]
    immunities: list[DamageTypeModel]
    vulnerabilities: list[DamageTypeModel]
    advantages: list[AttributeModel]
    disadvantages: list[AttributeModel]

    model_config = ConfigDict(from_attributes=True)


class RacePostBase(BaseModel):
    """
    Schema for creating a new race.

    - `race_name`: Name of the race to be created, must be between 1 and 50 characters.
    - `sizes`: List of size id's this race has.
    - `immunities`: List of dicts formatted according to PostDamageType with the
                    damage types the race is immune to.
    - `resistances`: List of dicts formatted according to PostDamageType with the
                    damage types the race is resistant to.
    - `vulnerabilities`: List of dicts formatted according to PostDamageType with the
                    damage types the race is vulnerable to.
    - `advantages`: List of dicts formatted according to PostAttribute with the the
                    attributes the race has advantage on.
    - `disadvantages`:List of dicts formatted according to PostAttribute with the the
                    attributes the race has disadvantage on.
    """

    race_name: Annotated[str, Field(min_length=1, max_length=50)]
    sizes: list[int]
    resistances: list[PostDamageType] = None
    immunities: list[PostDamageType] = None
    vulnerabilities: list[PostDamageType] = None
    advantages: list[PostAttribute] = None
    disadvantages: list[PostAttribute] = None


class RacePutBase(BaseModel):
    """
    Schema for creating a new race.

    - `race_name`: New name of the race, must be between 1 and 50 characters.
    - `sizes`: New list of size id's this race has.
    - `immunities`: List of dicts formatted according to PostDamageType with the
                    damage types the race is immune to.
    - `resistances`: List of dicts formatted according to PostDamageType with the
                    damage types the race is resistant to.
    - `vulnerabilities`: List of dicts formatted according to PostDamageType with the
                    damage types the race is vulnerable to.
    - `advantages`: List of dicts formatted according to PostAttribute with the the
                    attributes the race has advantage on.
    - `disadvantages`:List of dicts formatted according to PostAttribute with the the
                    attributes the race has disadvantage on.
    """

    race_name: str = None
    sizes: list[int] = None
    resistances: list[PutDamageType] = None
    immunities: list[PutDamageType] = None
    vulnerabilities: list[PutDamageType] = None
    advantages: list[PutAttribute] = None
    disadvantages: list[PutAttribute] = None


class RaceResponse(BaseModel):
    """
    Response model for creating or retrieving an race.

    - `message`: A descriptive message about the action performed.
    - `race`: The actual race data, represented by the `AttributeModel`.
    """

    message: str
    race: RaceModel

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[RaceModel])
def get_races(db: Session = Depends(get_db)) -> list[RaceModel]:
    """
    Queries the attributes database table for all rows.

    - **Returns** list[RaceModel]: All race instances in the database.

    **Response Example**:
    ```json
        [
            {
                "id": 1,
                "name": "Dwarf",
                "sizes": [
                    {
                        "id": 1,
                        "name": "Small"
                    },
                    {
                        "id": 2,
                        "name": "Medium"
                    },
                ],
                "subraces": [
                    {
                        "id": 1,
                        "name": "Duergar",
                        "race_id": 1
                    },
                ],
                "resistances": [
                    {
                        "id": 1,
                        "name": "Poison"
                    },
                ],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [
                    {
                        "id": 1,
                        "name": "Poisoned"
                    },
                ],
                "disadvantages": [],
            },
            {
                "id": 1,
                "name": "Gnome",
                "sizes": [
                    {
                        "id": 1,
                        "name": "Small"
                    },
                ],
                "subraces": [],
                "resistances": [],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [],
                "disadvantages": [],
            },
        ]
    """
    logger.info("Querying races table for all results.")
    stmt = select(Race)
    races = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(races)} from the races table.")
    return races


@router.get("/{race_id}", response_model=RaceModel)
def get_race(race_id: int, db: Session = Depends(get_db)) -> RaceModel:
    """
    Queries the races table in the database table for a specific row with the id of race_id.

    - **Returns** AttributeModel: The race instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried race does not exist.

    **Response Example**:
    ```json
        {
            "id": 1,
            "name": "Dwarf",
            "sizes": [
                {
                    "id": 1,
                    "name": "Small"
                },
                {
                    "id": 2,
                    "name": "Medium"
                },
            ],
            "subraces": [
                {
                    "id": 1,
                    "name": "Duergar",
                    "race_id": 1
                },
            ],
            "resistances": [
                {
                    "id": 1,
                    "name": "Poison"
                },
            ],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [
                {
                    "id": 1,
                    "name": "Poisoned"
                },
            ],
            "disadvantages": [],
        },
    ```
    """
    logger.info(f"Querying races table for row with id '{race_id}'.")
    stmt = select(Race).where(Race.id == race_id)
    race = db.execute(stmt).scalars().first()

    if not race:
        logger.error(f"No race with the id of '{race_id}'.")
        raise HTTPException(status_code=404, detail="Race not found.")

    logger.info(f"Returning race info with id of {race_id}.")
    return race


@router.post("/", response_model=RaceResponse, status_code=201)
def post_race(race: RacePostBase, db: Session = Depends(get_db)) -> RaceResponse:
    """
    Creates a new row in the races table.

    - **Returns** RaceResponse: A dictionary holding a message and the new race.

    - **HTTPException**: If a race with this name already exists.
    - **HTTPException**: If a size does not exist.
    - **HTTPException**: If a damage type or attribute does not exist.

    **Request Body Example**:
    ```json
    {
        "race_name": "example_race",
        "sizes": [1, 2],
        "resistances": [
            {
                damage_type_id: 1,
                condition: "condition of the resistance",
            },
        ],
        "immunities": [
            {
                damage_type_id: 1,
                condition: "condition of the immunity",
            },
        ],
        "vulnerabilities": [
            {
                damage_type_id: 1,
                condition: "condition of the vulnerability",
            },
        ],
        "advantages": [
            {
                attribute_id: 1,
                condition: "condition of the advantage",
            },
        ],
        "disadvantages": [
            {
                attribute_id: 1,
                condition: "condition of the disadvantage",
            },
        ],
    }
    ```
    - `race_name`: A string between 1 and 50 characters long (inclusive).
    - `immunities`: Optional.
    - `resistances`: Optional.
    - `vulnerabilities`: Optional.
    - `advantages`: Optional.
    - `disadvantages`: Optional.

    **Response Example**:
    ```json
    {
        "message": "New race 'example_race' has been added to the database.",
        "race": {
        {
            "id": 1,
            "name": "Dwarf",
            "sizes": [
                {
                    "id": 1,
                    "name": "Small"
                },
                {
                    "id": 2,
                    "name": "Medium"
                },
            ],
            "subraces": [
                {
                    "id": 1,
                    "name": "Duergar",
                    "race_id": 1
                },
            ],
            "resistances": [
                {
                    "id": 1,
                    "name": "Poison"
                },
            ],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [
                {
                    "id": 1,
                    "name": "Poisoned"
                },
            ],
            "disadvantages": [],
        },
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new race with name '{race.race_name}'.")

        logger.debug("Fetching sizes for race and checking if all are correct.")
        stmt = select(Size).where(Size.id.in_(race.sizes))
        sizes = db.execute(stmt).scalars().all()

        missing_sizes = set(race.sizes) - {size.id for size in sizes}
        if missing_sizes:
            logger.error(f"No size found for the following ids: {missing_sizes}")
            raise HTTPException(status_code=404, detail="One or more sizes not found.")

        logger.debug("Successfully fetched all sizes.")

        new_race = Race(name=race.race_name, sizes=sizes)
        db.add(new_race)
        db.commit()
        logger.debug(f"Committed race with name '{new_race.name}' to the database.")
        db.refresh(new_race)
    except IntegrityError as e:
        logger.error(
            f"Attribute with the name '{race.race_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Race already exists.")
    try:
        if race.resistances:
            logger.debug(f"Adding resistances to race")
            for resistance in race.resistances:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == resistance.damage_type_id)
                    .first()
                )
                if not damage_type:
                    logger.error(
                        f"No damage type with id '{resistance.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{resistance.damage_type_id}' does not exist.",
                    )
                race_resistance = RaceResistances(
                    race_id=new_race.id, damage_type_id=damage_type.id
                )
                db.add(race_resistance)
            logger.debug(f"Added resistances to '{new_race.name}'.")
        if race.immunities:
            logger.debug(f"Adding immunities to race")
            for immunity in race.immunities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == immunity.damage_type_id)
                    .first()
                )
                if not damage_type:
                    logger.error(
                        f"No damage type with id '{immunity.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{immunity.damage_type_id}' does not exist.",
                    )
                race_immunity = RaceImmunities(
                    race_id=new_race.id, damage_type_id=damage_type.id
                )
                db.add(race_immunity)
            logger.debug(f"Added immunities to '{new_race.name}'.")
        if race.vulnerabilities:
            logger.info(f"Adding vulnerabilities to race")
            for vulnerability in race.vulnerabilities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == vulnerability.damage_type_id)
                    .first()
                )
                if not damage_type:
                    logger.error(
                        f"No damage type with id '{vulnerability.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{vulnerability.damage_type_id}' does not exist.",
                    )
                race_vulnerability = RaceVulnerabilities(
                    race_id=new_race.id, damage_type_id=damage_type.id
                )
                db.add(race_vulnerability)
            logger.debug(f"Added vulnerabilities to '{new_race.name}'.")
        if race.advantages:
            logger.info(f"Adding advantages to race")
            for advantage in race.advantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == advantage.attribute_id)
                    .first()
                )
                if not attribute:
                    logger.error(
                        f"No attribute with id '{advantage.attribute_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Attribute with id '{advantage.attribute_id}' does not exist.",
                    )
                race_advantage = RaceAdvantages(
                    race_id=new_race.id, attribute_id=attribute.id
                )
                db.add(race_advantage)
            logger.debug(f"Added advantages to '{new_race.name}'.")
        if race.disadvantages:
            logger.info(f"Adding disadvantages to race")
            for disadvantage in race.disadvantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == disadvantage.attribute_id)
                    .first()
                )
                if not attribute:
                    logger.error(
                        f"No attribute with id '{disadvantage.attribute_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Attribute with id '{disadvantage.attribute_id}' does not exist.",
                    )
                race_disadvantage = RaceDisadvantages(
                    race_id=new_race.id, attribute_id=attribute.id
                )
                db.add(race_disadvantage)
            logger.debug(f"Added advantages to '{new_race.name}'.")
        db.commit()
        logger.debug(
            f"Committed '{new_race.name}' to the database with optional attributes and damage types."
        )
        return RaceResponse(
            message=f"New race '{new_race.name}' has been added to the database.",
            race=new_race,
        )
    except IntegrityError as e:
        logger.error(
            f"Attribute with the name '{race.race_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"The combination of race and damage type or attribute already exists.",
        )


@router.put("/{race_id}", response_model=RaceResponse)
def put_race(
    race_id: int, race: RacePutBase, db: Session = Depends(get_db)
) -> RaceResponse:
    """
    Updates a class in the database by its unique id.

    - **Returns** RaceResponse: A dictionary holding a message and the updated race.

    - **HTTPException**: If a race with this name already exists.
    - **HTTPException**: If a size does not exist.
    - **HTTPException**: If a damage type or attribute does not exist.

    **Request Body Example**:
    ```json
    {
        "race_name": "example_race",
        "sizes": [1, 2],
        "resistances": [
            {
                damage_type_id: 1,
                condition: "condition of the resistance",
                add_damage_type: boolean,
            },
        ],
        "immunities": [
            {
                damage_type_id: 1,
                condition: "condition of the immunity",
                add_damage_type: boolean,
            },
        ],
        "vulnerabilities": [
            {
                damage_type_id: 1,
                condition: "condition of the vulnerability",
                add_damage_type: boolean,
            },
        ],
        "advantages": [
            {
                attribute_id: 1,
                condition: "condition of the advantage",
                add_damage_type: boolean,
            },
        ],
        "disadvantages": [
            {
                attribute_id: 1,
                condition: "condition of the disadvantage",
                add_damage_type: boolean,
            },
        ],
    }
    ```
    - `race_name`: A string between 1 and 50 characters long (inclusive).
    - `immunities`: Optional.
    - `resistances`: Optional.
    - `vulnerabilities`: Optional.
    - `advantages`: Optional.
    - `disadvantages`: Optional.

    **Response Example**:
    ```json
    {
        "message": "New race 'example_race' has been added to the database.",
        {
            "id": 1,
            "name": "Dwarf",
            "sizes": [
                {
                    "id": 1,
                    "name": "Small"
                },
                {
                    "id": 2,
                    "name": "Medium"
                },
            ],
            "subraces": [
                {
                    "id": 1,
                    "name": "Duergar",
                    "race_id": 1
                },
            ],
            "resistances": [
                {
                    "id": 1,
                    "name": "Poison"
                },
            ],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [
                {
                    "id": 1,
                    "name": "Poisoned"
                },
            ],
            "disadvantages": [],
        },
    }
    ```
    """
    try:
        logger.info(f"Updating race with id '{race_id}'.")
        updated_race = db.get(Race, race_id)
        if not updated_race:
            logger.error(f"Attribute with id '{race_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The race you are trying to update does not exist.",
            )
        if race.race_name:
            logger.debug(
                f"Changing race with id '{race_id}' name to '{race.race_name}'."
            )
            updated_race.name = race.race_name
        if race.sizes:
            logger.debug("Fetching sizes for race and checking if all are correct.")

            stmt = select(Size).where(Size.id.in_(race.sizes))
            sizes = db.execute(stmt).scalars().all()

            missing_sizes = set(race.sizes) - {size.id for size in sizes}
            if missing_sizes:
                logger.error(f"No size found for the following ids: {missing_sizes}")
                raise HTTPException(
                    status_code=404, detail="One or more sizes not found."
                )

            logger.debug("Successfully fetched all sizes.")
            updated_race.sizes = sizes
        if race.immunities:
            logger.debug(f"Changing immunities for race '{updated_race.name}'.")
            for immunity in race.immunities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == immunity.damage_type_id)
                    .first()
                )
                if not damage_type:
                    logger.error(
                        f"No damage type with id '{immunity.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif immunity.add_damage_type:
                    logger.debug(
                        f"Adding immunity with name '{damage_type.name}' to race."
                    )
                    new_immunity = RaceImmunities(
                        race_id=race_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    logger.debug(
                        f"Removing immunity with name '{damage_type.name}' from race."
                    )
                    old_immunity = (
                        db.query(RaceImmunities)
                        .filter(
                            and_(
                                RaceImmunities.race_id == race_id,
                                RaceImmunities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
                logger.debug(f"Changed immunities from race '{updated_race.name}'.")
        if race.resistances:
            logger.debug(f"Changing resistances for race '{updated_race.name}'.")
            for resistance in race.resistances:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == resistance.damage_type_id)
                    .first()
                )
                if not damage_type:
                    logger.error(
                        f"No damage type with id '{resistance.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif resistance.add_damage_type:
                    logger.debug(
                        f"Adding resistance with name '{damage_type.name}' to race."
                    )
                    new_resistance = RaceResistances(
                        race_id=race_id,
                        damage_type_id=damage_type.id,
                        condition=resistance.condition,
                    )
                    db.add(new_resistance)
                else:
                    logger.debug(
                        f"Removing immunity with name '{damage_type.name}' from race."
                    )
                    old_resistance = (
                        db.query(RaceResistances)
                        .filter(
                            and_(
                                RaceResistances.race_id == race_id,
                                RaceResistances.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
                logger.debug(f"Changed resistances from race '{updated_race.name}'.")
        if race.vulnerabilities:
            logger.debug(f"Changing vulnerabilities for race '{updated_race.name}'.")
            for vulnerability in race.vulnerabilities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == vulnerability.damage_type_id)
                    .first()
                )
                if not damage_type:
                    logger.error(
                        f"No damage type with id '{vulnerability.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif vulnerability.add_damage_type:
                    logger.debug(
                        f"Adding vulnerability with name '{damage_type.name}' to race."
                    )
                    new_vulnerability = RaceVulnerabilities(
                        race_id=race_id,
                        damage_type_id=damage_type.id,
                        condition=vulnerability.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    logger.debug(
                        f"Removing vulnerability with name '{damage_type.name}' from race."
                    )
                    old_vulnerability = (
                        db.query(RaceVulnerabilities)
                        .filter(
                            and_(
                                RaceVulnerabilities.race_id == race_id,
                                RaceVulnerabilities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
                logger.debug(
                    f"Changed vulnerabilities from race '{updated_race.name}'."
                )
        if race.advantages:
            logger.debug(f"Changing advantages for race '{updated_race.name}'.")
            for advantage in race.advantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == advantage.attribute_id)
                    .first()
                )
                if not attribute:
                    logger.error(
                        f"No attribute with id '{advantage.attribute_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail="Attribute with this id does not exist.",
                    )
                elif advantage.add_attribute:
                    logger.debug(
                        f"Adding advantage with name '{attribute.name}' to race."
                    )
                    new_advantage = RaceAdvantages(
                        race_id=race_id,
                        attribute_id=attribute.id,
                        condition=advantage.condition,
                    )
                    db.add(new_advantage)
                else:
                    logger.debug(
                        f"Removing advantage with name '{attribute.name}' from race."
                    )
                    old_advantage = (
                        db.query(RaceAdvantages)
                        .filter(
                            and_(
                                RaceAdvantages.race_id == race_id,
                                RaceAdvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_advantage)
                logger.debug(f"Changed advantages from race '{updated_race.name}'.")
        if race.disadvantages:
            logger.debug(f"Changing disadvantages for race '{updated_race.name}'.")
            for disadvantage in race.disadvantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == disadvantage.attribute_id)
                    .first()
                )
                if not attribute:
                    logger.error(
                        f"No attribute with id '{disadvantage.attribute_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail="Attribute with this id does not exist.",
                    )
                elif disadvantage.add_attribute:
                    logger.debug(
                        f"Adding disadvantage with name '{attribute.name}' to race."
                    )
                    new_disadvantage = RaceDisadvantages(
                        race_id=race_id,
                        attribute_id=attribute.id,
                        condition=disadvantage.condition,
                    )
                    db.add(new_disadvantage)
                else:
                    logger.debug(
                        f"Removing disadvantage with name '{attribute.name}' from race."
                    )
                    old_disadvantage = (
                        db.query(RaceDisadvantages)
                        .filter(
                            and_(
                                RaceDisadvantages.race_id == race_id,
                                RaceDisadvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_disadvantage)
                logger.debug(f"Changed disadvantages from race '{updated_race.name}'.")
        db.commit()
        logger.info(f"Updated information of race with id '{race_id}'.")
        return RaceResponse(
            message=f"Race '{updated_race.name}' has been updated.",
            race=updated_race,
        )
    except IntegrityError as e:
        logger.error(
            f"The name that is trying to be used already exists in the table. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{race_id}", response_model=DeleteResponse)
def delete_race(race_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a race from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Attribute has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting race with the id '{race_id}'.")
    race = db.get(Race, race_id)

    if not race:
        logger.error(f"Attribute with id '{race_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The race you are trying to delete does not exist.",
        )

    db.delete(race)
    db.commit()
    logger.info(f"Attribute with id '{race_id}' deleted.")

    return DeleteResponse(message="Race has been deleted.")
