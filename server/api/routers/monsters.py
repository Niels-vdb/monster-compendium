from typing import Annotated, Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db

from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.creatures import (
    CreatureImmunities,
    CreatureResistances,
    CreatureVulnerabilities,
)
from server.database.models.effects import Effect
from server.database.models.monsters import Monster
from server.database.models.races import Race, Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/monsters",
    tags=["Monsters"],
    responses={404: {"description": "Not found."}},
)


class PostEffect(BaseModel):
    effect_id: int
    condition: str


class PutEffect(BaseModel):
    effect_id: int
    condition: str = None
    add_effect: bool


class MonsterPostBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    armour_class: int = None
    walking_speed: int = None
    swimming_speed: int = None
    flying_speed: int = None
    image: bytes = None

    race: int = None
    subrace: int = None
    size_id: int = None
    type_id: int = None

    parties: list[int] = None
    classes: list[int] = None
    subclasses: list[int] = None
    immunities: list[PostEffect] = None
    resistances: list[PostEffect] = None
    vulnerabilities: list[PostEffect] = None


class MonsterPutBase(BaseModel):
    name: str = None
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    armour_class: int = None
    walking_speed: int = None
    swimming_speed: int = None
    flying_speed: int = None
    image: bytes = None

    race: int = None
    subrace: int = None
    size_id: int = None
    type_id: int = None

    classes: list[int] = None
    add_class: bool = None
    subclasses: list[int] = None
    add_subclass: bool = None
    parties: list[int] = None
    add_parties: bool = None
    immunities: list[PutEffect] = None
    resistances: list[PutEffect] = None
    vulnerabilities: list[PutEffect] = None


@router.get("/")
def get_monsters(db: Session = Depends(get_db)):
    monsters = db.query(Monster).all()
    if not monsters:
        raise HTTPException(status_code=404, detail="No monsters found.")
    return {"monsters": monsters}


@router.get("/{monster_id}")
def get_monster(monster_id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == monster_id).first()
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found.")
    return {
        "id": monster.id,
        "name": monster.name,
        "description": monster.description,
        "information": monster.information,
        "alive": monster.alive,
        "active": monster.active,
        "armour_class": monster.armour_class,
        "walking_speed": monster.walking_speed,
        "swimming_speed": monster.swimming_speed,
        "flying_speed": monster.flying_speed,
        "image": monster.image,
        "race": monster.race,
        "subrace": monster.subrace,
        "size": monster.size,
        "creature_type": monster.creature_type,
        "parties": monster.parties,
        "classes": monster.classes,
        "subclasses": monster.subclasses,
        "resistances": monster.resistances,
        "immunities": monster.immunities,
        "vulnerabilities": monster.vulnerabilities,
    }


@router.post("/")
def post_monster(monster: MonsterPostBase, db: Session = Depends(get_db)):
    attributes: dict[str, Any] = {}

    if monster.description:
        attributes["description"] = monster.description
    if monster.information:
        attributes["information"] = monster.information
    if monster.alive:
        attributes["alive"] = monster.alive
    if monster.active:
        attributes["active"] = monster.active
    if monster.armour_class:
        attributes["armour_class"] = monster.armour_class
    if monster.walking_speed:
        attributes["walking_speed"] = monster.walking_speed
    if monster.swimming_speed:
        attributes["swimming_speed"] = monster.swimming_speed
    if monster.flying_speed:
        attributes["flying_speed"] = monster.flying_speed
    if monster.image:
        attributes["image"] = monster.image
    if monster.race:
        race = db.query(Race).filter(Race.id == monster.race).first()
        if not race:
            raise HTTPException(
                status_code=404, detail="Race with this id does not exist."
            )
        attributes["race"] = race.id
    if monster.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == monster.subrace).first()
        if not subrace:
            raise HTTPException(
                status_code=404, detail="Subrace with this id does not exist."
            )
        attributes["subrace"] = subrace.id
    if monster.size_id:
        size = db.query(Size).filter(Size.id == monster.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, detail="Size with this id does not exist."
            )
        attributes["size_id"] = size.id
    if monster.type_id:
        creature_type = db.query(Type).filter(Type.id == monster.type_id).first()
        if not creature_type:
            raise HTTPException(
                status_code=404, detail="Type with this id does not exist."
            )
        attributes["type_id"] = creature_type.id
    if monster.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first()
            for party in monster.parties
        ]
        for value in attributes["parties"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Party with this id does not exist."
                )
    if monster.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in monster.classes
        ]
        for value in attributes["classes"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Class with this id does not exist."
                )
    if monster.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in monster.subclasses
        ]
        for value in attributes["subclasses"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Subclass with this id does not exist."
                )
    try:
        new_monster = Monster(name=monster.name, **attributes)
        db.add(new_monster)
        db.commit()
        db.refresh(new_monster)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )

    if monster.immunities:
        for immunity in monster.immunities:
            effect = db.query(Effect).filter(Effect.id == immunity.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            monster_immunity = CreatureImmunities(
                creature_id=new_monster.id,
                effect_id=effect.id,
                condition=immunity.condition,
            )
            db.add(monster_immunity)
    if monster.resistances:
        for resistance in monster.resistances:
            effect = db.query(Effect).filter(Effect.id == resistance.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            monster_resistance = CreatureResistances(
                creature_id=new_monster.id,
                effect_id=effect.id,
                condition=resistance.condition,
            )
            db.add(monster_resistance)
    if monster.vulnerabilities:
        for vulnerability in monster.vulnerabilities:
            effect = (
                db.query(Effect).filter(Effect.id == vulnerability.effect_id).first()
            )
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            monster_vulnerability = CreatureVulnerabilities(
                creature_id=new_monster.id,
                effect_id=effect.id,
                condition=vulnerability.condition,
            )
            db.add(monster_vulnerability)
    try:
        db.commit()
        return {
            "message": f"New monster '{new_monster.name}' has been added to the database.",
            "monster": new_monster,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{monster_id}")
def put_monster(
    monster_id: str, monster: MonsterPutBase, db: Session = Depends(get_db)
):
    try:
        updated_monster = db.query(Monster).filter(Monster.id == monster_id).first()
        if monster.name:
            updated_monster.name = monster.name
        if monster.description:
            updated_monster.description = monster.description
        if monster.information:
            updated_monster.information = monster.information
        if monster.alive != None:
            updated_monster.alive = monster.alive
        if monster.active != None:
            updated_monster.active = monster.active
        if monster.armour_class:
            updated_monster.armour_class = monster.armour_class
        if monster.walking_speed:
            updated_monster.walking_speed = monster.walking_speed
        if monster.swimming_speed:
            updated_monster.swimming_speed = monster.swimming_speed
        if monster.flying_speed:
            updated_monster.flying_speed = monster.flying_speed
        if monster.image:
            updated_monster.image = monster.image
        if monster.race:
            race = db.query(Race).filter(Race.id == monster.race).first()
            if not race:
                raise HTTPException(
                    status_code=404, detail="Race with this id does not exist."
                )
            updated_monster.race = race.id
        if monster.subrace:
            subrace = db.query(Subrace).filter(Subrace.id == monster.subrace).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="Subrace with this id does not exist."
                )
            updated_monster.subrace = subrace.id
        if monster.size_id:
            size = db.query(Size).filter(Size.id == monster.size_id).first()
            if not size:
                raise HTTPException(
                    status_code=404, detail="Size with this id does not exist."
                )
            updated_monster.size_id = size.id
        if monster.type_id:
            creature_type = db.query(Type).filter(Type.id == monster.type_id).first()
            if not creature_type:
                raise HTTPException(
                    status_code=404, detail="Type with this id does not exist."
                )
            updated_monster.type_id = creature_type.id
        if monster.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first()
                for cls in monster.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="Class with this id does not exist."
                    )
            if monster.add_class:
                updated_monster.classes += classes
            else:
                for cls in classes:
                    if cls in updated_monster.classes:
                        updated_monster.classes.remove(cls)
        if monster.subclasses:
            subclasses = [
                db.query(Subclass).filter(Subclass.id == subclass).first()
                for subclass in monster.subclasses
            ]
            for subclass in subclasses:
                if subclass == None:
                    raise HTTPException(
                        status_code=404, detail="Subclass with this id does not exist."
                    )
            if monster.add_subclass:
                updated_monster.subclasses += subclasses
            else:
                for subclass in subclasses:
                    if subclass in updated_monster.subclasses:
                        updated_monster.subclasses.remove(subclass)
        if monster.parties:
            parties = [
                db.query(Party).filter(Party.id == party).first()
                for party in monster.parties
            ]
            for party in parties:
                if party == None:
                    raise HTTPException(
                        status_code=404, detail="Party with this id does not exist."
                    )
            if monster.add_parties:
                updated_monster.parties += parties
            else:
                for party in parties:
                    if party in updated_monster.parties:
                        updated_monster.parties.remove(party)
        if monster.immunities:
            for immunity in monster.immunities:
                effect = (
                    db.query(Effect).filter(Effect.id == immunity.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif immunity.add_effect:
                    new_immunity = CreatureImmunities(
                        creature_id=monster_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(CreatureImmunities)
                        .filter(
                            and_(
                                CreatureImmunities.creature_id == monster_id,
                                CreatureImmunities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if monster.resistances:
            for resistance in monster.resistances:
                effect = (
                    db.query(Effect).filter(Effect.id == resistance.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif resistance.add_effect:
                    new_resistance = CreatureResistances(
                        creature_id=monster_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(CreatureResistances)
                        .filter(
                            and_(
                                CreatureResistances.creature_id == monster_id,
                                CreatureResistances.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if monster.vulnerabilities:
            for vulnerability in monster.vulnerabilities:
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
                        creature_id=monster_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(CreatureVulnerabilities)
                        .filter(
                            and_(
                                CreatureVulnerabilities.creature_id == monster_id,
                                CreatureVulnerabilities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        db.commit()
        return {
            "message": f"Monster '{updated_monster.name}' has been updated.",
            "monster": updated_monster,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{monster_id}")
def delete_monster(monster_id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == monster_id).first()
    if not monster:
        raise HTTPException(
            status_code=404,
            detail="The monster you are trying to delete does not exist.",
        )
    db.delete(monster)
    db.commit()
    return {"message": f"Monster has been deleted."}
