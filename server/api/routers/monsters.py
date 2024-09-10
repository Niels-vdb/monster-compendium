from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.monsters import Monster

router = APIRouter(
    prefix="/api/monsters",
    tags=["monsters"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_monsters(db: Session = Depends(get_db)):
    monsters = db.query(Monster).all()
    if not monsters:
        raise HTTPException(status_code=404, detail="No monsters found")
    return {"monsters": monsters}


@router.get("/{monster_id}")
def get_monster(monster_id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == monster_id).first()
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    return {
        "id": monster.id,
        "name": monster.name,
        "active": monster.active,
        "alive": monster.alive,
        "armour_class": monster.armour_class,
        "classes": monster.classes,
        "subclasses": monster.subclasses,
        "race": monster.race,
        "subrace": monster.subrace,
        "creature_type": monster.creature_type,
        "description": monster.description,
        "information": monster.information,
        "size": monster.size,
        "resistances": monster.resistances,
        "immunities": monster.immunities,
        "vulnerabilities": monster.vulnerabilities,
        "image": monster.image,
    }
