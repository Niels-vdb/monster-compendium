from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.api.models.delete_response import DeleteResponse
from server.api.utils.creature_utilities import CreatureUtilities
from server.api.utils.utilities import Utilities
from server.logger.logger import logger
from server.api.models.base_response import BaseResponse
from server.api.models.creatures import CreatureModel, CreaturePostBase, CreaturePutBase
from server.database.models.attributes import Attribute
from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.creatures import (
    CreatureAdvantages,
    CreatureDisadvantages,
    CreatureImmunities,
    CreatureResistances,
    CreatureVulnerabilities,
)
from server.database.models.damage_types import DamageType
from server.database.models.non_player_characters import NonPlayerCharacter
from server.database.models.races import Race
from server.database.models.subraces import Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/non_player_characters",
    tags=["Non Player Characters"],
    responses={404: {"description": "Not found."}},
)


class NPCResponse(BaseResponse):
    """
    Response model for creating or retrieving a npc.
    Inherits from BaseResponse

    - `message`: A descriptive message about the action performed.
    - `npc`: The actual npc data, represented by the `CreatureModel`.
    """

    npc: CreatureModel


@router.get("/", response_model=list[CreatureModel])
def get_npcs(db: Session = Depends(get_db)) -> list[CreatureModel]:
    """
    Queries the non player characters database table for all rows.

    - **Returns** list[CreatureModel]: All class instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Endofyre",
            "description": "A lying god",
            "information": "Some information about this deceiving goddess.",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "walking_speed": 30,
            "swimming_speed": 20,
            "flying_speed": 0,
            "climbing_speed": None,
            "image": None,
            "race": None,
            "subrace": None,
            "size": {"id": 1, "name": "Tiny"},
            "creature_type": {"id": 1, "name": "Aberration"},
            "classes": [{"id": 1, "name": "Artificer"}],
            "subclasses": [{"id": 1, "name": "Alchemist"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "resistances": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
        {
            "id": 2,
            "name": "Oracle",
            "description": "The daughter of a god",
            "information": "Some information the woman who knows all.",
            "alive": True,
            "active": True,
            "armour_class": 16,
            "walking_speed": 30,
            "swimming_speed": 20,
            "flying_speed": 0,
            "climbing_speed": None,
            "image": None,
            "race": None,
            "subrace": None,
            "size": {"id": 1, "name": "Tiny"},
            "creature_type": {"id": 1, "name": "Aberration"},
            "classes": [{"id": 1, "name": "Artificer"}],
            "subclasses": [{"id": 1, "name": "Alchemist"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "resistances": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
        },
    ]
    """
    logger.info("Querying npc's table for all results.")
    stmt = select(NonPlayerCharacter)
    npcs = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(npcs)} from the npc's table.")
    return npcs


@router.get("/{npc_id}", response_model=CreatureModel)
def get_npc(npc_id: int, db: Session = Depends(get_db)) -> CreatureModel:
    """
    Queries the npc's table in the database table for a specific row with the id of enemy_id.

    - **Returns** CreatureModel: The enemy instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried enemy does not exist.

    **Response Example**:
    {
        "id": 1,
        "name": "Endofyre",
        "description": "A lying god",
        "information": "Some information about this deceiving goddess.",
        "alive": True,
        "active": True,
        "armour_class": 16,
        "walking_speed": 30,
        "swimming_speed": 20,
        "flying_speed": 0,
        "climbing_speed": None,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"id": 1, "name": "Tiny"},
        "creature_type": {"id": 1, "name": "Aberration"},
        "classes": [{"id": 1, "name": "Artificer"}],
        "subclasses": [{"id": 1, "name": "Alchemist"}],
        "immunities": [{"id": 1, "name": "Fire"}],
        "resistances": [{"id": 1, "name": "Fire"}],
        "vulnerabilities": [{"id": 1, "name": "Fire"}],
        "advantages": [{"id": 1, "name": "Charmed"}],
        "disadvantages": [{"id": 1, "name": "Charmed"}],
    }
    """
    logger.info(f"Querying npc table for row with id '{npc_id}'.")
    stmt = select(NonPlayerCharacter).where(NonPlayerCharacter.id == npc_id)
    npc = db.execute(stmt).scalar_one_or_none()

    if not npc:
        logger.error(f"No npc with the id of '{npc_id}'.")
        raise HTTPException(status_code=404, detail="Non player character not found.")

    logger.info(f"Returning npc info with id of {npc_id}.")
    return npc


@router.post("/", response_model=NPCResponse, status_code=201)
def post_npc(npc: CreaturePostBase, db: Session = Depends(get_db)) -> NPCResponse:
    """
    Creates a new row in the npc's table.

    - **Returns** NPCResponse: A dictionary holding a message and the new npc.

    - **HTTPException**: If an npc with this name already exists.

    **Request Body Example**:
    ```json
    {
        "name": "example_name",
        "information": "example_information.",
        "description": "example_description.",
        "image": bytes,
        "alive": boolean,
        "active": boolean,
        "armour_class": in,
        "walking_speed": int,
        "swimming_speed": int,
        "climbing_speed": int,
        "flying_speed": int,
        "race_id": int,
        "subrace_id": int,
        "size_id": int,
        "type_id": int,
        "classes": [int],
        "subclasses": [int],
        "parties": [int],
        "resistances": [PostDamageType,],
        "immunities": [PostDamageType,],
        "vulnerabilities": [PostDamageType,],
        "advantages": [PostAttribute,],
        "disadvantages": [PostAttribute,],
    }
    ```
    - `name`: A string between 1 and 50 characters long (inclusive).
    - `information"`: A string with information about the npc (optional).
    - `description`: A string with a description of the npc (optional).
    - `image`: An image representing the npc (optional). NOT YET IMPLEMENTED!!!!
    - `alive`: A boolean representing if the npc is alive (optional).
    - `active`: A boolean representing if the npc is active (optional).
    - `armour_class`: An integer representing the armour class of the npc (optional).
    - `walking_speed`: An integer representing the walking speed of the npc (optional).
    - `swimming_speed`: An integer representing the swimming speed of the npc (optional).
    - `climbing_speed`: An integer representing the climbing speed of the npc (optional).
    - `flying_speed`: An integer representing the flying speed of the npc (optional).
    - `race_id`: An integer representing the race id of the npc (optional).
    - `subrace_id`: An integer representing the subrace id of the npc (optional).
    - `size_id`: An integer representing the size id of the npc (optional).
    - `type_id`: An integer representing the type id of the npc (optional).
    - `classes`: A list holding the id integers to add a class (optional).
    - `subclasses`: A list holding the id integers to add a subclass (optional).
    - `parties`: A list holding the id integers to add a party (optional).
    - `resistances`: A dictionary with the structure of PostDamageType to add a resistance (optional).
    - `immunities`: A dictionary with the structure of PostDamageType to add a immunities (optional).
    - `vulnerabilities`: A dictionary with the structure of PostDamageType to add a vulnerabilities (optional).
    - `advantages`: A dictionary with the structure of PostAttribute to add a advantages (optional).
    - `disadvantages`: A dictionary with the structure of PostAttribute to add a disadvantages (optional).

    **Response Example**:
    ```json
    {
        "message": "Enemy 'example_name' has been created.",
        "npc": {
            "id": 1,
            "name": "example_name",
            "description": "example_description",
            "information": "example_information",
            "alive": boolean,
            "active": boolean,
            "armour_class": int,
            "walking_speed": int,
            "swimming_speed": int,
            "flying_speed":int,
            "climbing_speed": int,
            "image": None,
            "race": RaceBase,
            "subrace": SubraceBase,
            "size": SizeBase,
            "creature_type": TypeBase,
            "classes": [ClassBase],
            "subclasses": [SubclassBase],
            "immunities": [DamageTypeBase,],
            "resistances": [DamageTypeBase,],
            "vulnerabilities": [DamageTypeBase,],
            "advantages": [AttributeBase,],
            "disadvantages": [AttributeBase,],
    }
    ```
    """
    logger.info(f"Creating new npc with name '{npc.name}'.")

    utils = Utilities(db)

    attributes: dict[str, Any] = {}

    if npc.name:
        logger.debug(f"Trying to add name to new npc '{npc.name}'.")
        attributes["name"] = npc.name
    if npc.description:
        logger.debug(f"Trying to add description to new npc '{npc.name}'.")
        attributes["description"] = npc.description
    if npc.information:
        logger.debug(f"Trying to add information to new npc '{npc.name}'.")
        attributes["information"] = npc.information
    if npc.alive != None:
        logger.debug(f"Trying to add alive status to new npc '{npc.name}'.")
        attributes["alive"] = npc.alive
    if npc.active != None:
        logger.debug(f"Trying to add active status to new npc '{npc.name}'.")
        attributes["active"] = npc.active
    if npc.armour_class:
        logger.debug(f"Trying to add armour class to new npc '{npc.name}'.")
        attributes["armour_class"] = npc.armour_class
    if npc.walking_speed:
        logger.debug(f"Trying to add walking speed to new npc '{npc.name}'.")
        attributes["walking_speed"] = npc.walking_speed
    if npc.swimming_speed:
        logger.debug(f"Trying to add swimming speed to new npc '{npc.name}'.")
        attributes["swimming_speed"] = npc.swimming_speed
    if npc.flying_speed:
        logger.debug(f"Trying to add flying speed to new npc '{npc.name}'.")
        attributes["flying_speed"] = npc.flying_speed
    if npc.climbing_speed:
        logger.debug(f"Trying to add climbing speed to new npc '{npc.name}'.")
        attributes["climbing_speed"] = npc.climbing_speed
    if npc.image:
        logger.debug(f"Trying to add image to new npc '{npc.name}'.")
        attributes["image"] = npc.image
    if npc.race_id:
        logger.debug(f"Trying to add race id to new npc '{npc.name}'.")
        attributes["race_id"] = utils.get_by_id(Race, npc.race_id).id
    if npc.subrace_id:
        logger.debug(f"Trying to add subrace id to new npc '{npc.name}'.")
        attributes["subrace_id"] = utils.get_by_id(Subrace, npc.subrace_id).id
    if npc.size_id:
        logger.debug(f"Trying to add size id to new npc '{npc.name}'.")
        attributes["size_id"] = utils.get_by_id(Size, npc.size_id).id
    if npc.type_id:
        logger.debug(f"Trying to add type id to new npc '{npc.name}'.")
        attributes["type_id"] = utils.get_by_id(Type, npc.type_id).id
    if npc.parties:
        logger.debug(f"Trying to add parties to new npc '{npc.name}'.")
        attributes["parties"] = [utils.get_by_id(Party, party) for party in npc.parties]
    if npc.classes:
        logger.debug(f"Trying to add classes to new npc '{npc.name}'.")
        attributes["classes"] = [utils.get_by_id(Class, cls) for cls in npc.classes]
    if npc.subclasses:
        logger.debug(f"Trying to add subclasses to new npc '{npc.name}'.")
        attributes["subclasses"] = [
            utils.get_by_id(Subclass, subclass) for subclass in npc.subclasses
        ]

    logger.debug(f"Added all initial information to new npc '{npc.name}'.")
    try:
        new_npc = NonPlayerCharacter(**attributes)
        db.add(new_npc)

        db.commit()
        db.refresh(new_npc)
        logger.info(f"Committed npc '{npc.name}' to the database.")
    except Exception as e:
        logger.error(
            f"An error occurred while trying to create the npc. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )

    logger.debug(f"Adding additional data to npc '{npc.name}'.")
    creature_utils = CreatureUtilities(db, new_npc)

    if npc.immunities:
        creature_utils.add_immunities(npc.immunities)
    if npc.resistances:
        creature_utils.add_resistances(npc.resistances)
    if npc.vulnerabilities:
        creature_utils.add_vulnerabilities(npc.vulnerabilities)
    if npc.advantages:
        creature_utils.add_advantages(npc.advantages)
    if npc.disadvantages:
        creature_utils.add_disadvantages(npc.disadvantages)

    try:
        db.commit()
        logger.info(
            f"Committed additional data for '{new_npc.name}' to the many to many tables."
        )
        return NPCResponse(
            message=f"New npc '{new_npc.name}' has been added to the database.",
            npc=new_npc,
        )
    except Exception as e:
        logger.error(
            f"When trying to add additional data to '{new_npc.name}' the following error occurred: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{npc_id}", response_model=NPCResponse)
def put_npc(
    npc_id: str, npc: CreaturePutBase, db: Session = Depends(get_db)
) -> NPCResponse:
    """
    Updates an npc in the database by its unique id.

    - **Returns** NPCResponse: A message and the updated npc.

    - **HTTPException**: When the npc id does not exist.

    **Request Body Example**:
    ```json
    {
        "name": "example_name",
        "information": "example_information.",
        "description": "example_description.",
        "image": bytes,
        "alive": boolean,
        "active": boolean,
        "armour_class": in,
        "walking_speed": int,
        "swimming_speed": int,
        "climbing_speed": int,
        "flying_speed": int,
        "race_id": int,
        "subrace_id": int,
        "size_id": int,
        "type_id": int,
        "classes": [PutClass,],
        "subclasses": [PutSubclass,],
        "parties": [PutParty,],
        "resistances": [PutDamageType,],
        "immunities": [PutDamageType,],
        "vulnerabilities": [PutDamageType,],
        "advantages": [PutAttribute,],
        "disadvantages": [PutAttribute,],
    }
    ```
    - `name`: A new string between 1 and 50 characters long (optional).
    - `information"`: A new string with information about the npc (optional).
    - `description`: A new string with a description of the npc (optional).
    - `image`: An image representing the npc (optional). NOT YET IMPLEMENTED!!!!
    - `alive`: A boolean representing if the npc is alive (optional).
    - `active`: A boolean representing if the npc is active (optional).
    - `armour_class`: An integer representing the new armour class of the npc (optional).
    - `walking_speed`: An integer representing the new walking speed of the npc (optional).
    - `swimming_speed`: An integer representing the new swimming speed of the npc (optional).
    - `climbing_speed`: An integer representing the new climbing speed of the npc (optional).
    - `flying_speed`: An integer representing the new flying speed of the npc (optional).
    - `race_id`: An integer representing the new race id of the npc (optional).
    - `subrace_id`: An integer representing the new subrace id of the npc (optional).
    - `size_id`: An integer representing the new size id of the npc (optional).
    - `type_id`: An integer representing the new type id of the npc (optional).
    - `classes`: A dictionary with the structure of PutClass to add or delete a class (optional).
    - `subclasses`: A dictionary with the structure of PutSubclass to add or delete a subclass (optional).
    - `parties`: A dictionary with the structure of PutParty to add or delete a party (optional).
    - `resistances`: A dictionary with the structure of PutDamageType to add or delete a resistance (optional).
    - `immunities`: A dictionary with the structure of PutDamageType to add or delete a immunities (optional).
    - `vulnerabilities`: A dictionary with the structure of PutDamageType to add or delete a vulnerabilities (optional).
    - `advantages`: A dictionary with the structure of PutAttribute to add or delete a advantages (optional).
    - `disadvantages`: A dictionary with the structure of PutAttribute to add or delete a disadvantages (optional).

    **Response Example**:
    ```json
    {
        "message": "Enemy 'example_name' has been updated.",
        "npc": {
            "id": 1,
            "name": "example_name",
            "description": "example_description",
            "information": "example_information",
            "alive": boolean,
            "active": boolean,
            "armour_class": int,
            "walking_speed": int,
            "swimming_speed": int,
            "flying_speed":int,
            "climbing_speed": int,
            "image": None,
            "race": RaceBase,
            "subrace": SubraceBase,
            "size": SizeBase,
            "creature_type": TypeBase,
            "classes": [ClassBase,],
            "subclasses": [SubclassBase,],
            "immunities": [DamageTypeBase,],
            "resistances": [DamageTypeBase,],
            "vulnerabilities": [DamageTypeBase,],
            "advantages": [AttributeBase,],
            "disadvantages": [AttributeBase,],
    }
    ```
    """
    try:
        logger.info(f"Updating npc with id '{npc_id}'.")
        updated_npc = db.get(NonPlayerCharacter, npc_id)

        if not updated_npc:
            logger.error(f"Class with id '{npc_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The npc you are trying to update does not exist.",
            )

        utils = CreatureUtilities(db, updated_npc)

        if npc.name:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' name to '{npc.name}'."
            )
            updated_npc.name = npc.name
        if npc.description:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' description to '{npc.description}'."
            )
            updated_npc.description = npc.description
        if npc.information:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' information to '{npc.information}'."
            )
            updated_npc.information = npc.information
        if npc.alive != None:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' alive status to '{npc.alive}'."
            )
            updated_npc.alive = npc.alive
        if npc.active != None:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' active status to '{npc.active}'."
            )
            updated_npc.active = npc.active
        if npc.armour_class:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' armour class to '{npc.armour_class}'."
            )
            updated_npc.armour_class = npc.armour_class
        if npc.walking_speed:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' walking speed to '{npc.walking_speed}'."
            )
            updated_npc.walking_speed = npc.walking_speed
        if npc.swimming_speed:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' swimming speed to '{npc.swimming_speed}'."
            )
            updated_npc.swimming_speed = npc.swimming_speed
        if npc.flying_speed:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' flying speed to '{npc.flying_speed}'."
            )
            updated_npc.flying_speed = npc.flying_speed
        if npc.climbing_speed:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' climbing speed to '{npc.climbing_speed}'."
            )
            updated_npc.climbing_speed = npc.climbing_speed
        if npc.image:
            logger.debug(f"Trying to change npc with id '{npc_id}' image.")
            updated_npc.image = npc.image
        if npc.race_id:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' race_id to '{npc.race_id}'."
            )
            utils.update_race(npc.race_id)
        if npc.subrace_id:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' subrace_id to '{npc.subrace_id}'."
            )
            utils.update_subrace(npc.subrace_id)
        if npc.size_id:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' size_id to '{npc.size_id}'."
            )
            utils.update_size(npc.size_id)
        if npc.type_id:
            logger.debug(
                f"Trying to change npc with id '{npc_id}' type_id to '{npc.type_id}'."
            )
            utils.update_type(npc.type_id)
        if npc.classes:
            logger.debug(f"Trying to change npc with id '{npc_id}' classes .")
            utils.update_classes(npc.classes)
        if npc.subclasses:
            logger.debug(f"Trying to change npc with id '{npc_id}' subclasses.")
            utils.update_subclasses(npc.subclasses)
        if npc.parties:
            logger.debug(f"Trying to change npc with id '{npc_id}' parties.")
            utils.update_parties(npc.parties)
        if npc.immunities:
            logger.debug(f"Trying to change npc with id '{npc_id}' immunities.")
            utils.update_immunities(npc.immunities)
        if npc.resistances:
            logger.debug(f"Trying to change npc with id '{npc_id}' resistances.")
            utils.update_resistances(npc.resistances)
        if npc.vulnerabilities:
            logger.debug(f"Trying to change npc with id '{npc_id}' vulnerabilities.")
            utils.update_vulnerabilities(npc.vulnerabilities)
        if npc.advantages:
            logger.debug(f"Trying to change npc with id '{npc_id}' advantages.")
            utils.update_advantages(npc.advantages)
        if npc.disadvantages:
            logger.debug(f"Trying to change npc with id '{npc_id}' disadvantages.")
            utils.update_disadvantages(npc.disadvantages)

        db.commit()
        logger.info(f"Committed changes to npc with id '{npc_id}'.")

        return NPCResponse(
            message=f"Enemy '{updated_npc.name}' has been updated.",
            npc=updated_npc,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{npc.name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{npc_id}", response_model=DeleteResponse)
def delete_npc(npc_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes an npc from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "NPC has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting npc with the id '{npc_id}'.")
    npc = db.get(NonPlayerCharacter, npc_id)
    if not npc:
        logger.error(f"NPC with id '{npc_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The NPC you are trying to delete does not exist.",
        )

    db.delete(npc)
    db.commit()

    logger.info(f"NPC with id '{npc_id}' deleted.")
    return DeleteResponse(message=f"NPC has been deleted.")
