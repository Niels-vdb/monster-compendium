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
from server.database.models.non_player_characters import NonPlayerCharacter
from server.database.models.races import Race
from server.database.models.subraces import Subrace
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
        "flying_speed": npc.flying_speed,
        "climbing_speed": npc.climbing_speed,
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
        "advantages": npc.advantages,
        "disadvantages": npc.disadvantages,
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
    if npc.climbing_speed:
        attributes["climbing_speed"] = npc.climbing_speed
    if npc.image:
        attributes["image"] = npc.image
    if npc.race_id:
        race = db.query(Race).filter(Race.id == npc.race_id).first()
        if not race:
            raise HTTPException(status_code=404, detail="This race does not exist.")
        attributes["race_id"] = race.id
    if npc.subrace_id:
        subrace = db.query(Subrace).filter(Subrace.id == npc.subrace_id).first()
        if not subrace:
            raise HTTPException(status_code=404, detail="This subrace does not exist.")
        attributes["subrace_id"] = subrace.id
    if npc.size_id:
        size = db.query(Size).filter(Size.id == npc.size_id).first()
        if not size:
            raise HTTPException(status_code=404, detail="This size does not exist.")
        attributes["size_id"] = size.id
    if npc.type_id:
        creature_type = db.query(Type).filter(Type.id == npc.type_id).first()
        if not creature_type:
            raise HTTPException(status_code=404, detail="This type does not exist.")
        attributes["type_id"] = creature_type.id
    if npc.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in npc.parties
        ]
        for party in attributes["parties"]:
            if not party:
                raise HTTPException(
                    status_code=404, detail="This party does not exist."
                )
    if npc.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in npc.classes
        ]
        for cls in attributes["classes"]:
            if not cls:
                raise HTTPException(
                    status_code=404, detail="This class does not exist."
                )
    if npc.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in npc.subclasses
        ]
        for subclass in attributes["subclasses"]:
            if not subclass:
                raise HTTPException(
                    status_code=404, detail="This subclass does not exist."
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
            npc_immunity = CreatureImmunities(
                creature_id=new_npc.id,
                damage_type_id=damage_type.id,
                condition=immunity.condition,
            )
            db.add(npc_immunity)
    if npc.resistances:
        for resistance in npc.resistances:
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
            npc_resistance = CreatureResistances(
                creature_id=new_npc.id,
                damage_type_id=damage_type.id,
                condition=resistance.condition,
            )
            db.add(npc_resistance)
    if npc.vulnerabilities:
        for vulnerability in npc.vulnerabilities:
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
            npc_vulnerability = CreatureVulnerabilities(
                creature_id=new_npc.id,
                damage_type_id=damage_type.id,
                condition=vulnerability.condition,
            )
            db.add(npc_vulnerability)
    if npc.advantages:
        for advantage in npc.advantages:
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
            npc_advantage = CreatureAdvantages(
                creature_id=new_npc.id, attribute_id=attribute.id
            )
            db.add(npc_advantage)
    if npc.disadvantages:
        for disadvantage in npc.disadvantages:
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
            npc_disadvantage = CreatureDisadvantages(
                creature_id=new_npc.id, attribute_id=attribute.id
            )
            db.add(npc_disadvantage)
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
        if npc.climbing_speed:
            updated_npc.climbing_speed = npc.climbing_speed
        if npc.image:
            updated_npc.image = npc.image
        if npc.race_id:
            race = db.query(Race).filter(Race.id == npc.race_id).first()
            if not race:
                raise HTTPException(status_code=404, detail="This race does not exist.")
            updated_npc.race_id = race.id
        if npc.subrace_id:
            subrace = db.query(Subrace).filter(Subrace.id == npc.subrace_id).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="This subrace does not exist."
                )
            updated_npc.subrace_id = subrace.id
        if npc.size_id:
            size = db.query(Size).filter(Size.id == npc.size_id).first()
            if not size:
                raise HTTPException(status_code=404, detail="This size does not exist.")
            updated_npc.size_id = size.id
        if npc.type_id:
            creature_type = db.query(Type).filter(Type.id == npc.type_id).first()
            if not creature_type:
                raise HTTPException(status_code=404, detail="This type does not exist.")
            updated_npc.type_id = creature_type.id
        if npc.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first() for cls in npc.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="This class does not exist."
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
                        status_code=404, detail="This subclass does not exist."
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
                        status_code=404, detail="This party does not exist."
                    )
            if npc.add_parties:
                updated_npc.parties += parties
            else:
                for party in parties:
                    if party in updated_npc.parties:
                        updated_npc.parties.remove(party)
        if npc.immunities:
            for immunity in npc.immunities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == immunity.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail="This damage type does not exist.",
                    )
                elif immunity.add_damage_type:
                    new_immunity = CreatureImmunities(
                        creature_id=npc_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(CreatureImmunities)
                        .filter(
                            and_(
                                CreatureImmunities.creature_id == npc_id,
                                CreatureImmunities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if npc.resistances:
            for resistance in npc.resistances:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == resistance.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail="This damage type does not exist.",
                    )
                elif resistance.add_damage_type:
                    new_resistance = CreatureResistances(
                        creature_id=npc_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(CreatureResistances)
                        .filter(
                            and_(
                                CreatureResistances.creature_id == npc_id,
                                CreatureResistances.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if npc.vulnerabilities:
            for vulnerability in npc.vulnerabilities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == vulnerability.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail="This damage type does not exist.",
                    )
                elif vulnerability.add_damage_type:
                    new_vulnerability = CreatureVulnerabilities(
                        creature_id=npc_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(CreatureVulnerabilities)
                        .filter(
                            and_(
                                CreatureVulnerabilities.creature_id == npc_id,
                                CreatureVulnerabilities.damage_type_id
                                == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        if npc.advantages:
            for advantage in npc.advantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == advantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail="This attribute does not exist.",
                    )
                elif advantage.add_attribute:
                    new_advantage = CreatureAdvantages(
                        creature_id=npc_id,
                        attribute_id=attribute.id,
                        condition=advantage.condition,
                    )
                    db.add(new_advantage)
                else:
                    old_advantage = (
                        db.query(CreatureAdvantages)
                        .filter(
                            and_(
                                CreatureAdvantages.creature_id == npc_id,
                                CreatureAdvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_advantage)
        if npc.disadvantages:
            for disadvantage in npc.disadvantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == disadvantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail="This attribute does not exist.",
                    )
                elif disadvantage.add_attribute:
                    new_disadvantage = CreatureDisadvantages(
                        creature_id=npc_id,
                        attribute_id=attribute.id,
                        condition=disadvantage.condition,
                    )
                    db.add(new_disadvantage)
                else:
                    old_disadvantage = (
                        db.query(CreatureDisadvantages)
                        .filter(
                            and_(
                                CreatureDisadvantages.creature_id == npc_id,
                                CreatureDisadvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_disadvantage)

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
