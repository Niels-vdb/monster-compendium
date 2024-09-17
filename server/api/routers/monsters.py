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
from server.database.models.enemies import Enemy
from server.database.models.races import Race, Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/enemies",
    tags=["Enemies"],
    responses={404: {"description": "Not found."}},
)


class PostEffect(BaseModel):
    effect_id: int
    condition: str


class PutEffect(BaseModel):
    effect_id: int
    condition: str = None
    add_effect: bool


class EnemyPostBase(BaseModel):
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


class EnemyPutBase(BaseModel):
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
def get_enemies(db: Session = Depends(get_db)):
    enemies = db.query(Enemy).all()
    if not enemies:
        raise HTTPException(status_code=404, detail="No enemies found.")
    return {"enemies": enemies}


@router.get("/{enemy_id}")
def get_enemy(enemy_id: int, db: Session = Depends(get_db)):
    enemy = db.query(Enemy).filter(Enemy.id == enemy_id).first()
    if not enemy:
        raise HTTPException(status_code=404, detail="Enemy not found.")
    return {
        "id": enemy.id,
        "name": enemy.name,
        "description": enemy.description,
        "information": enemy.information,
        "alive": enemy.alive,
        "active": enemy.active,
        "armour_class": enemy.armour_class,
        "walking_speed": enemy.walking_speed,
        "swimming_speed": enemy.swimming_speed,
        "flying_speed": enemy.flying_speed,
        "image": enemy.image,
        "race": enemy.race,
        "subrace": enemy.subrace,
        "size": enemy.size,
        "creature_type": enemy.creature_type,
        "parties": enemy.parties,
        "classes": enemy.classes,
        "subclasses": enemy.subclasses,
        "resistances": enemy.resistances,
        "immunities": enemy.immunities,
        "vulnerabilities": enemy.vulnerabilities,
    }


@router.post("/")
def post_enemy(enemy: EnemyPostBase, db: Session = Depends(get_db)):
    attributes: dict[str, Any] = {}

    if enemy.description:
        attributes["description"] = enemy.description
    if enemy.information:
        attributes["information"] = enemy.information
    if enemy.alive:
        attributes["alive"] = enemy.alive
    if enemy.active:
        attributes["active"] = enemy.active
    if enemy.armour_class:
        attributes["armour_class"] = enemy.armour_class
    if enemy.walking_speed:
        attributes["walking_speed"] = enemy.walking_speed
    if enemy.swimming_speed:
        attributes["swimming_speed"] = enemy.swimming_speed
    if enemy.flying_speed:
        attributes["flying_speed"] = enemy.flying_speed
    if enemy.image:
        attributes["image"] = enemy.image
    if enemy.race:
        race = db.query(Race).filter(Race.id == enemy.race).first()
        if not race:
            raise HTTPException(
                status_code=404, detail="Race with this id does not exist."
            )
        attributes["race"] = race.id
    if enemy.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == enemy.subrace).first()
        if not subrace:
            raise HTTPException(
                status_code=404, detail="Subrace with this id does not exist."
            )
        attributes["subrace"] = subrace.id
    if enemy.size_id:
        size = db.query(Size).filter(Size.id == enemy.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, detail="Size with this id does not exist."
            )
        attributes["size_id"] = size.id
    if enemy.type_id:
        creature_type = db.query(Type).filter(Type.id == enemy.type_id).first()
        if not creature_type:
            raise HTTPException(
                status_code=404, detail="Type with this id does not exist."
            )
        attributes["type_id"] = creature_type.id
    if enemy.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in enemy.parties
        ]
        for value in attributes["parties"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Party with this id does not exist."
                )
    if enemy.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in enemy.classes
        ]
        for value in attributes["classes"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Class with this id does not exist."
                )
    if enemy.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in enemy.subclasses
        ]
        for value in attributes["subclasses"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Subclass with this id does not exist."
                )
    try:
        new_enemy = Enemy(name=enemy.name, **attributes)
        db.add(new_enemy)
        db.commit()
        db.refresh(new_enemy)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )

    if enemy.immunities:
        for immunity in enemy.immunities:
            effect = db.query(Effect).filter(Effect.id == immunity.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            enemy_immunity = CreatureImmunities(
                creature_id=new_enemy.id,
                effect_id=effect.id,
                condition=immunity.condition,
            )
            db.add(enemy_immunity)
    if enemy.resistances:
        for resistance in enemy.resistances:
            effect = db.query(Effect).filter(Effect.id == resistance.effect_id).first()
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            enemy_resistance = CreatureResistances(
                creature_id=new_enemy.id,
                effect_id=effect.id,
                condition=resistance.condition,
            )
            db.add(enemy_resistance)
    if enemy.vulnerabilities:
        for vulnerability in enemy.vulnerabilities:
            effect = (
                db.query(Effect).filter(Effect.id == vulnerability.effect_id).first()
            )
            if not effect:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
            enemy_vulnerability = CreatureVulnerabilities(
                creature_id=new_enemy.id,
                effect_id=effect.id,
                condition=vulnerability.condition,
            )
            db.add(enemy_vulnerability)
    try:
        db.commit()
        return {
            "message": f"New enemy '{new_enemy.name}' has been added to the database.",
            "enemy": new_enemy,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{enemy_id}")
def put_enemy(enemy_id: str, enemy: EnemyPutBase, db: Session = Depends(get_db)):
    try:
        updated_enemy = db.query(Enemy).filter(Enemy.id == enemy_id).first()
        if enemy.name:
            updated_enemy.name = enemy.name
        if enemy.description:
            updated_enemy.description = enemy.description
        if enemy.information:
            updated_enemy.information = enemy.information
        if enemy.alive != None:
            updated_enemy.alive = enemy.alive
        if enemy.active != None:
            updated_enemy.active = enemy.active
        if enemy.armour_class:
            updated_enemy.armour_class = enemy.armour_class
        if enemy.walking_speed:
            updated_enemy.walking_speed = enemy.walking_speed
        if enemy.swimming_speed:
            updated_enemy.swimming_speed = enemy.swimming_speed
        if enemy.flying_speed:
            updated_enemy.flying_speed = enemy.flying_speed
        if enemy.image:
            updated_enemy.image = enemy.image
        if enemy.race:
            race = db.query(Race).filter(Race.id == enemy.race).first()
            if not race:
                raise HTTPException(
                    status_code=404, detail="Race with this id does not exist."
                )
            updated_enemy.race = race.id
        if enemy.subrace:
            subrace = db.query(Subrace).filter(Subrace.id == enemy.subrace).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="Subrace with this id does not exist."
                )
            updated_enemy.subrace = subrace.id
        if enemy.size_id:
            size = db.query(Size).filter(Size.id == enemy.size_id).first()
            if not size:
                raise HTTPException(
                    status_code=404, detail="Size with this id does not exist."
                )
            updated_enemy.size_id = size.id
        if enemy.type_id:
            creature_type = db.query(Type).filter(Type.id == enemy.type_id).first()
            if not creature_type:
                raise HTTPException(
                    status_code=404, detail="Type with this id does not exist."
                )
            updated_enemy.type_id = creature_type.id
        if enemy.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first() for cls in enemy.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="Class with this id does not exist."
                    )
            if enemy.add_class:
                updated_enemy.classes += classes
            else:
                for cls in classes:
                    if cls in updated_enemy.classes:
                        updated_enemy.classes.remove(cls)
        if enemy.subclasses:
            subclasses = [
                db.query(Subclass).filter(Subclass.id == subclass).first()
                for subclass in enemy.subclasses
            ]
            for subclass in subclasses:
                if subclass == None:
                    raise HTTPException(
                        status_code=404, detail="Subclass with this id does not exist."
                    )
            if enemy.add_subclass:
                updated_enemy.subclasses += subclasses
            else:
                for subclass in subclasses:
                    if subclass in updated_enemy.subclasses:
                        updated_enemy.subclasses.remove(subclass)
        if enemy.parties:
            parties = [
                db.query(Party).filter(Party.id == party).first()
                for party in enemy.parties
            ]
            for party in parties:
                if party == None:
                    raise HTTPException(
                        status_code=404, detail="Party with this id does not exist."
                    )
            if enemy.add_parties:
                updated_enemy.parties += parties
            else:
                for party in parties:
                    if party in updated_enemy.parties:
                        updated_enemy.parties.remove(party)
        if enemy.immunities:
            for immunity in enemy.immunities:
                effect = (
                    db.query(Effect).filter(Effect.id == immunity.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif immunity.add_effect:
                    new_immunity = CreatureImmunities(
                        creature_id=enemy_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(CreatureImmunities)
                        .filter(
                            and_(
                                CreatureImmunities.creature_id == enemy_id,
                                CreatureImmunities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if enemy.resistances:
            for resistance in enemy.resistances:
                effect = (
                    db.query(Effect).filter(Effect.id == resistance.effect_id).first()
                )
                if not effect:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
                elif resistance.add_effect:
                    new_resistance = CreatureResistances(
                        creature_id=enemy_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(CreatureResistances)
                        .filter(
                            and_(
                                CreatureResistances.creature_id == enemy_id,
                                CreatureResistances.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if enemy.vulnerabilities:
            for vulnerability in enemy.vulnerabilities:
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
                        creature_id=enemy_id,
                        effect_id=effect.id,
                        condition=immunity.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(CreatureVulnerabilities)
                        .filter(
                            and_(
                                CreatureVulnerabilities.creature_id == enemy_id,
                                CreatureVulnerabilities.effect_id == effect.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        db.commit()
        return {
            "message": f"Enemy '{updated_enemy.name}' has been updated.",
            "enemy": updated_enemy,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{enemy_id}")
def delete_enemy(enemy_id: int, db: Session = Depends(get_db)):
    enemy = db.query(Enemy).filter(Enemy.id == enemy_id).first()
    if not enemy:
        raise HTTPException(
            status_code=404,
            detail="The enemy you are trying to delete does not exist.",
        )
    db.delete(enemy)
    db.commit()
    return {"message": f"Enemy has been deleted."}
