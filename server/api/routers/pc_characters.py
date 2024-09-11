from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.player_characters import PlayerCharacter

router = APIRouter(
    prefix="/api/pc_characters",
    tags=["PC characters"],
    responses={404: {"description": "Not found."}},
)


@router.get("/")
def get_pc_characters(db: Session = Depends(get_db)):
    pc_characters = db.query(PlayerCharacter).all()
    if not pc_characters:
        raise HTTPException(status_code=404, detail="No PC characters found.")
    return {"pc_characters": pc_characters}


@router.get("/{pc_character_id}")
def get_pc_character(pc_character_id: int, db: Session = Depends(get_db)):
    pc_character = (
        db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_character_id).first()
    )
    if not pc_character:
        raise HTTPException(status_code=404, detail="PC character not found.")
    return {
        "id": pc_character.id,
        "name": pc_character.name,
        "description": pc_character.description,
        "information": pc_character.information,
        "alive": pc_character.alive,
        "active": pc_character.active,
        "armour_class": pc_character.armour_class,
        "image": pc_character.image,
        "race": pc_character.race,
        "subrace": pc_character.subrace,
        "size": pc_character.size,
        "creature_type": pc_character.creature_type,
        "user": pc_character.user,
        "parties": pc_character.parties,
        "classes": pc_character.classes,
        "subclasses": pc_character.subclasses,
        "resistances": pc_character.resistances,
        "immunities": pc_character.immunities,
        "vulnerabilities": pc_character.vulnerabilities,
    }
