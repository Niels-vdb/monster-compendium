from typing import Annotated, Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.api.models.creatures import CreaturePostBase, CreaturePutBase
from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.creatures import (
    CreatureImmunities,
    CreatureResistances,
    CreatureVulnerabilities,
)
from server.database.models.effects import Effect
from server.database.models.player_characters import PlayerCharacter
from server.database.models.races import Race, Subrace
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
    if pc.image:
        attributes["image"] = pc.image
    if pc.race:
        race = db.query(Race).filter(Race.id == pc.race).first()
        if not race:
            raise HTTPException(
                status_code=404, detail="Race with this id does not exist."
            )
        attributes["race"] = race.id
    if pc.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == pc.subrace).first()
        if not subrace:
            raise HTTPException(
                status_code=404, detail="Subrace with this id does not exist."
            )
        attributes["subrace"] = subrace.id
    if pc.size_id:
        size = db.query(Size).filter(Size.id == pc.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, detail="Size with this id does not exist."
            )
        attributes["size_id"] = size.id
    if pc.type_id:
        creature_type = db.query(Type).filter(Type.id == pc.type_id).first()
        if not creature_type:
            raise HTTPException(
                status_code=404, detail="Type with this id does not exist."
            )
        attributes["type_id"] = creature_type.id
    if pc.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in pc.parties
        ]
        for value in attributes["parties"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Party with this id does not exist."
                )
    if pc.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in pc.classes
        ]
        for value in attributes["classes"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Class with this id does not exist."
                )
    if pc.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in pc.subclasses
        ]
        for value in attributes["subclasses"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Subclass with this id does not exist."
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
            effect = db.query(Effect).filter(Effect.id == immunity.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            pc_immunity = CreatureImmunities(
                creature_id=new_pc.id,
                effect_id=effect.id,
                condition=immunity.condition,
            )
            db.add(pc_immunity)
    if pc.resistances:
        for resistance in pc.resistances:
            effect = db.query(Effect).filter(Effect.id == resistance.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            pc_resistance = CreatureResistances(
                creature_id=new_pc.id,
                effect_id=effect.id,
                condition=resistance.condition,
            )
            db.add(pc_resistance)
    if pc.vulnerabilities:
        for vulnerability in pc.vulnerabilities:
            effect = (
                db.query(Effect).filter(Effect.id == vulnerability.effect_id).first()
            )
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            pc_vulnerability = CreatureVulnerabilities(
                creature_id=new_pc.id,
                effect_id=effect.id,
                condition=vulnerability.condition,
            )
            db.add(pc_vulnerability)

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
        if pc.image:
            updated_pc.image = pc.image
        if pc.race:
            race = db.query(Race).filter(Race.id == pc.race).first()
            if not race:
                raise HTTPException(
                    status_code=404, detail="Race with this id does not exist."
                )
            updated_pc.race = race.id
        if pc.subrace:
            subrace = db.query(Subrace).filter(Subrace.id == pc.subrace).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="Subrace with this id does not exist."
                )
            updated_pc.subrace = subrace.id
        if pc.size_id:
            size = db.query(Size).filter(Size.id == pc.size_id).first()
            if not size:
                raise HTTPException(
                    status_code=404, detail="Size with this id does not exist."
                )
            updated_pc.size_id = size.id
        if pc.type_id:
            creature_type = db.query(Type).filter(Type.id == pc.type_id).first()
            if not creature_type:
                raise HTTPException(
                    status_code=404, detail="Type with this id does not exist."
                )
            updated_pc.type_id = creature_type.id
        if pc.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first() for cls in pc.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="Class with this id does not exist."
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
                        status_code=404, detail="Subclass with this id does not exist."
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
                        status_code=404, detail="Party with this id does not exist."
                    )
            if pc.add_parties:
                updated_pc.parties += parties
            else:
                for party in parties:
                    if party in updated_pc.parties:
                        updated_pc.parties.remove(party)
        if pc.immunities:
            for immunity in pc.immunities:
                effect = (
                    db.query(Effect).filter(Effect.id == immunity.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif immunity.add_effect:
                    new_immunity = CreatureImmunities(
                        creature_id=pc_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(CreatureImmunities)
                        .filter(
                            and_(
                                CreatureImmunities.creature_id == pc_id,
                                CreatureImmunities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if pc.resistances:
            for resistance in pc.resistances:
                effect = (
                    db.query(Effect).filter(Effect.id == resistance.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif resistance.add_effect:
                    new_resistance = CreatureResistances(
                        creature_id=pc_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(CreatureResistances)
                        .filter(
                            and_(
                                CreatureResistances.creature_id == pc_id,
                                CreatureResistances.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if pc.vulnerabilities:
            for vulnerability in pc.vulnerabilities:
                effect = (
                    db.query(Effect)
                    .filter(Effect.id == vulnerability.effect_id)
                    .first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif vulnerability.add_effect:
                    new_vulnerability = CreatureVulnerabilities(
                        creature_id=pc_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(CreatureVulnerabilities)
                        .filter(
                            and_(
                                CreatureVulnerabilities.creature_id == pc_id,
                                CreatureVulnerabilities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
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
