from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.api.models.attributes import PostAttribute, PutAttribute
from server.api.models.damage_types import PostDamageType, PutDamageType
from server.database.models.characteristics import Size
from server.database.models.damage_types import DamageType
from server.database.models.attributes import Attribute
from server.database.models.races import (
    Race,
    RaceAdvantages,
    RaceDisadvantages,
    RaceImmunities,
    RaceResistances,
    RaceVulnerabilities,
)

router = APIRouter(
    prefix="/api/races",
    tags=["Races"],
    responses={404: {"description": "Not found."}},
)


class RacePostBase(BaseModel):
    race_name: Annotated[str, Field(min_length=1)]
    sizes: list[int]
    resistances: list[PostDamageType] = None
    immunities: list[PostDamageType] = None
    vulnerabilities: list[PostDamageType] = None
    advantages: list[PostAttribute] = None
    disadvantages: list[PostAttribute] = None


class RacePutBase(BaseModel):
    race_name: str = None
    sizes: list[int] = None
    resistances: list[PutDamageType] = None
    immunities: list[PutDamageType] = None
    vulnerabilities: list[PutDamageType] = None
    advantages: list[PutAttribute] = None
    disadvantages: list[PutAttribute] = None


@router.get("/")
def get_races(db: Session = Depends(get_db)):
    races = db.query(Race).all()
    if not races:
        raise HTTPException(status_code=404, detail="No races found.")
    return {"races": races}


@router.get("/{race_id}")
def get_race(race_id: int, db: Session = Depends(get_db)):
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found.")
    return {
        "id": race.id,
        "name": race.name,
        "sizes": race.sizes,
        "subraces": race.subraces,
        "resistances": race.resistances,
        "immunities": race.immunities,
        "vulnerabilities": race.vulnerabilities,
        "advantages": race.advantages,
        "disadvantages": race.disadvantages,
    }


@router.post("/")
def post_race(race: RacePostBase, db: Session = Depends(get_db)):
    try:
        sizes = [
            db.query(Size).filter(Size.id == size_id).first() for size_id in race.sizes
        ]
        new_race = Race(name=race.race_name, sizes=sizes)
        db.add(new_race)
        db.commit()
        db.refresh(new_race)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Race already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=400,
            detail="The size you are trying to bind to this race does not exist.",
        )
    try:
        if race.resistances:
            for resistance in race.resistances:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == resistance.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{resistance.damage_type_id}' does not exist.",
                    )
                race_resistance = RaceResistances(
                    race_id=new_race.id, damage_type_id=damage_type.id
                )
                db.add(race_resistance)
        if race.immunities:
            for immunity in race.immunities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == immunity.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{immunity.damage_type_id}' does not exist.",
                    )
                race_immunity = RaceImmunities(
                    race_id=new_race.id, damage_type_id=damage_type.id
                )
                db.add(race_immunity)
        if race.vulnerabilities:
            for vulnerability in race.vulnerabilities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == vulnerability.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Damage type with id '{vulnerability.damage_type_id}' does not exist.",
                    )
                race_vulnerability = RaceVulnerabilities(
                    race_id=new_race.id, damage_type_id=damage_type.id
                )
                db.add(race_vulnerability)
        if race.advantages:
            for advantage in race.advantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == advantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Attribute with id '{advantage.attribute_id}' does not exist.",
                    )
                race_advantage = RaceAdvantages(
                    race_id=new_race.id, attribute_id=attribute.id
                )
                db.add(race_advantage)
        if race.disadvantages:
            for disadvantage in race.disadvantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == disadvantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Attribute with id '{disadvantage.attribute_id}' does not exist.",
                    )
                race_disadvantage = RaceDisadvantages(
                    race_id=new_race.id, attribute_id=attribute.id
                )
                db.add(race_disadvantage)
        db.commit()
        return {
            "message": f"New race '{new_race.name}' has been added to the database.",
            "race": race,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail=f"The combination of race and damage type or attribute already exists.",
        )


@router.put("/{race_id}")
def put_race(race_id: int, race: RacePutBase, db: Session = Depends(get_db)):
    try:
        updated_race = db.query(Race).filter(Race.id == race_id).first()
        if not updated_race:
            raise HTTPException(
                status_code=404,
                detail="The race you are trying to update does not exist.",
            )
        if race.race_name:
            updated_race.name = race.race_name
        if race.sizes:
            sizes: list = []
            for size_id in race.sizes:
                size = db.query(Size).filter(Size.id == size_id).first()
                if not size:
                    raise HTTPException(
                        status_code=404,
                        detail="The size you are trying to link to this subrace does not exist.",
                    )
                sizes.append(size)
            updated_race.sizes = sizes
        if race.immunities:
            for immunity in race.immunities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == immunity.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif immunity.add_damage_type:
                    new_immunity = RaceImmunities(
                        race_id=race_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(RaceImmunities)
                        .filter(
                            and_(
                                RaceImmunities.race_id == race_id,
                                RaceImmunities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if race.resistances:
            for resistance in race.resistances:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == resistance.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif resistance.add_damage_type:
                    new_resistance = RaceResistances(
                        race_id=race_id,
                        damage_type_id=damage_type.id,
                        condition=resistance.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(RaceResistances)
                        .filter(
                            and_(
                                RaceResistances.race_id == race_id,
                                RaceResistances.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if race.vulnerabilities:
            for vulnerability in race.vulnerabilities:
                damage_type = (
                    db.query(DamageType)
                    .filter(DamageType.id == vulnerability.damage_type_id)
                    .first()
                )
                if not damage_type:
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif vulnerability.add_damage_type:
                    new_vulnerability = RaceVulnerabilities(
                        race_id=race_id,
                        damage_type_id=damage_type.id,
                        condition=vulnerability.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(RaceVulnerabilities)
                        .filter(
                            and_(
                                RaceVulnerabilities.race_id == race_id,
                                RaceVulnerabilities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        if race.advantages:
            for advantage in race.advantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == advantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif advantage.add_attribute:
                    new_advantage = RaceAdvantages(
                        race_id=race_id,
                        attribute_id=attribute.id,
                        condition=advantage.condition,
                    )
                    db.add(new_advantage)
                else:
                    old_advantage = (
                        db.query(RaceAdvantages)
                        .filter(
                            and_(
                                RaceAdvantages.race_id == race_id,
                                RaceAdvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_advantage)
        if race.disadvantages:
            for disadvantage in race.disadvantages:
                attribute = (
                    db.query(Attribute)
                    .filter(Attribute.id == disadvantage.attribute_id)
                    .first()
                )
                if not attribute:
                    raise HTTPException(
                        status_code=404,
                        detail="Damage type with this id does not exist.",
                    )
                elif disadvantage.add_attribute:
                    new_disadvantage = RaceDisadvantages(
                        race_id=race_id,
                        attribute_id=attribute.id,
                        condition=disadvantage.condition,
                    )
                    db.add(new_disadvantage)
                else:
                    old_disadvantage = (
                        db.query(RaceDisadvantages)
                        .filter(
                            and_(
                                RaceDisadvantages.race_id == race_id,
                                RaceDisadvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_disadvantage)

        db.commit()
        return {
            "message": f"Race '{updated_race.name}' has been updated.",
            "subrace": updated_race,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{race_id}")
def delete_race(race_id: int, db: Session = Depends(get_db)):
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(
            status_code=404,
            detail="The race you are trying to delete does not exist.",
        )
    db.delete(race)
    db.commit()
    return {"message": "Race has been deleted."}
