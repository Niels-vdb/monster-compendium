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
from server.database.models.non_player_characters import NonPlayerCharacter
from server.database.models.races import Race, Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/non_player_characters",
    tags=["Non Player Characters"],
    responses={404: {"description": "Not found."}},
)


@router.get("/")
def get_npcs(db: Session = Depends(get_db)):
    npc_characters = db.query(NonPlayerCharacter).all()
    if not npc_characters:
        raise HTTPException(status_code=404, detail="No NPC's found.")
    return {"non_player_characters": npc_characters}


@router.get("/{npc_id}")
def get_npc(npc_id: int, db: Session = Depends(get_db)):
    npc = db.query(NonPlayerCharacter).filter(NonPlayerCharacter.id == npc_id).first()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found.")
    return {
        "id": npc.id,
        "name": npc.name,
        "description": npc.description,
        "information": npc.information,
        "active": npc.active,
        "alive": npc.alive,
        "armour_class": npc.armour_class,
        "walking_speed": npc.walking_speed,
        "swimming_speed": npc.swimming_speed,
        "swimming_speed": npc.swimming_speed,
        "image": npc.image,
        "race": npc.race,
        "subrace": npc.subrace,
        "size": npc.size,
        "type": npc.type_id,
        "creature_type": npc.creature_type,
        "parties": npc.parties,
        "classes": npc.classes,
        "subclasses": npc.subclasses,
        "resistances": npc.resistances,
        "immunities": npc.immunities,
        "vulnerabilities": npc.vulnerabilities,
    }


@router.post("/")
def post_npc(npc: CreaturePostBase, db: Session = Depends(get_db)):
    attributes: dict[str, Any] = {}

    if npc.description:
        attributes["description"] = npc.description
    if npc.information:
        attributes["information"] = npc.information
    if npc.alive:
        attributes["alive"] = npc.alive
    if npc.active:
        attributes["active"] = npc.active
    if npc.armour_class:
        attributes["armour_class"] = npc.armour_class
    if npc.walking_speed:
        attributes["walking_speed"] = npc.walking_speed
    if npc.swimming_speed:
        attributes["swimming_speed"] = npc.swimming_speed
    if npc.flying_speed:
        attributes["flying_speed"] = npc.flying_speed
    if npc.image:
        attributes["image"] = npc.image
    if npc.race:
        race = db.query(Race).filter(Race.id == npc.race).first()
        if not race:
            raise HTTPException(
                status_code=404, detail="Race with this id does not exist."
            )
        attributes["race"] = race.id
    if npc.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == npc.subrace).first()
        if not subrace:
            raise HTTPException(
                status_code=404, detail="Subrace with this id does not exist."
            )
        attributes["subrace"] = subrace.id
    if npc.size_id:
        size = db.query(Size).filter(Size.id == npc.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, detail="Size with this id does not exist."
            )
        attributes["size_id"] = size.id
    if npc.type_id:
        creature_type = db.query(Type).filter(Type.id == npc.type_id).first()
        if not creature_type:
            raise HTTPException(
                status_code=404, detail="Type with this id does not exist."
            )
        attributes["type_id"] = creature_type.id
    if npc.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in npc.parties
        ]
        for value in attributes["parties"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Party with this id does not exist."
                )
    if npc.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in npc.classes
        ]
        for value in attributes["classes"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Class with this id does not exist."
                )
    if npc.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in npc.subclasses
        ]
        for value in attributes["subclasses"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Subclass with this id does not exist."
                )
    try:
        new_npc = NonPlayerCharacter(name=npc.name, **attributes)
        db.add(new_npc)
        db.commit()
        db.refresh(new_npc)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )

    if npc.immunities:
        for immunity in npc.immunities:
            effect = db.query(Effect).filter(Effect.id == immunity.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            npc_immunity = CreatureImmunities(
                creature_id=new_npc.id,
                effect_id=effect.id,
                condition=immunity.condition,
            )
            db.add(npc_immunity)
    if npc.resistances:
        for resistance in npc.resistances:
            effect = db.query(Effect).filter(Effect.id == resistance.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            npc_resistance = CreatureResistances(
                creature_id=new_npc.id,
                effect_id=effect.id,
                condition=resistance.condition,
            )
            db.add(npc_resistance)
    if npc.vulnerabilities:
        for vulnerability in npc.vulnerabilities:
            effect = (
                db.query(Effect).filter(Effect.id == vulnerability.effect_id).first()
            )
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            npc_vulnerability = CreatureVulnerabilities(
                creature_id=new_npc.id,
                effect_id=effect.id,
                condition=vulnerability.condition,
            )
            db.add(npc_vulnerability)
    try:
        db.commit()
        return {
            "message": f"New npc '{new_npc.name}' has been added to the database.",
            "npc": new_npc,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{npc_id}")
def put_npc(npc_id: str, npc: CreaturePutBase, db: Session = Depends(get_db)):
    try:
        updated_npc = (
            db.query(NonPlayerCharacter).filter(NonPlayerCharacter.id == npc_id).first()
        )
        if npc.name:
            updated_npc.name = npc.name
        if npc.description:
            updated_npc.description = npc.description
        if npc.information:
            updated_npc.information = npc.information
        if npc.alive != None:
            updated_npc.alive = npc.alive
        if npc.active != None:
            updated_npc.active = npc.active
        if npc.armour_class:
            updated_npc.armour_class = npc.armour_class
        if npc.walking_speed:
            updated_npc.walking_speed = npc.walking_speed
        if npc.flying_speed:
            updated_npc.flying_speed = npc.flying_speed
        if npc.swimming_speed:
            updated_npc.swimming_speed = npc.swimming_speed
        if npc.image:
            updated_npc.image = npc.image
        if npc.race:
            race = db.query(Race).filter(Race.id == npc.race).first()
            if not race:
                raise HTTPException(
                    status_code=404, detail="Race with this id does not exist."
                )
            updated_npc.race = race.id
        if npc.subrace:
            subrace = db.query(Subrace).filter(Subrace.id == npc.subrace).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="Subrace with this id does not exist."
                )
            updated_npc.subrace = subrace.id
        if npc.size_id:
            size = db.query(Size).filter(Size.id == npc.size_id).first()
            if not size:
                raise HTTPException(
                    status_code=404, detail="Size with this id does not exist."
                )
            updated_npc.size_id = size.id
        if npc.type_id:
            creature_type = db.query(Type).filter(Type.id == npc.type_id).first()
            if not creature_type:
                raise HTTPException(
                    status_code=404, detail="Type with this id does not exist."
                )
            updated_npc.type_id = creature_type.id
        if npc.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first() for cls in npc.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="Class with this id does not exist."
                    )
            if npc.add_class:
                updated_npc.classes += classes
            else:
                for cls in classes:
                    if cls in updated_npc.classes:
                        updated_npc.classes.remove(cls)
        if npc.subclasses:
            subclasses = [
                db.query(Subclass).filter(Subclass.id == subclass).first()
                for subclass in npc.subclasses
            ]
            for subclass in subclasses:
                if subclass == None:
                    raise HTTPException(
                        status_code=404, detail="Subclass with this id does not exist."
                    )
            if npc.add_subclass:
                updated_npc.subclasses += subclasses
            else:
                for subclass in subclasses:
                    if subclass in updated_npc.subclasses:
                        updated_npc.subclasses.remove(subclass)
        if npc.parties:
            parties = [
                db.query(Party).filter(Party.id == party).first()
                for party in npc.parties
            ]
            for party in parties:
                if party == None:
                    raise HTTPException(
                        status_code=404, detail="Party with this id does not exist."
                    )
            if npc.add_parties:
                updated_npc.parties += parties
            else:
                for party in parties:
                    if party in updated_npc.parties:
                        updated_npc.parties.remove(party)
        if npc.immunities:
            for immunity in npc.immunities:
                effect = (
                    db.query(Effect).filter(Effect.id == immunity.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif immunity.add_effect:
                    new_immunity = CreatureImmunities(
                        creature_id=npc_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(CreatureImmunities)
                        .filter(
                            and_(
                                CreatureImmunities.creature_id == npc_id,
                                CreatureImmunities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if npc.resistances:
            for resistance in npc.resistances:
                effect = (
                    db.query(Effect).filter(Effect.id == resistance.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif resistance.add_effect:
                    new_resistance = CreatureResistances(
                        creature_id=npc_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(CreatureResistances)
                        .filter(
                            and_(
                                CreatureResistances.creature_id == npc_id,
                                CreatureResistances.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if npc.vulnerabilities:
            for vulnerability in npc.vulnerabilities:
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
                        creature_id=npc_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(CreatureVulnerabilities)
                        .filter(
                            and_(
                                CreatureVulnerabilities.creature_id == npc_id,
                                CreatureVulnerabilities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        db.commit()
        return {
            "message": f"NPC '{updated_npc.name}' has been updated.",
            "non_player_character": updated_npc,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{npc_id}")
def delete_npc(npc_id: int, db: Session = Depends(get_db)):
    npc = db.query(NonPlayerCharacter).filter(NonPlayerCharacter.id == npc_id).first()
    if not npc:
        raise HTTPException(
            status_code=404,
            detail="The NPC you are trying to delete does not exist.",
        )
    db.delete(npc)
    db.commit()
    return {"message": f"NPC has been deleted."}
