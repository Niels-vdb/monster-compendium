from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db

from ...database.models.damage_types import DamageType

router = APIRouter(
    prefix="/api/damage_types",
    tags=["Damage Types"],
    responses={404: {"description": "Not found."}},
)


class DamageTypePostBase(BaseModel):
    damage_type_name: Annotated[str, Field(min_length=1)]


class DamageTypePutBase(BaseModel):
    damage_type_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_damage_types(db: Session = Depends(get_db)):
    damage_types = db.query(DamageType).all()
    if not damage_types:
        raise HTTPException(status_code=404, detail="No damage_types found.")
    return {"damage_types": damage_types}


@router.get("/{damage_type_id}")
def get_damage_type(damage_type_id: int, db: Session = Depends(get_db)):
    damage_type = db.query(DamageType).filter(DamageType.id == damage_type_id).first()
    if not damage_type:
        raise HTTPException(status_code=404, detail="Damage type not found.")
    return {"id": damage_type.id, "name": damage_type.name}


@router.post("/")
def post_damage_type(damage_type: DamageTypePostBase, db: Session = Depends(get_db)):
    try:
        new_damage_type = DamageType(name=damage_type.damage_type_name)
        db.add(new_damage_type)
        db.commit()
        db.refresh(new_damage_type)
        return {
            "message": f"New damage_type '{new_damage_type.name}' has been added to the database.",
            "damage_type": new_damage_type,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Damage type already exists.")


@router.put("/{damage_type_id}")
def put_damage_type(
    damage_type_id: int, damage_type: DamageTypePutBase, db: Session = Depends(get_db)
):
    try:
        updated_damage_type = (
            db.query(DamageType).filter(DamageType.id == damage_type_id).first()
        )
        if not updated_damage_type:
            raise HTTPException(
                status_code=404,
                detail="The damage_type you are trying to update does not exist.",
            )
        if damage_type.damage_type_name != None:
            updated_damage_type.name = damage_type.damage_type_name
        db.commit()
        return {
            "message": f"Damage type '{updated_damage_type.name}' has been updated.",
            "damage_type": updated_damage_type,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{damage_type_id}")
def delete_damage_type(damage_type_id: int, db: Session = Depends(get_db)):
    damage_type = db.query(DamageType).filter(DamageType.id == damage_type_id).first()
    if not damage_type:
        raise HTTPException(
            status_code=404,
            detail="The damage_type you are trying to delete does not exist.",
        )
    db.delete(damage_type)
    db.commit()
    return {"message": f"Damage type has been deleted."}
