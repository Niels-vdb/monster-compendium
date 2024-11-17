from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.config.logger_config import logger
from server.api.auth.security import oauth2_scheme
from server.models import Size
from server.models import Type
from server.models import Class
from server.models import Subclass
from server.models import PlayerCharacter
from server.models import Race
from server.models import Subrace
from server.models import Party
from server.api.models.delete_response import DeleteResponse
from server.api.models.creatures import CreaturePutBase
from server.api.models.player_character import PCModel, PCPostBase, PCResponse
from server.api.utils.creature_utilities import CreatureUtilities
from server.api.utils.utilities import Utilities

router = APIRouter(
    prefix="/api/player_characters",
    tags=["Player Characters"],
    responses={404: {"description": "Not found."}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.get("/", response_model=list[PCModel])
def get_pc_characters(db: Session = Depends(get_db)) -> list[PCModel]:
    """
    Queries the non player characters database table for all rows.

    - **Returns** list[PCModel]: All class instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Rhoetus",
            "description": "A centaur barbarian.",
            "information": "Some information about this centaur.",
            "alive": True,
            "active": True,
            "armour_class": 17,
            "walking_speed": 40,
            "swimming_speed": 20,
            "flying_speed": 0,
            "climbing_speed": None,
            "image": None,
            "race": None,
            "subrace": None,
            "size": {"id": 1, "name": "Medium"},
            "creature_type": {"id": 1, "name": "Humanoid"},
            "classes": [{"id": 1, "name": "Artificer"}],
            "subclasses": [{"id": 1, "name": "Alchemist"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "resistances": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
            "user": {"id": 1, "name": "test1", "username": "Test1", "image": None},
        },
        {
            "id": 2,
            "name": "Electra",
            "description": "A beautiful Naiad.",
            "information": "Some information the woman who enchanted all.",
            "alive": True,
            "active": True,
            "armour_class": 18,
            "walking_speed": 30,
            "swimming_speed": 20,
            "flying_speed": 0,
            "climbing_speed": None,
            "image": None,
            "race": None,
            "subrace": None,
            "size": {"id": 1, "name": "Medium"},
            "creature_type": {"id": 1, "name": "Humanoid"},
            "classes": [{"id": 1, "name": "Artificer"}],
            "subclasses": [{"id": 1, "name": "Alchemist"}],
            "immunities": [{"id": 1, "name": "Fire"}],
            "resistances": [{"id": 1, "name": "Fire"}],
            "vulnerabilities": [{"id": 1, "name": "Fire"}],
            "advantages": [{"id": 1, "name": "Charmed"}],
            "disadvantages": [{"id": 1, "name": "Charmed"}],
            "user": {"id": 2, "name": "test2", "username": "Test2", "image": None},
        },
    ]
    """
    logger.info("Querying player characters table for all results.")
    stmt = select(PlayerCharacter)
    player_characters = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(player_characters)} from the player characters table.")
    return player_characters


@router.get("/{pc_id}", response_model=PCModel)
def get_pc(pc_id: int, db: Session = Depends(get_db)) -> PCModel:
    """
    Queries the pc's table in the database table for a specific row with the id of pc_id.

    - **Returns** PCModel: The player character instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried player character does not exist.

    **Response Example**:
    {
        "id": 1,
        "name": "Rhoetus",
        "description": "A centaur barbarian.",
        "information": "Some information about this centaur.",
        "alive": True,
        "active": True,
        "armour_class": 17,
        "walking_speed": 40,
        "swimming_speed": 20,
        "flying_speed": 0,
        "climbing_speed": None,
        "image": None,
        "race": None,
        "subrace": None,
        "size": {"id": 1, "name": "Medium"},
        "creature_type": {"id": 1, "name": "Humanoid"},
        "classes": [{"id": 1, "name": "Artificer"}],
        "subclasses": [{"id": 1, "name": "Alchemist"}],
        "immunities": [{"id": 1, "name": "Fire"}],
        "resistances": [{"id": 1, "name": "Fire"}],
        "vulnerabilities": [{"id": 1, "name": "Fire"}],
        "advantages": [{"id": 1, "name": "Charmed"}],
        "disadvantages": [{"id": 1, "name": "Charmed"}],
    }
    """
    logger.info(f"Querying pc table for row with id '{pc_id}'.")
    stmt = select(PlayerCharacter).where(PlayerCharacter.id == pc_id)
    pc = db.execute(stmt).scalar_one_or_none()

    if not pc:
        logger.error(f"No pc with the id of '{pc_id}'.")
        raise HTTPException(status_code=404, detail="Player character not found.")

    logger.info(f"Returning pc info with id of {pc_id}.")
    return pc


@router.post("/", response_model=PCResponse, status_code=201)
def post_pc(pc: PCPostBase, db: Session = Depends(get_db)) -> PCResponse:
    """
    Creates a new row in the pc's table.

    - **Returns** PCResponse: A dictionary holding a message and the new pc.

    - **HTTPException**: If an pc with this name already exists.

    **Request Body Example**:
    ```json
    {
        "name": "example_name",
        "user_id": int,
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
    - `user_id`: The id of the user this character belongs to (inclusive).
    - `information"`: A string with information about the pc (optional).
    - `description`: A string with a description of the pc (optional).
    - `image`: An image representing the pc (optional). NOT YET IMPLEMENTED!!!!
    - `alive`: A boolean representing if the pc is alive (optional).
    - `active`: A boolean representing if the pc is active (optional).
    - `armour_class`: An integer representing the armour class of the pc (optional).
    - `walking_speed`: An integer representing the walking speed of the pc (optional).
    - `swimming_speed`: An integer representing the swimming speed of the pc (optional).
    - `climbing_speed`: An integer representing the climbing speed of the pc (optional).
    - `flying_speed`: An integer representing the flying speed of the pc (optional).
    - `race_id`: An integer representing the race id of the pc (optional).
    - `subrace_id`: An integer representing the subrace id of the pc (optional).
    - `size_id`: An integer representing the size id of the pc (optional).
    - `type_id`: An integer representing the type id of the pc (optional).
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
        "pc": {
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
            "user": {"id": 1, "name": "test", "username": "Test", "image": None},
    }
    ```
    """
    logger.info(f"Creating new pc with name '{pc.name}'.")

    utils = Utilities(db)

    attributes: dict[str, Any] = {
        "name": pc.name,
        "user_id": pc.user_id,
    }

    if pc.description:
        logger.debug(f"Trying to add description to new pc '{pc.name}'.")
        attributes["description"] = pc.description
    if pc.information:
        logger.debug(f"Trying to add information to new pc '{pc.name}'.")
        attributes["information"] = pc.information
    if pc.alive != None:
        logger.debug(f"Trying to add alive status to new pc '{pc.name}'.")
        attributes["alive"] = pc.alive
    if pc.active != None:
        logger.debug(f"Trying to add active status to new pc '{pc.name}'.")
        attributes["active"] = pc.active
    if pc.armour_class:
        logger.debug(f"Trying to add armour class to new pc '{pc.name}'.")
        attributes["armour_class"] = pc.armour_class
    if pc.walking_speed:
        logger.debug(f"Trying to add walking speed to new pc '{pc.name}'.")
        attributes["walking_speed"] = pc.walking_speed
    if pc.swimming_speed:
        logger.debug(f"Trying to add swimming speed to new pc '{pc.name}'.")
        attributes["swimming_speed"] = pc.swimming_speed
    if pc.flying_speed:
        logger.debug(f"Trying to add flying speed to new pc '{pc.name}'.")
        attributes["flying_speed"] = pc.flying_speed
    if pc.climbing_speed:
        logger.debug(f"Trying to add climbing speed to new pc '{pc.name}'.")
        attributes["climbing_speed"] = pc.climbing_speed
    if pc.image:
        logger.debug(f"Trying to add image to new pc '{pc.name}'.")
        attributes["image"] = pc.image
    if pc.race_id:
        logger.debug(f"Trying to add race id to new pc '{pc.name}'.")
        attributes["race_id"] = utils.get_by_id(Race, pc.race_id).id
    if pc.subrace_id:
        logger.debug(f"Trying to add subrace id to new pc '{pc.name}'.")
        attributes["subrace_id"] = utils.get_by_id(Subrace, pc.subrace_id).id
    if pc.size_id:
        logger.debug(f"Trying to add size id to new pc '{pc.name}'.")
        attributes["size_id"] = utils.get_by_id(Size, pc.size_id).id
    if pc.type_id:
        logger.debug(f"Trying to add type id to new pc '{pc.name}'.")
        attributes["type_id"] = utils.get_by_id(Type, pc.type_id).id
    if pc.parties:
        logger.debug(f"Trying to add parties to new pc '{pc.name}'.")
        attributes["parties"] = [utils.get_by_id(Party, party) for party in pc.parties]
    if pc.classes:
        logger.debug(f"Trying to add classes to new pc '{pc.name}'.")
        attributes["classes"] = [utils.get_by_id(Class, cls) for cls in pc.classes]
    if pc.subclasses:
        logger.debug(f"Trying to add subclasses to new pc '{pc.name}'.")
        attributes["subclasses"] = [
            utils.get_by_id(Subclass, subclass) for subclass in pc.subclasses
        ]

    logger.debug(f"Added all initial information to new pc '{pc.name}'.")
    try:
        new_pc = PlayerCharacter(**attributes)
        db.add(new_pc)

        db.commit()
        db.refresh(new_pc)
        logger.info(f"Committed pc '{pc.name}' to the database.")
    except Exception as e:
        logger.error(
            f"An error occurred while trying to create the pc. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )

    logger.debug(f"Adding additional data to pc '{pc.name}'.")
    creature_utils = CreatureUtilities(db, new_pc)

    if pc.immunities:
        creature_utils.add_immunities(pc.immunities)
    if pc.resistances:
        creature_utils.add_resistances(pc.resistances)
    if pc.vulnerabilities:
        creature_utils.add_vulnerabilities(pc.vulnerabilities)
    if pc.advantages:
        creature_utils.add_advantages(pc.advantages)
    if pc.disadvantages:
        creature_utils.add_disadvantages(pc.disadvantages)

    try:
        db.commit()
        logger.info(
            f"Committed additional data for '{new_pc.name}' to the many to many tables."
        )
        return PCResponse(
            message=f"New pc '{new_pc.name}' has been added to the database.",
            pc=new_pc,
        )
    except Exception as e:
        logger.error(
            f"When trying to add additional data to '{new_pc.name}' the following error occurred: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{pc_id}", response_model=PCResponse)
def put_pc(
        pc_id: str, pc: CreaturePutBase, db: Session = Depends(get_db)
) -> PCResponse:
    """
    Updates an pc in the database by its unique id.

    - **Returns** PCResponse: A message and the updated pc.

    - **HTTPException**: When the pc id does not exist.

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
    - `information"`: A new string with information about the pc (optional).
    - `description`: A new string with a description of the pc (optional).
    - `image`: An image representing the pc (optional). NOT YET IMPLEMENTED!!!!
    - `alive`: A boolean representing if the pc is alive (optional).
    - `active`: A boolean representing if the pc is active (optional).
    - `armour_class`: An integer representing the new armour class of the pc (optional).
    - `walking_speed`: An integer representing the new walking speed of the pc (optional).
    - `swimming_speed`: An integer representing the new swimming speed of the pc (optional).
    - `climbing_speed`: An integer representing the new climbing speed of the pc (optional).
    - `flying_speed`: An integer representing the new flying speed of the pc (optional).
    - `race_id`: An integer representing the new race id of the pc (optional).
    - `subrace_id`: An integer representing the new subrace id of the pc (optional).
    - `size_id`: An integer representing the new size id of the pc (optional).
    - `type_id`: An integer representing the new type id of the pc (optional).
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
        "message": "Player character 'example_name' has been updated.",
        "pc": {
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
            "user": {"id": 1, "name": "test", "username": "Test", "image": None},
    }
    ```
    """
    try:
        logger.info(f"Updating pc with id '{pc_id}'.")
        updated_pc = db.get(PlayerCharacter, pc_id)

        if not updated_pc:
            logger.error(f"Class with id '{pc_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The pc you are trying to update does not exist.",
            )

        utils = CreatureUtilities(db, updated_pc)

        if pc.name:
            logger.debug(f"Trying to change pc with id '{pc_id}' name to '{pc.name}'.")
            updated_pc.name = pc.name
        if pc.description:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' description to '{pc.description}'."
            )
            updated_pc.description = pc.description
        if pc.information:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' information to '{pc.information}'."
            )
            updated_pc.information = pc.information
        if pc.alive != None:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' alive status to '{pc.alive}'."
            )
            updated_pc.alive = pc.alive
        if pc.active != None:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' active status to '{pc.active}'."
            )
            updated_pc.active = pc.active
        if pc.armour_class:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' armour class to '{pc.armour_class}'."
            )
            updated_pc.armour_class = pc.armour_class
        if pc.walking_speed:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' walking speed to '{pc.walking_speed}'."
            )
            updated_pc.walking_speed = pc.walking_speed
        if pc.swimming_speed:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' swimming speed to '{pc.swimming_speed}'."
            )
            updated_pc.swimming_speed = pc.swimming_speed
        if pc.flying_speed:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' flying speed to '{pc.flying_speed}'."
            )
            updated_pc.flying_speed = pc.flying_speed
        if pc.climbing_speed:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' climbing speed to '{pc.climbing_speed}'."
            )
            updated_pc.climbing_speed = pc.climbing_speed
        if pc.image:
            logger.debug(f"Trying to change pc with id '{pc_id}' image.")
            updated_pc.image = pc.image
        if pc.race_id:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' race_id to '{pc.race_id}'."
            )
            utils.update_race(pc.race_id)
        if pc.subrace_id:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' subrace_id to '{pc.subrace_id}'."
            )
            utils.update_subrace(pc.subrace_id)
        if pc.size_id:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' size_id to '{pc.size_id}'."
            )
            utils.update_size(pc.size_id)
        if pc.type_id:
            logger.debug(
                f"Trying to change pc with id '{pc_id}' type_id to '{pc.type_id}'."
            )
            utils.update_type(pc.type_id)
        if pc.classes:
            logger.debug(f"Trying to change pc with id '{pc_id}' classes .")
            utils.update_classes(pc.classes)
        if pc.subclasses:
            logger.debug(f"Trying to change pc with id '{pc_id}' subclasses.")
            utils.update_subclasses(pc.subclasses)
        if pc.parties:
            logger.debug(f"Trying to change pc with id '{pc_id}' parties.")
            utils.update_parties(pc.parties)
        if pc.immunities:
            logger.debug(f"Trying to change pc with id '{pc_id}' immunities.")
            utils.update_immunities(pc.immunities)
        if pc.resistances:
            logger.debug(f"Trying to change pc with id '{pc_id}' resistances.")
            utils.update_resistances(pc.resistances)
        if pc.vulnerabilities:
            logger.debug(f"Trying to change pc with id '{pc_id}' vulnerabilities.")
            utils.update_vulnerabilities(pc.vulnerabilities)
        if pc.advantages:
            logger.debug(f"Trying to change pc with id '{pc_id}' advantages.")
            utils.update_advantages(pc.advantages)
        if pc.disadvantages:
            logger.debug(f"Trying to change pc with id '{pc_id}' disadvantages.")
            utils.update_disadvantages(pc.disadvantages)

        db.commit()
        logger.info(f"Committed changes to pc with id '{pc_id}'.")

        return PCResponse(
            message=f"Player character '{updated_pc.name}' has been updated.",
            pc=updated_pc,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{pc.name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{pc_id}", response_model=DeleteResponse)
def delete_pc(pc_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a pc from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "NPC has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting pc with the id '{pc_id}'.")
    pc = db.get(PlayerCharacter, pc_id)

    if not pc:
        logger.error(f"Player character with id '{pc_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The player character you are trying to delete does not exist.",
        )

    db.delete(pc)
    db.commit()

    logger.info(f"Player character with id '{pc_id}' deleted.")
    return DeleteResponse(message=f"Player character has been deleted.")
