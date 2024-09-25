import re
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
from server.logger.logger import logger
from server.api.models.attributes import PostAttribute, PutAttribute
from server.api.models.damage_types import PostDamageType, PutDamageType
from server.api.models.race_subrace_bases import RaceBase, SubraceBase
from server.database.models.attributes import Attribute
from server.database.models.damage_types import DamageType
from server.database.models.races import Race
from server.database.models.subraces import (
    Subrace,
    SubraceAdvantages,
    SubraceDisadvantages,
    SubraceImmunities,
    SubraceResistances,
    SubraceVulnerabilities,
)

router = APIRouter(
    prefix="/api/subraces",
    tags=["Races"],
    responses={404: {"description": "Not found."}},
)


class SubraceModel(SubraceBase):
    """
    Extends the SubraceBase entity.

    - `id`: Unique identifier of the subrace.
    - `name`: Name of the subrace.
    - `race`: The parent race of the subrace.
    """

    race: RaceBase
    resistances: list[DamageTypeModel] | None
    immunities: list[DamageTypeModel] | None
    vulnerabilities: list[DamageTypeModel] | None
    advantages: list[AttributeModel] | None
    disadvantages: list[AttributeModel] | None


class SubracePostBase(BaseModel):
    """
    Schema for creating a new subrace.

    - `subrace_name`: Name of the subrace to be created, must be between 1 and 50 characters.
    - `race_id`: The id of the parent race.
    - `immunities`: List of dicts formatted according to PostDamageType with the
                    damage types the subrace is immune to.
    - `resistances`: List of dicts formatted according to PostDamageType with the
                    damage types the subrace is resistant to.
    - `vulnerabilities`: List of dicts formatted according to PostDamageType with the
                    damage types the subrace is vulnerable to.
    - `advantages`: List of dicts formatted according to PostAttribute with the the
                    attributes the subrace has advantage on.
    - `disadvantages`:List of dicts formatted according to PostAttribute with the the
                    attributes the subrace has disadvantage on.
    """

    subrace_name: Annotated[str, Field(min_length=1, max_length=50)]
    race_id: int
    resistances: list[PostDamageType] | None = None
    immunities: list[PostDamageType] | None = None
    vulnerabilities: list[PostDamageType] | None = None
    advantages: list[PostAttribute] | None = None
    disadvantages: list[PostAttribute] | None = None


class SubracePutBase(BaseModel):
    """
    Schema for updating an existing subrace.

    - `subrace_name`: New name of the subrace, must be between 1 and 50 characters.
    - `race_id`: New parent race id.
    - `immunities`: List of dicts formatted according to PostDamageType with the
                    damage types the subrace is immune to.
    - `resistances`: List of dicts formatted according to PostDamageType with the
                    damage types the subrace is resistant to.
    - `vulnerabilities`: List of dicts formatted according to PostDamageType with the
                    damage types the subrace is vulnerable to.
    - `advantages`: List of dicts formatted according to PostAttribute with the the
                    attributes the subrace has advantage on.
    - `disadvantages`:List of dicts formatted according to PostAttribute with the the
                    attributes the subrace has disadvantage on.
    """

    subrace_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    race_id: int | None = None
    resistances: list[PutDamageType] | None = None
    immunities: list[PutDamageType] | None = None
    vulnerabilities: list[PutDamageType] | None = None
    advantages: list[PutAttribute] | None = None
    disadvantages: list[PutAttribute] | None = None


class SubraceResponse(BaseModel):
    """
    Response model for creating or retrieving a subrace.

    - `message`: A descriptive message about the action performed.
    - `subrace`: The actual subrace data, represented by the `SubraceModel`.
    """

    message: str
    subrace: SubraceModel

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[SubraceModel])
def get_subraces(db: Session = Depends(get_db)) -> list[SubraceModel]:
    """
    Queries the subraces database table for all rows.

    - **Returns** list[SubraceModel]: All subrace instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Hill",
            "race": {
                "id": 1,
                "name": "Dwarf,
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
                "resistances": [
                    {
                        "id": 1,
                        "name": "Poison"
                    },
                ],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [],
                "disadvantages": [],
            },
            "resistances": [],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
        },
        {
            "id": 2,
            "name": "Duergar",
            "race": {
                "id": 1,
                "name": "Dwarf,
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
                "resistances": [
                    {
                        "id": 1,
                        "name": "Poison"
                    },
                ],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [],
                "disadvantages": [],
            },
            "resistances": [],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
        },
    ]
    """
    logger.info("Querying subraces table for all results.")
    stmt = select(Subrace)
    subraces = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(subraces)} from the races table.")
    return subraces


@router.get("/{subrace_id}", response_model=SubraceModel)
def get_subrace(subrace_id: int, db: Session = Depends(get_db)) -> SubraceModel:
    """
    Queries the subraces database table for a specific row with the id of subrace_id.

    - **Returns** SubraceModel: The subrace instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried subrace does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "Hill",
        "race": {
            "id": 1,
            "name": "Dwarf,
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
            "resistances": [
                {
                    "id": 1,
                    "name": "Poison"
                },
            ],
            "immunities": [],
            "vulnerabilities": [],
            "advantages": [],
            "disadvantages": [],
        },
        "resistances": [],
        "immunities": [],
        "vulnerabilities": [],
        "advantages": [],
        "disadvantages": [],
    },
    """
    logger.info(f"Querying subraces table for row with id '{subrace_id}'.")
    stmt = select(Subrace).where(Subrace.id == subrace_id)
    subrace = db.execute(stmt).scalars().first()

    if not subrace:
        logger.error(f"No subrace with the id of '{subrace_id}'.")
        raise HTTPException(status_code=404, detail="Subrace not found.")

    logger.info(f"Returning subrace info with id of {subrace_id}.")
    return subrace


@router.post("/", response_model=SubraceResponse, status_code=201)
def post_subrace(
    subrace: SubracePostBase, db: Session = Depends(get_db)
) -> SubraceResponse:
    """
    Creates a new row in the subraces table.

    - **Returns** RaceResponse: A dictionary holding a message and the new subrace.

    - **HTTPException**: If a subrace with this name already exists.
    - **HTTPException**: If the race does not exist.
    - **HTTPException**: If a damage type or attribute does not exist.

    **Request Body Example**:
    ```json
    {
        "subrace_name": "example_subrace",
        "race_id": example_int,
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
    - `subrace_name`: A string between 1 and 50 characters long (inclusive).
    - `race_id`: The id of the parent race (inclusive).
    - `immunities`: Optional.
    - `resistances`: Optional.
    - `vulnerabilities`: Optional.
    - `advantages`: Optional.
    - `disadvantages`: Optional.

    **Response Example**:
    ```json
    {
        "message": "New subrace 'example_subrace' has been added to the database.",
        "subrace": {
        {
            "id": 1,
            "name": "example_subrace",
            "resistances": [{"id": 1, "name": "example_damage_type_type"}],
            "immunities": [{"id": 1, "name": "example_damage_type_type"}],
            "vulnerabilities": [{"id": 1, "name": "example_damage_type_type"}],
            "advantages": [{"id": 1, "name": "example_attribute_type"}],
            "disadvantages": [{"id": 1, "name": "example_attribute_type"}],
            "race": {
                "id": 1,
                "name": "Dwarf",
                "sizes": [{"id": 1, "name": "Tiny"}],
                "resistances": [{"id": 1, "name": "example_damage_type"}],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [{"id": 1, "name": "example_attribute_type"}],
                "disadvantages": [],
            },
        },
    }
    ```
    """
    try:
        logger.info(f"Creating new subrace with name '{subrace.subrace_name}'.")

        logger.debug("Fetching race for subrace and checking if all are correct.")
        race = db.get(Race, subrace.race_id)

        if not race:
            raise HTTPException(
                status_code=404,
                detail="The race you are trying to bind to this subrace does not exist.",
            )

        new_subrace = Subrace(name=subrace.subrace_name, race_id=race.id)
        db.add(new_subrace)

        db.commit()
        db.refresh(new_subrace)
        logger.debug(
            f"Committed subrace with name '{new_subrace.name}' to the database."
        )

    except IntegrityError as e:
        logger.error(
            f"Subrace with the name '{subrace.subrace_name}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Subrace already exists.")
    try:
        if subrace.resistances:
            logger.debug(
                f"Trying to add resistances to subrace with id: {new_subrace.id}"
            )
            for resistance in subrace.resistances:
                damage_type = db.get(DamageType, resistance.damage_type_id)

                if not damage_type:
                    logger.error(
                        f"No damage type with id '{resistance.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{resistance.damage_type_id}' does not exist.",
                    )

                subrace_resistance = SubraceResistances(
                    subrace_id=new_subrace.id, damage_type_id=damage_type.id
                )
                db.add(subrace_resistance)
            logger.debug(f"Added resistances to '{new_subrace.name}'.")

        if subrace.immunities:
            logger.debug(
                f"Trying to add immunities to subrace with id: {new_subrace.id}"
            )
            for immunity in subrace.immunities:
                damage_type = db.get(DamageType, immunity.damage_type_id)

                if not damage_type:
                    logger.error(
                        f"No damage type with id '{immunity.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{immunity.damage_type_id}' does not exist.",
                    )

                subrace_immunity = SubraceImmunities(
                    subrace_id=new_subrace.id, damage_type_id=damage_type.id
                )
                db.add(subrace_immunity)
            logger.debug(f"Added immunities to '{new_subrace.name}'.")

        if subrace.vulnerabilities:
            logger.info(
                f"Trying to add vulnerabilities to subrace with id: {new_subrace.id}"
            )
            for vulnerability in subrace.vulnerabilities:
                damage_type = db.get(DamageType, vulnerability.damage_type_id)

                if not damage_type:
                    logger.error(
                        f"No damage type with id '{vulnerability.damage_type_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{vulnerability.damage_type_id}' does not exist.",
                    )

                subrace_vulnerability = SubraceVulnerabilities(
                    subrace_id=new_subrace.id, damage_type_id=damage_type.id
                )
                db.add(subrace_vulnerability)
            logger.debug(f"Added vulnerabilities to '{new_subrace.name}'.")

        if subrace.advantages:
            logger.info(
                f"Trying to add advantages to subrace with id: {new_subrace.id}"
            )
            for advantage in subrace.advantages:
                attribute = db.get(Attribute, advantage.attribute_id)

                if not attribute:
                    logger.error(
                        f"No attribute with id '{advantage.attribute_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Attribute with id '{advantage.attribute_id}' does not exist.",
                    )

                subrace_advantage = SubraceAdvantages(
                    subrace_id=new_subrace.id, attribute_id=attribute.id
                )
                db.add(subrace_advantage)
            logger.debug(f"Added advantages to '{new_subrace.name}'.")

        if subrace.disadvantages:
            logger.info(
                f"Trying to add disadvantages to subrace with id: {new_subrace.id}"
            )
            for disadvantage in subrace.disadvantages:
                attribute = db.get(Attribute, disadvantage.attribute_id)

                if not attribute:
                    logger.error(
                        f"No attribute with id '{disadvantage.attribute_id}' found."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Attribute with id '{disadvantage.attribute_id}' does not exist.",
                    )

                subrace_disadvantage = SubraceDisadvantages(
                    subrace_id=new_subrace.id, attribute_id=attribute.id
                )
                db.add(subrace_disadvantage)
            logger.debug(f"Added advantages to '{new_subrace.name}'.")

        db.commit()
        logger.debug(
            f"Committed '{new_subrace.name}' to the database with optional attributes and damage types."
        )

        return SubraceResponse(
            message=f"New subrace '{new_subrace.name}' has been added to the database.",
            subrace=new_subrace,
        )

    except IntegrityError as e:
        logger.error(
            f"Combination of subrace with the name '{subrace.subrace_name}'  \
            and a damage type or attribute already exists. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"The combination of subrace and damage type or attribute already exists.",
        )


@router.put("/{subrace_id}", response_model=SubraceResponse)
def put_subrace(
    subrace_id: int, subrace: SubracePutBase, db: Session = Depends(get_db)
) -> SubraceResponse:
    """
    Updates a subrace in the database by its unique id.

    - **Returns** SubraceResponse: A message and the updated subrace.

    - **HTTPException**: When the subrace id does not exist.
    - **HTTPException**: When the name of the subrace already exists in the database.

    **Request Body Example**:
    ```json
    {
        "subrace_name": "example_subrace",
        "race_id": example_int,
        "resistances": [
            {
                damage_type_id: 1,
                condition: "condition of the resistance",
                add_damage_type: bool,
            },
        ],
        "immunities": [
            {
                damage_type_id: 1,
                condition: "condition of the immunity",
                add_damage_type: bool,
            },
        ],
        "vulnerabilities": [
            {
                damage_type_id: 1,
                condition: "condition of the vulnerability",
                add_damage_type: bool,
            },
        ],
        "advantages": [
            {
                attribute_id: 1,
                condition: "condition of the advantage",
                add_attribute: bool,
            },
        ],
        "disadvantages": [
            {
                attribute_id: 1,
                condition: "condition of the disadvantage",
                add_attribute: bool,
            },
        ],
    }
    ```
    - `subrace_name`: A string between 1 and 50 characters long (inclusive).
    - `race_id`: The id of the parent race (inclusive).
    - `immunities`: Optional.
    - `resistances`: Optional.
    - `vulnerabilities`: Optional.
    - `advantages`: Optional.
    - `disadvantages`: Optional.

    **Response Example**:
    ```json
    {
        "message": "New subrace 'example_subrace' has been added to the database.",
        "subrace": {
        {
            "id": 1,
            "name": "example_subrace",
            "resistances": [{"id": 1, "name": "example_damage_type_type"}],
            "immunities": [{"id": 1, "name": "example_damage_type_type"}],
            "vulnerabilities": [{"id": 1, "name": "example_damage_type_type"}],
            "advantages": [{"id": 1, "name": "example_attribute_type"}],
            "disadvantages": [{"id": 1, "name": "example_attribute_type"}],
            "race": {
                "id": 1,
                "name": "Dwarf",
                "sizes": [{"id": 1, "name": "Tiny"}],
                "resistances": [{"id": 1, "name": "example_damage_type"}],
                "immunities": [],
                "vulnerabilities": [],
                "advantages": [{"id": 1, "name": "example_attribute_type"}],
                "disadvantages": [],
            },
        },
    }
    """
    try:
        logger.info(f"Updating subrace with id '{subrace_id}'.")

        updated_subrace = db.get(Subrace, subrace_id)
        if not updated_subrace:
            logger.error(f"Subclass with id '{subrace_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The subrace you are trying to update does not exist.",
            )

        if subrace.subrace_name:
            logger.debug(
                f"Changing subrace with id '{subrace_id}' name to '{subrace.subrace_name}'."
            )
            updated_subrace.name = subrace.subrace_name
        if subrace.race_id:
            logger.debug(
                f"Changing subrace with id '{subrace_id}' race id to '{subrace.race_id}'."
            )
            race = db.get(Race, subrace.race_id)
            if not race:
                logger.error(
                    f"Race with id '{subrace.race_id}' not found in the database."
                )
                raise HTTPException(
                    status_code=404,
                    detail="The race you are trying to link to this subrace does not exist.",
                )
            updated_subrace.race_id = race.id
        if subrace.immunities:
            logger.debug(
                f"Trying to change immunities for subrace '{updated_subrace.name}'."
            )

            for immunity in subrace.immunities:
                damage_type = db.get(DamageType, immunity.damage_type_id)

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
                        f"Adding immunity with name '{damage_type.name}' to subrace with id: {subrace_id}."
                    )

                    new_immunity = SubraceImmunities(
                        subrace_id=subrace_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    logger.debug(
                        f"Removing immunity with name '{damage_type.name}' from subrace with id: {subrace_id}."
                    )
                    stmt = select(SubraceImmunities).where(
                        and_(
                            SubraceImmunities.subrace_id == subrace_id,
                            SubraceImmunities.damage_type_id == damage_type.id,
                        )
                    )
                    old_immunity = db.execute(stmt).scalar_one_or_none()

                    if not old_immunity:
                        logger.error(
                            f"The subrace '{subrace_id}' does not have immunity with id '{damage_type.id}'."
                        )
                        raise HTTPException(
                            status_code=404,
                            detail=f"The subrace '{updated_subrace.name}' does not have this immunity.",
                        )

                    db.delete(old_immunity)
                logger.debug(
                    f"Changed immunities from subrace '{updated_subrace.name}'."
                )

        if subrace.resistances:
            for resistance in subrace.resistances:
                logger.debug(
                    f"Trying to change resistances for subrace '{updated_subrace.name}'."
                )
                damage_type = db.get(DamageType, resistance.damage_type_id)

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
                        f"Adding resistance with name '{damage_type.name}' to subrace with id: {subrace_id}."
                    )
                    new_resistance = SubraceResistances(
                        subrace_id=subrace_id,
                        damage_type_id=damage_type.id,
                        condition=resistance.condition,
                    )
                    db.add(new_resistance)
                else:
                    logger.debug(
                        f"Removing resistance with name '{damage_type.name}' from subrace with id: {subrace_id}."
                    )
                    stmt = select(SubraceResistances).where(
                        and_(
                            SubraceResistances.subrace_id == subrace_id,
                            SubraceResistances.damage_type_id == damage_type.id,
                        )
                    )
                    old_resistance = db.execute(stmt).scalar_one_or_none()

                    if not old_resistance:
                        logger.error(
                            f"The subrace '{subrace_id}' does not have resistance with id '{damage_type.id}'."
                        )

                        raise HTTPException(
                            status_code=404,
                            detail=f"The subrace '{updated_subrace.name}' does not have this resistance.",
                        )

                    db.delete(old_resistance)
                logger.debug(
                    f"Changed resistances from subrace '{updated_subrace.name}'."
                )

        if subrace.vulnerabilities:
            logger.debug(
                f"Trying to change vulnerabilities for subrace '{updated_subrace.name}'."
            )
            for vulnerability in subrace.vulnerabilities:
                damage_type = db.get(DamageType, vulnerability.damage_type_id)

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
                        f"Adding vulnerability with name '{damage_type.name}' to subrace with id: {subrace_id}."
                    )
                    new_vulnerability = SubraceVulnerabilities(
                        subrace_id=subrace_id,
                        damage_type_id=damage_type.id,
                        condition=vulnerability.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    logger.debug(
                        f"Removing resistance with name '{damage_type.name}' from subrace with id: {subrace_id}."
                    )
                    stmt = select(SubraceVulnerabilities).where(
                        and_(
                            SubraceVulnerabilities.subrace_id == subrace_id,
                            SubraceVulnerabilities.damage_type_id == damage_type.id,
                        )
                    )
                    old_vulnerability = db.execute(stmt).scalar_one_or_none()

                    if not old_vulnerability:
                        logger.error(
                            f"The subrace '{subrace_id}' does not have vulnerability with id '{damage_type.id}'."
                        )
                        raise HTTPException(
                            status_code=404,
                            detail=f"The subrace '{updated_subrace.name}' does not have this vulnerability.",
                        )

                    db.delete(old_vulnerability)
                logger.debug(
                    f"Changed vulnerabilities from subrace '{updated_subrace.name}'."
                )
        if subrace.advantages:
            logger.debug(
                f"Trying to change advantages for subrace '{updated_subrace.name}'."
            )
            for advantage in subrace.advantages:
                attribute = db.get(Attribute, advantage.attribute_id)

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
                        f"Adding advantage with name '{attribute.name}' to subrace with id: {subrace_id}."
                    )
                    new_advantage = SubraceAdvantages(
                        subrace_id=subrace_id,
                        attribute_id=attribute.id,
                        condition=advantage.condition,
                    )
                    db.add(new_advantage)
                else:
                    logger.debug(
                        f"Removing advantage with name '{attribute.name}' from subrace with id: {subrace_id}."
                    )
                    stmt = select(SubraceAdvantages).where(
                        and_(
                            SubraceAdvantages.subrace_id == subrace_id,
                            SubraceAdvantages.attribute_id == attribute.id,
                        )
                    )
                    old_advantage = db.execute(stmt).scalar_one_or_none()

                    if not old_advantage:
                        logger.error(
                            f"The subrace '{subrace_id}' does not have advantage with id '{attribute.id}'."
                        )
                        raise HTTPException(
                            status_code=404,
                            detail=f"The subrace '{updated_subrace.name}' does not have this advantage.",
                        )

                    db.delete(old_advantage)
                logger.debug(
                    f"Changed advantages from subrace '{updated_subrace.name}'."
                )

        if subrace.disadvantages:
            logger.debug(
                f"Trying to change disadvantages for subrace '{updated_subrace.name}'."
            )
            for disadvantage in subrace.disadvantages:
                attribute = db.get(Attribute, disadvantage.attribute_id)

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
                    new_disadvantage = SubraceDisadvantages(
                        subrace_id=subrace_id,
                        attribute_id=attribute.id,
                        condition=disadvantage.condition,
                    )
                    db.add(new_disadvantage)
                else:
                    stmt = select(SubraceDisadvantages).where(
                        and_(
                            SubraceDisadvantages.subrace_id == subrace_id,
                            SubraceDisadvantages.attribute_id == attribute.id,
                        )
                    )
                    old_disadvantage = db.execute(stmt).scalar_one_or_none()

                    if not old_disadvantage:
                        logger.error(
                            f"The subrace '{subrace_id}' does not have disadvantage with id '{attribute.id}'."
                        )
                        raise HTTPException(
                            status_code=404,
                            detail=f"The subrace '{updated_subrace.name}' does not have this disadvantage.",
                        )

                    db.delete(old_disadvantage)
                logger.debug(
                    f"Changed disadvantages from subrace '{updated_subrace.name}'."
                )

        db.commit()
        logger.info(f"Updated information of subrace with id '{subrace_id}'.")

        return SubraceResponse(
            message=f"Subrace '{updated_subrace.name}' has been updated.",
            subrace=updated_subrace,
        )
    except IntegrityError as e:
        logger.error(
            f"The name that is trying to be used already exists in the table. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{subrace_id}", response_model=DeleteResponse)
def delete_subrace(subrace_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a subrace from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Race has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting subrace with the id '{subrace_id}'.")
    subrace = db.get(Subrace, subrace_id)

    if not subrace:
        logger.error(f"Subrace with id '{subrace_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The subrace you are trying to delete does not exist.",
        )

    db.delete(subrace)
    db.commit()

    logger.info(f"Subrace with id '{subrace_id}' deleted.")
    return DeleteResponse(message="Subrace has been deleted.")
