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
from server.models import Enemy
from server.models import Race
from server.models import Subrace
from server.models import Party
from server.api.utils.utilities import Utilities
from server.api.utils.creature_utilities import CreatureUtilities
from server.api.models.delete_response import DeleteResponse
from server.api.models.enemy import EnemyResponse
from server.api.models.creatures import (
    CreatureModel,
    CreaturePostBase,
    CreaturePutBase,
)

router = APIRouter(
    prefix="/api/enemies",
    tags=["Enemies"],
    responses={404: {"description": "Not found."}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.get("/", response_model=list[CreatureModel])
def get_enemies(db: Session = Depends(get_db)) -> list[CreatureModel]:
    """
    Queries the enemies database table for all rows.

    - **Returns** list[CreatureModel]: All enemy instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Giff",
            "description": "A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
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
            "name": "Frogemoth",
            "description": "A large Frog like creature",
            "information": "Some information about this big Frog.",
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
    logger.info("Querying enemies table for all results.")
    stmt = select(Enemy)
    enemies = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(enemies)} from the enemies table.")
    return enemies


@router.get("/{enemy_id}", response_model=CreatureModel)
def get_enemy(enemy_id: int, db: Session = Depends(get_db)) -> CreatureModel:
    """
    Queries the enemies table in the database table for a specific row with the id of enemy_id.

    - **Returns** CreatureModel: The enemy instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried enemy does not exist.

    **Response Example**:
    {
        "id": 1,
        "name": "Giff",
        "description": "A large hippo like creature",
        "information": "Some information about this big hippo, like his knowledge about firearms.",
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
    logger.info(f"Querying enemy table for row with id '{enemy_id}'.")
    stmt = select(Enemy).where(Enemy.id == enemy_id)
    enemy = db.execute(stmt).scalar_one_or_none()

    if not enemy:
        logger.error(f"No enemy with the id of '{enemy_id}'.")
        raise HTTPException(status_code=404, detail="Enemy not found.")

    logger.info(f"Returning enemy info with id of {enemy_id}.")
    return enemy


@router.post("/", response_model=EnemyResponse, status_code=201)
def post_enemy(enemy: CreaturePostBase, db: Session = Depends(get_db)) -> EnemyResponse:
    """
    Creates a new row in the enemies table.

    - **Returns** EnemyResponse: A dictionary holding a message and the new enemy.

    - **HTTPException**: If an enemy with this name already exists.

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
    - `information"`: A string with information about the enemy (optional).
    - `description`: A string with a description of the enemy (optional).
    - `image`: An image representing the enemy (optional). NOT YET IMPLEMENTED!!!!
    - `alive`: A boolean representing if the enemy is alive (optional).
    - `active`: A boolean representing if the enemy is active (optional).
    - `armour_class`: An integer representing the armour class of the enemy (optional).
    - `walking_speed`: An integer representing the walking speed of the enemy (optional).
    - `swimming_speed`: An integer representing the swimming speed of the enemy (optional).
    - `climbing_speed`: An integer representing the climbing speed of the enemy (optional).
    - `flying_speed`: An integer representing the flying speed of the enemy (optional).
    - `race_id`: An integer representing the race id of the enemy (optional).
    - `subrace_id`: An integer representing the subrace id of the enemy (optional).
    - `size_id`: An integer representing the size id of the enemy (optional).
    - `type_id`: An integer representing the type id of the enemy (optional).
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
        "enemy": {
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
            "parties": [PartyBase,],
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
    logger.info(f"Creating new enemy with name '{enemy.name}'.")

    utils = Utilities(db)

    attributes: dict[str, Any] = {}

    if enemy.name:
        logger.debug(f"Trying to add name to new enemy '{enemy.name}'.")
        attributes["name"] = enemy.name
    if enemy.description:
        logger.debug(f"Trying to add description to new enemy '{enemy.name}'.")
        attributes["description"] = enemy.description
    if enemy.information:
        logger.debug(f"Trying to add information to new enemy '{enemy.name}'.")
        attributes["information"] = enemy.information
    if enemy.alive != None:
        logger.debug(f"Trying to add alive status to new enemy '{enemy.name}'.")
        attributes["alive"] = enemy.alive
    if enemy.active != None:
        logger.debug(f"Trying to add active status to new enemy '{enemy.name}'.")
        attributes["active"] = enemy.active
    if enemy.armour_class:
        logger.debug(f"Trying to add armour class to new enemy '{enemy.name}'.")
        attributes["armour_class"] = enemy.armour_class
    if enemy.walking_speed:
        logger.debug(f"Trying to add walking speed to new enemy '{enemy.name}'.")
        attributes["walking_speed"] = enemy.walking_speed
    if enemy.swimming_speed:
        logger.debug(f"Trying to add swimming speed to new enemy '{enemy.name}'.")
        attributes["swimming_speed"] = enemy.swimming_speed
    if enemy.flying_speed:
        logger.debug(f"Trying to add flying speed to new enemy '{enemy.name}'.")
        attributes["flying_speed"] = enemy.flying_speed
    if enemy.climbing_speed:
        logger.debug(f"Trying to add climbing speed to new enemy '{enemy.name}'.")
        attributes["climbing_speed"] = enemy.climbing_speed
    if enemy.image:
        logger.debug(f"Trying to add image to new enemy '{enemy.name}'.")
        attributes["image"] = enemy.image
    if enemy.race_id:
        logger.debug(f"Trying to add race id to new enemy '{enemy.name}'.")
        attributes["race_id"] = utils.get_by_id(Race, enemy.race_id).id
    if enemy.subrace_id:
        logger.debug(f"Trying to add subrace id to new enemy '{enemy.name}'.")
        attributes["subrace_id"] = utils.get_by_id(Subrace, enemy.subrace_id).id
    if enemy.size_id:
        logger.debug(f"Trying to add size id to new enemy '{enemy.name}'.")
        attributes["size_id"] = utils.get_by_id(Size, enemy.size_id).id
    if enemy.type_id:
        logger.debug(f"Trying to add type id to new enemy '{enemy.name}'.")
        attributes["type_id"] = utils.get_by_id(Type, enemy.type_id).id
    if enemy.parties:
        logger.debug(f"Trying to add parties to new enemy '{enemy.name}'.")
        attributes["parties"] = [
            utils.get_by_id(Party, party) for party in enemy.parties
        ]
    if enemy.classes:
        logger.debug(f"Trying to add classes to new enemy '{enemy.name}'.")
        attributes["classes"] = [utils.get_by_id(Class, cls) for cls in enemy.classes]
    if enemy.subclasses:
        logger.debug(f"Trying to add subclasses to new enemy '{enemy.name}'.")
        attributes["subclasses"] = [
            utils.get_by_id(Subclass, subclass) for subclass in enemy.subclasses
        ]

    logger.debug(f"Added all initial information to new enemy '{enemy.name}'.")
    try:
        new_enemy = Enemy(**attributes)
        db.add(new_enemy)

        db.commit()
        db.refresh(new_enemy)
        logger.info(f"Committed enemy '{enemy.name}' to the database.")
    except Exception as e:
        logger.error(
            f"An error occurred while trying to create the enemy. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )

    logger.debug(f"Adding additional data to enemy '{enemy.name}'.")
    creature_utils = CreatureUtilities(db, new_enemy)

    if enemy.immunities:
        creature_utils.add_immunities(enemy.immunities)
    if enemy.resistances:
        creature_utils.add_resistances(enemy.resistances)
    if enemy.vulnerabilities:
        creature_utils.add_vulnerabilities(enemy.vulnerabilities)
    if enemy.advantages:
        creature_utils.add_advantages(enemy.advantages)
    if enemy.disadvantages:
        creature_utils.add_disadvantages(enemy.disadvantages)

    try:
        db.commit()
        logger.info(
            f"Committed additional data for '{new_enemy.name}' to the many to many tables."
        )
        return EnemyResponse(
            message=f"New enemy '{new_enemy.name}' has been added to the database.",
            enemy=new_enemy,
        )
    except Exception as e:
        logger.error(
            f"When trying to add additional data to '{new_enemy.name}' the following error occurred: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{enemy_id}", response_model=EnemyResponse)
def put_enemy(
    enemy_id: str, enemy: CreaturePutBase, db: Session = Depends(get_db)
) -> EnemyResponse:
    """
    Updates an enemy in the database by its unique id.

    - **Returns** ClassResponse: A message and the updated enemy.

    - **HTTPException**: When the enemy id does not exist.
    - **HTTPException**: When the updated .

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
    - `information"`: A new string with information about the enemy (optional).
    - `description`: A new string with a description of the enemy (optional).
    - `image`: An image representing the enemy (optional). NOT YET IMPLEMENTED!!!!
    - `alive`: A boolean representing if the enemy is alive (optional).
    - `active`: A boolean representing if the enemy is active (optional).
    - `armour_class`: An integer representing the new armour class of the enemy (optional).
    - `walking_speed`: An integer representing the new walking speed of the enemy (optional).
    - `swimming_speed`: An integer representing the new swimming speed of the enemy (optional).
    - `climbing_speed`: An integer representing the new climbing speed of the enemy (optional).
    - `flying_speed`: An integer representing the new flying speed of the enemy (optional).
    - `race_id`: An integer representing the new race id of the enemy (optional).
    - `subrace_id`: An integer representing the new subrace id of the enemy (optional).
    - `size_id`: An integer representing the new size id of the enemy (optional).
    - `type_id`: An integer representing the new type id of the enemy (optional).
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
        "enemy": {
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
        logger.info(f"Updating enemy with id '{enemy_id}'.")
        updated_enemy = db.get(Enemy, enemy_id)

        if not updated_enemy:
            logger.error(f"Class with id '{enemy_id}' not found.")
            raise HTTPException(
                status_code=404,
                detail="The enemy you are trying to update does not exist.",
            )

        utils = CreatureUtilities(db, updated_enemy)

        if enemy.name:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' name to '{enemy.name}'."
            )
            updated_enemy.name = enemy.name
        if enemy.description:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' description to '{enemy.description}'."
            )
            updated_enemy.description = enemy.description
        if enemy.information:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' information to '{enemy.information}'."
            )
            updated_enemy.information = enemy.information
        if enemy.alive != None:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' alive status to '{enemy.alive}'."
            )
            updated_enemy.alive = enemy.alive
        if enemy.active != None:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' active status to '{enemy.active}'."
            )
            updated_enemy.active = enemy.active
        if enemy.armour_class:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' armour class to '{enemy.armour_class}'."
            )
            updated_enemy.armour_class = enemy.armour_class
        if enemy.walking_speed:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' walking speed to '{enemy.walking_speed}'."
            )
            updated_enemy.walking_speed = enemy.walking_speed
        if enemy.swimming_speed:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' swimming speed to '{enemy.swimming_speed}'."
            )
            updated_enemy.swimming_speed = enemy.swimming_speed
        if enemy.flying_speed:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' flying speed to '{enemy.flying_speed}'."
            )
            updated_enemy.flying_speed = enemy.flying_speed
        if enemy.climbing_speed:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' climbing speed to '{enemy.climbing_speed}'."
            )
            updated_enemy.climbing_speed = enemy.climbing_speed
        if enemy.image:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' image.")
            updated_enemy.image = enemy.image
        if enemy.race_id:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' race_id to '{enemy.race_id}'."
            )
            utils.update_race(enemy.race_id)
        if enemy.subrace_id:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' subrace_id to '{enemy.subrace_id}'."
            )
            utils.update_subrace(enemy.subrace_id)
        if enemy.size_id:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' size_id to '{enemy.size_id}'."
            )
            utils.update_size(enemy.size_id)
        if enemy.type_id:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' type_id to '{enemy.type_id}'."
            )
            utils.update_type(enemy.type_id)
        if enemy.classes:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' classes .")
            utils.update_classes(enemy.classes)
        if enemy.subclasses:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' subclasses.")
            utils.update_subclasses(enemy.subclasses)
        if enemy.parties:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' parties.")
            utils.update_parties(enemy.parties)
        if enemy.immunities:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' immunities.")
            utils.update_immunities(enemy.immunities)
        if enemy.resistances:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' resistances.")
            utils.update_resistances(enemy.resistances)
        if enemy.vulnerabilities:
            logger.debug(
                f"Trying to change enemy with id '{enemy_id}' vulnerabilities."
            )
            utils.update_vulnerabilities(enemy.vulnerabilities)
        if enemy.advantages:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' advantages.")
            utils.update_advantages(enemy.advantages)
        if enemy.disadvantages:
            logger.debug(f"Trying to change enemy with id '{enemy_id}' disadvantages.")
            utils.update_disadvantages(enemy.disadvantages)

        db.commit()
        logger.info(f"Committed changes to enemy with id '{enemy_id}'.")

        return EnemyResponse(
            message=f"Enemy '{updated_enemy.name}' has been updated.",
            enemy=updated_enemy,
        )

    except IntegrityError as e:
        logger.error(
            f"The name '{enemy.name}' already exists in the database. Error: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{enemy_id}", response_model=DeleteResponse)
def delete_enemy(enemy_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes an enemy from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "Enemy has been deleted.",
    }
    ```
    """
    logger.info(f"Deleting enemy with the id '{enemy_id}'.")
    enemy = db.get(Enemy, enemy_id)

    if not enemy:
        logger.error(f"Enemy with id '{enemy_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The enemy you are trying to delete does not exist.",
        )
    db.delete(enemy)
    db.commit()

    logger.info(f"Enemy with id '{enemy_id}' deleted.")
    return DeleteResponse(message=f"Enemy has been deleted.")
