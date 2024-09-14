from pydantic import BaseModel, Field
from pydantic.types import Annotated

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


class RacePostBase(BaseModel):
    race_name: Annotated[str, Field(min_length=1)]
    sizes: list[int] = None
    resistances: list[int] = None


class RacePutBase(BaseModel):
    race_name: str = None
    sizes: list[int] = None
    resistances: list[int] = None


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
def post_race(race: RacePostBase, db: Session = Depends(get_db)):
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
            "message": f"New race '{race.name}' has been added to the database.",
            "race": race,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Race already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=400,
            detail="The size or resistance you are trying to bind to this race does not exist.",
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
        if race.race_name != None:
            updated_race.name = race.race_name
        if race.sizes != None:
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
        if race.resistances != None:
            resistances: list = []
            for resistance in race.resistances:
                effect = db.query(Effect).filter(Effect.id == resistance).first()
                if not effect:
                    raise HTTPException(
                        status_code=404,
                        detail="The effect you are trying to link to this subrace does not exist.",
                    )
                resistances.append(effect)
            updated_race.resistances = resistances
        db.commit()
        return {
            "message": f"Subrace '{updated_race.name}' has been updated.",
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
