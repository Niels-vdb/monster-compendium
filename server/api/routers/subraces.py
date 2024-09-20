import re
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
from server.database.models.attributes import Attribute
from server.database.models.damage_types import DamageType
from server.database.models.races import Race
from server.database.models.subraces import (
    Subrace,
    SubraceAdvantages,
    SubraceDisadvantages,
    SubraceImmunities,
    SubraceResistances,
    SubraceVulnerabilities,
)

router = APIRouter(
    prefix="/api/subraces",
    tags=["Races"],
    responses={404: {"description": "Not found."}},
)


class SubracePostBase(BaseModel):
    subrace_name: Annotated[str, Field(min_length=1)]
    race_id: int
    resistances: list[PostDamageType] = None
    immunities: list[PostDamageType] = None
    vulnerabilities: list[PostDamageType] = None
    advantages: list[PostAttribute] = None
    disadvantages: list[PostAttribute] = None


class SubracePutBase(BaseModel):
    subrace_name: str = None
    race_id: int = None
    resistances: list[PutDamageType] = None
    immunities: list[PutDamageType] = None
    vulnerabilities: list[PutDamageType] = None
    advantages: list[PutAttribute] = None
    disadvantages: list[PutAttribute] = None


@router.get("/")
def get_subraces(db: Session = Depends(get_db)):
    subraces = db.query(Subrace).all()
    if not subraces:
        raise HTTPException(status_code=404, detail="No subraces found.")
    return {"subraces": subraces}


@router.get("/{subrace_id}")
def get_subrace(subrace_id: int, db: Session = Depends(get_db)):
    subrace = db.query(Subrace).filter(Subrace.id == subrace_id).first()
    if not subrace:
        raise HTTPException(status_code=404, detail="Subrace not found.")
    return {
        "id": subrace.id,
        "name": subrace.name,
        "race": subrace.race,
        "resistances": subrace.resistances,
        "immunities": subrace.immunities,
        "vulnerabilities": subrace.vulnerabilities,
        "advantages": subrace.advantages,
        "disadvantages": subrace.disadvantages,
    }


@router.post("/")
def post_subrace(subrace: SubracePostBase, db: Session = Depends(get_db)):
    try:
        race = db.query(Race).filter(Race.id == subrace.race_id).first()
        if not race:
            raise HTTPException(
                status_code=404,
                detail="The race you are trying to bind to this subrace does not exist.",
            )
        new_subrace = Subrace(name=subrace.subrace_name, race_id=race.id)
        db.add(new_subrace)
        db.commit()
        db.refresh(new_subrace)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Subrace already exists.")
    try:
        if subrace.resistances:
            for resistance in subrace.resistances:
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
                subrace_resistance = SubraceResistances(
                    subrace_id=new_subrace.id, damage_type_id=damage_type.id
                )
                db.add(subrace_resistance)
        if subrace.immunities:
            for immunity in subrace.immunities:
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
                subrace_immunity = SubraceImmunities(
                    subrace_id=new_subrace.id, damage_type_id=damage_type.id
                )
                db.add(subrace_immunity)
        if subrace.vulnerabilities:
            for vulnerability in subrace.vulnerabilities:
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
                subrace_vulnerability = SubraceVulnerabilities(
                    subrace_id=new_subrace.id, damage_type_id=damage_type.id
                )
                db.add(subrace_vulnerability)
        if subrace.advantages:
            for advantage in subrace.advantages:
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
                subrace_advantage = SubraceAdvantages(
                    subrace_id=new_subrace.id, attribute_id=attribute.id
                )
                db.add(subrace_advantage)
        if subrace.disadvantages:
            for disadvantage in subrace.disadvantages:
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
                subrace_disadvantage = SubraceDisadvantages(
                    subrace_id=new_subrace.id, attribute_id=attribute.id
                )
                db.add(subrace_disadvantage)

        return {
            "message": f"New subrace '{new_subrace.name}' has been added to the database.",
            "subrace": new_subrace,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail=f"The combination of race and damage type or attribute already exists.",
        )


@router.put("/{subrace_id}")
def put_subrace(
    subrace_id: int, subrace: SubracePutBase, db: Session = Depends(get_db)
):
    try:
        updated_subrace = db.query(Subrace).filter(Subrace.id == subrace_id).first()
        if not updated_subrace:
            raise HTTPException(
                status_code=404,
                detail="The subrace you are trying to update does not exist.",
            )
        if subrace.subrace_name:
            updated_subrace.name = subrace.subrace_name
        if subrace.race_id:
            race = db.query(Race).filter(Race.id == subrace.race_id).first()
            if not race:
                raise HTTPException(
                    status_code=404,
                    detail="The race you are trying to link to this subrace does not exist.",
                )
            updated_subrace.race_id = race.id
        if subrace.immunities:
            for immunity in subrace.immunities:
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
                    new_immunity = SubraceImmunities(
                        subrace_id=subrace_id,
                        damage_type_id=damage_type.id,
                        condition=immunity.condition,
                    )
                    db.add(new_immunity)
                else:
                    old_immunity = (
                        db.query(SubraceImmunities)
                        .filter(
                            and_(
                                SubraceImmunities.subrace_id == subrace_id,
                                SubraceImmunities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_immunity)
        if subrace.resistances:
            for resistance in subrace.resistances:
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
                    new_resistance = SubraceResistances(
                        subrace_id=subrace_id,
                        damage_type_id=damage_type.id,
                        condition=resistance.condition,
                    )
                    db.add(new_resistance)
                else:
                    old_resistance = (
                        db.query(SubraceResistances)
                        .filter(
                            and_(
                                SubraceResistances.subrace_id == subrace_id,
                                SubraceResistances.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_resistance)
        if subrace.vulnerabilities:
            for vulnerability in subrace.vulnerabilities:
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
                    new_vulnerability = SubraceVulnerabilities(
                        subrace_id=subrace_id,
                        damage_type_id=damage_type.id,
                        condition=vulnerability.condition,
                    )
                    db.add(new_vulnerability)
                else:
                    old_vulnerability = (
                        db.query(SubraceVulnerabilities)
                        .filter(
                            and_(
                                SubraceVulnerabilities.subrace_id == subrace_id,
                                SubraceVulnerabilities.damage_type_id == damage_type.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_vulnerability)
        if subrace.advantages:
            for advantage in subrace.advantages:
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
                    new_advantage = SubraceAdvantages(
                        subrace_id=subrace_id,
                        attribute_id=attribute.id,
                        condition=advantage.condition,
                    )
                    db.add(new_advantage)
                else:
                    old_advantage = (
                        db.query(SubraceAdvantages)
                        .filter(
                            and_(
                                SubraceAdvantages.subrace_id == subrace_id,
                                SubraceAdvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_advantage)
        if subrace.disadvantages:
            for disadvantage in subrace.disadvantages:
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
                    new_disadvantage = SubraceDisadvantages(
                        subrace_id=subrace_id,
                        attribute_id=attribute.id,
                        condition=disadvantage.condition,
                    )
                    db.add(new_disadvantage)
                else:
                    old_disadvantage = (
                        db.query(SubraceDisadvantages)
                        .filter(
                            and_(
                                SubraceDisadvantages.subrace_id == subrace_id,
                                SubraceDisadvantages.attribute_id == attribute.id,
                            )
                        )
                        .first()
                    )
                    db.delete(old_disadvantage)

        db.commit()
        return {
            "message": f"Subrace '{updated_subrace.name}' has been updated.",
            "subrace": updated_subrace,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{subrace_id}")
def delete_subrace(subrace_id: int, db: Session = Depends(get_db)):
    subrace = db.query(Subrace).filter(Subrace.id == subrace_id).first()
    if not subrace:
        raise HTTPException(
            status_code=404,
            detail="The subrace you are trying to delete does not exist.",
        )
    db.delete(subrace)
    db.commit()
    return {"message": f"Subrace has been deleted."}
