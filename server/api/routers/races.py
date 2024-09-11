from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.characteristics import Size
from server.database.models.effects import Effect
from server.database.models.races import Race

router = APIRouter(
    prefix="/api/races",
    tags=["Races"],
    responses={404: {"description": "Not found."}},
)


class RaceBase(BaseModel):
    race_name: str
    sizes: list[int]
    resistances: list[int]


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
    }


@router.post("/")
def post_race(race: RaceBase, db: Session = Depends(get_db)):
    try:
        sizes = [
            db.query(Size).filter(Size.id == size_id).first() for size_id in race.sizes
        ]
        resistances = [
            db.query(Effect).filter(Effect.id == effect_id).first()
            for effect_id in race.resistances
        ]
        race = Race(name=race.race_name, sizes=sizes, resistances=resistances)
        db.add(race)
        db.commit()
        db.refresh(race)
        return {
            "message": f"New race '{race.name}' has been added tot he database.",
            "race": race,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Race already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=400,
            detail="The size or resistance you are trying to bind to this race does not exist.",
        )
