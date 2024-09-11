from pydantic import BaseModel

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


class SubraceBase(BaseModel):
    subrace_name: str
    race_id: int
    resistances: list[int]


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
def post_subrace(subrace: SubraceBase, db: Session = Depends(get_db)):
    try:
        race = db.query(Race).filter(Race.id == subrace.race_id).first()
        resistances = [
            db.query(Effect).filter(Effect.id == effect_id).first()
            for effect_id in subrace.resistances
        ]
        subrace = Subrace(
            name=subrace.subrace_name, race_id=race.id, resistances=resistances
        )
        db.add(subrace)
        db.commit()
        db.refresh(subrace)
        return {
            "message": f"New subrace '{subrace.name}' has been added tot he database.",
            "subrace": subrace,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Subrace already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=400,
            detail="The resistance you are trying to bind to this subrace does not exist.",
        )
    except AttributeError as e:
        raise HTTPException(
            status_code=400,
            detail="The class you are trying to bind to this subrace does not exist.",
        )
