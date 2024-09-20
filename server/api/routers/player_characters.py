from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.api.models.creatures import CreaturePostBase, CreaturePutBase
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
from server.database.models.player_characters import PlayerCharacter
from server.database.models.races import Race
from server.database.models.subraces import Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/player_characters",
    tags=["Player Characters"],
    responses={404: {"description": "Not found."}},
)


class PCPostBase(CreaturePostBase):
    user_id: int


@router.get("/")
def get_pc_characters(db: Session = Depends(get_db)):
    pc_characters = db.query(PlayerCharacter).all()
    if not pc_characters:
        raise HTTPException(status_code=404, detail="No player characters found.")
    return {"player_characters": pc_characters}


@router.get("/{pc_id}")
def get_pc(pc_id: int, db: Session = Depends(get_db)):
    pc = db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_id).first()
    if not pc:
        raise HTTPException(status_code=404, detail="Player character not found.")
    return {
        "id": pc.id,
        "name": pc.name,
        "description": pc.description,
        "information": pc.information,
        "alive": pc.alive,
        "active": pc.active,
        "armour_class": pc.armour_class,
        "walking_speed": pc.walking_speed,
        "swimming_speed": pc.swimming_speed,
        "flying_speed": pc.flying_speed,
        "climbing_speed": pc.climbing_speed,
        "image": pc.image,
        "race": pc.race,
        "subrace": pc.subrace,
        "size": pc.size,
        "creature_type": pc.creature_type,
        "user": pc.user,
        "parties": pc.parties,
        "classes": pc.classes,
        "subclasses": pc.subclasses,
        "resistances": pc.resistances,
        "immunities": pc.immunities,
        "vulnerabilities": pc.vulnerabilities,
        "advantages": pc.advantages,
        "disadvantages": pc.disadvantages,
    }


@router.post("/")
def post_pc(pc: PCPostBase, db: Session = Depends(get_db)):
    attributes: dict[str, Any] = {}

    if pc.description:
        attributes["description"] = pc.description
    if pc.information:
        attributes["information"] = pc.information
    if pc.alive:
        attributes["alive"] = pc.alive
    if pc.active:
        attributes["active"] = pc.active
    if pc.armour_class:
        attributes["armour_class"] = pc.armour_class
    if pc.walking_speed:
        attributes["walking_speed"] = pc.walking_speed
    if pc.swimming_speed:
        attributes["swimming_speed"] = pc.swimming_speed
    if pc.flying_speed:
        attributes["flying_speed"] = pc.flying_speed
    if pc.climbing_speed:
        attributes["climbing_speed"] = pc.climbing_speed
    if pc.image:
        attributes["image"] = pc.image
    if pc.race:
        race = db.query(Race).filter(Race.id == pc.race).first()
        if not race:
            raise HTTPException(status_code=404, detail=f"This race does not exist.")
        attributes["race"] = race.id
    if pc.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == pc.subrace).first()
        if not subrace:
            raise HTTPException(status_code=404, detail=f"This subrace does not exist.")
        attributes["subrace"] = subrace.id
    if pc.size_id:
        size = db.query(Size).filter(Size.id == pc.size_id).first()
        if not size:
            raise HTTPException(status_code=404, detail=f"This size does not exist.")
        attributes["size_id"] = size.id
    if pc.type_id:
        creature_type = db.query(Type).filter(Type.id == pc.type_id).first()
        if not creature_type:
            raise HTTPException(status_code=404, detail=f"This type does not exist.")
        attributes["type_id"] = creature_type.id
    if pc.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in pc.parties
        ]
        for party in attributes["parties"]:
            if not party:
                raise HTTPException(
                    status_code=404, detail=f"This party does not exist."
                )
    if pc.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in pc.classes
        ]
        for cls in attributes["classes"]:
            if not cls:
                raise HTTPException(
                    status_code=404, detail=f"This class does not exist."
                )
    if pc.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in pc.subclasses
        ]
        for subclass in attributes["subclasses"]:
            if not subclass:
                raise HTTPException(
                    status_code=404, detail=f"This subclass does not exist."
                )

    try:
        new_pc = PlayerCharacter(name=pc.name, user_id=pc.user_id, **attributes)
        db.add(new_pc)
        db.commit()
        db.refresh(new_pc)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )
    if pc.immunities:
        for immunity in pc.immunities:
            damage_type = (
                db.query(DamageType)
                .filter(DamageType.id == immunity.damage_type_id)
                .first()
            )
            if not damage_type:
                raise HTTPException(
                    status_code=404,
                    detail=f"This damage type does not exist.",
                )
            pc_immunity = CreatureImmunities(
                creature_id=new_pc.id,
                damage_type_id=damage_type.id,
                condition=immunity.condition,
            )
            db.add(pc_immunity)
    if pc.resistances:
        for resistance in pc.resistances:
            damage_type = (
                db.query(DamageType)
                .filter(DamageType.id == resistance.damage_type_id)
                .first()
            )
            if not damage_type:
                raise HTTPException(
                    status_code=404,
                    detail=f"This damage type does not exist.",
                )
            pc_resistance = CreatureResistances(
                creature_id=new_pc.id,
                damage_type_id=damage_type.id,
                condition=resistance.condition,
            )
            db.add(pc_resistance)
    if pc.vulnerabilities:
        for vulnerability in pc.vulnerabilities:
            damage_type = (
                db.query(DamageType)
                .filter(DamageType.id == vulnerability.damage_type_id)
                .first()
            )
            if not damage_type:
                raise HTTPException(
                    status_code=404,
                    detail=f"This damage type does not exist.",
                )
            pc_vulnerability = CreatureVulnerabilities(
                creature_id=new_pc.id,
                damage_type_id=damage_type.id,
                condition=vulnerability.condition,
            )
            db.add(pc_vulnerability)
    if pc.advantages:
        for advantage in pc.advantages:
            attribute = (
                db.query(Attribute)
                .filter(Attribute.id == advantage.attribute_id)
                .first()
            )
            if not attribute:
                raise HTTPException(
                    status_code=404,
                    detail=f"This attribute does not exist.",
                )
            pc_advantage = CreatureAdvantages(
                creature_id=new_pc.id, attribute_id=attribute.id
            )
            db.add(pc_advantage)
    if pc.disadvantages:
        for disadvantage in pc.disadvantages:
            attribute = (
                db.query(Attribute)
                .filter(Attribute.id == disadvantage.attribute_id)
                .first()
            )
            if not attribute:
                raise HTTPException(
                    status_code=404,
                    detail=f"This attribute does not exist.",
                )
            pc_disadvantage = CreatureDisadvantages(
                creature_id=new_pc.id, attribute_id=attribute.id
            )
            db.add(pc_disadvantage)

    try:
        db.commit()
        return {
            "message": f"New player character '{new_pc.name}' has been added to the database.",
            "player_character": new_pc,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{pc_id}")
def put_pc(pc_id: str, pc: CreaturePutBase, db: Session = Depends(get_db)):
    try:
        updated_pc = (
            db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_id).first()
        )
        if pc.name:
            updated_pc.name = pc.name
        if pc.description:
            updated_pc.description = pc.description
        if pc.information:
            updated_pc.information = pc.information
        if pc.alive != None:
            updated_pc.alive = pc.alive
        if pc.active != None:
            updated_pc.active = pc.active
        if pc.armour_class:
            updated_pc.armour_class = pc.armour_class
        if pc.walking_speed:
            updated_pc.walking_speed = pc.walking_speed
        if pc.swimming_speed:
            updated_pc.swimming_speed = pc.swimming_speed
        if pc.flying_speed:
            updated_pc.flying_speed = pc.flying_speed
        if pc.climbing_speed:
            updated_pc.climbing_speed = pc.climbing_speed
        if pc.image:
            updated_pc.image = pc.image
        if pc.race:
            race = db.query(Race).filter(Race.id == pc.race).first()
            if not race:
                raise HTTPException(status_code=404, detail="This race does not exist.")
            updated_pc.race = race.id
        if pc.subrace:
            subrace = db.query(Subrace).filter(Subrace.id == pc.subrace).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="This subrace does not exist."
                )
            updated_pc.subrace = subrace.id
        if pc.size_id:
            size = db.query(Size).filter(Size.id == pc.size_id).first()
            if not size:
                raise HTTPException(status_code=404, detail="This size does not exist.")
            updated_pc.size_id = size.id
        if pc.type_id:
            creature_type = db.query(Type).filter(Type.id == pc.type_id).first()
            if not creature_type:
                raise HTTPException(status_code=404, detail="This type does not exist.")
            updated_pc.type_id = creature_type.id
        if pc.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first() for cls in pc.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="This class does not exist."
                    )
            if pc.add_class:
                updated_pc.classes += classes
            else:
                for cls in classes:
                    if cls in updated_pc.classes:
                        updated_pc.classes.remove(cls)
        if pc.subclasses:
            subclasses = [
                db.query(Subclass).filter(Subclass.id == subclass).first()
                for subclass in pc.subclasses
            ]
            for subclass in subclasses:
                if subclass == None:
                    raise HTTPException(
                        status_code=404, detail="This subclass does not exist."
                    )
            if pc.add_subclass:
                updated_pc.subclasses += subclasses
            else:
                for subclass in subclasses:
                    if subclass in updated_pc.subclasses:
                        updated_pc.subclasses.remove(subclass)
        if pc.parties:
            parties = [
                db.query(Party).filter(Party.id == party).first()
                for party in pc.parties
            ]
            for party in parties:
                if party == None:
                    raise HTTPException(
                        status_code=404, detail="This party does not exist."
                    )
            if pc.add_parties:
                updated_pc.parties += parties
            else:
                for party in parties:
                    if party in updated_pc.parties:
                        updated_pc.parties.remove(party)
        if pc.immunities:
            for immunity in pc.immunities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == immunity.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail=f"This damage type does not exist.",
                    )
                elif immunity.add_damage_type:
                    new_immunity = CreatureImmunities(
                        creature_id=pc_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(CreatureImmunities)
                        .filter(
                            and_(
                                CreatureImmunities.creature_id == pc_id,
                                CreatureImmunities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if pc.resistances:
            for resistance in pc.resistances:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == resistance.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail=f"This damage type does not exist.",
                    )
                elif resistance.add_damage_type:
                    new_resistance = CreatureResistances(
                        creature_id=pc_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(CreatureResistances)
                        .filter(
                            and_(
                                CreatureResistances.creature_id == pc_id,
                                CreatureResistances.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if pc.vulnerabilities:
            for vulnerability in pc.vulnerabilities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == vulnerability.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail=f"This damage type does not exist.",
                    )
                elif vulnerability.add_damage_type:
                    new_vulnerability = CreatureVulnerabilities(
                        creature_id=pc_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(CreatureVulnerabilities)
                        .filter(
                            and_(
                                CreatureVulnerabilities.creature_id == pc_id,
                                CreatureVulnerabilities.damage_type_id
                                == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        if pc.advantages:
            for advantage in pc.advantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == advantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail=f"This attribute does not exist.",
                    )
                elif advantage.add_attribute:
                    new_advantage = CreatureAdvantages(
                        creature_id=pc_id,
                        attribute_id=attribute.id,
                        condition=advantage.condition,
                    )
                    db.add(new_advantage)
                else:
                    old_advantage = (
                        db.query(CreatureAdvantages)
                        .filter(
                            and_(
                                CreatureAdvantages.creature_id == pc_id,
                                CreatureAdvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_advantage)
        if pc.disadvantages:
            for disadvantage in pc.disadvantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == disadvantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail=f"This attribute does not exist.",
                    )
                elif disadvantage.add_attribute:
                    new_disadvantage = CreatureDisadvantages(
                        creature_id=pc_id,
                        attribute_id=attribute.id,
                        condition=disadvantage.condition,
                    )
                    db.add(new_disadvantage)
                else:
                    old_disadvantage = (
                        db.query(CreatureDisadvantages)
                        .filter(
                            and_(
                                CreatureDisadvantages.creature_id == pc_id,
                                CreatureDisadvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_disadvantage)

        db.commit()
        return {
            "message": f"Player character '{updated_pc.name}' has been updated.",
            "player_character": updated_pc,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{pc_id}")
def delete_pc(pc_id: int, db: Session = Depends(get_db)):
    pc = db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_id).first()
    if not pc:
        raise HTTPException(
            status_code=404,
            detail="The player character you are trying to delete does not exist.",
        )
    db.delete(pc)
    db.commit()
    return {"message": f"Player character has been deleted."}
