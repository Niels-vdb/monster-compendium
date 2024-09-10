from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.races import Race

router = APIRouter(
    prefix="/api/races",
    tags=["Races"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_races(db: Session = Depends(get_db)):
    races = db.query(Race).all()
    if not races:
        raise HTTPException(status_code=404, detail="No races found")
    return {"races": races}


@router.get("/{race_id}")
def get_race(race_id: int, db: Session = Depends(get_db)):
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return {
        "id": race.id,
        "name": race.name,
        "subraces": race.subraces,
        "resistances": race.resistances,
    }
