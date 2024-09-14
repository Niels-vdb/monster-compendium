import re
from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.effects import Effect
from server.database.models.races import Race, Subrace

router = APIRouter(
    prefix="/api/subraces",
    tags=["Races"],
    responses={404: {"description": "Not found."}},
)


class SubracePostBase(BaseModel):
    subrace_name: Annotated[str, Field(min_length=1)]
    race_id: int
    resistances: list[int] = None


class SubracePutBase(BaseModel):
    subrace_name: str = None
    race_id: int = None
    resistances: list[int] = None


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
        resistances = [
            db.query(Effect).filter(Effect.id == effect_id).first()
            for effect_id in subrace.resistances
        ]
        new_subrace = Subrace(
            name=subrace.subrace_name, race_id=race.id, resistances=resistances
        )
        db.add(new_subrace)
        db.commit()
        db.refresh(new_subrace)
        return {
            "message": f"New subrace '{new_subrace.name}' has been added to the database.",
            "subrace": new_subrace,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Subrace already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=400,
            detail="The resistance you are trying to bind to this subrace does not exist.",
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
        if subrace.subrace_name != None:
            updated_subrace.name = subrace.subrace_name
        if subrace.race_id != None:
            race = db.query(Race).filter(Race.id == subrace.race_id).first()
            if not race:
                raise HTTPException(
                    status_code=404,
                    detail="The race you are trying to link to this subrace does not exist.",
                )
            updated_subrace.race_id = race.id
        if subrace.resistances != None:
            resistances: list = []
            for resistance in subrace.resistances:
                effect = db.query(Effect).filter(Effect.id == resistance).first()
                if not effect:
                    raise HTTPException(
                        status_code=404,
                        detail="The effect you are trying to link to this subrace does not exist.",
                    )
                resistances.append(effect)
            updated_subrace.resistances = resistances
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
