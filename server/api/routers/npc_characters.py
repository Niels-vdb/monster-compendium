from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.non_player_characters import NPCCharacter

router = APIRouter(
    prefix="/api/npc_characters",
    tags=["NPC characters"],
    responses={404: {"description": "Not found."}},
)


@router.get("/")
def get_npc_characters(db: Session = Depends(get_db)):
    npc_characters = db.query(NPCCharacter).all()
    if not npc_characters:
        raise HTTPException(status_code=404, detail="No NPC characters found.")
    return {"npc_characters": npc_characters}


@router.get("/{npc_character_id}")
def get_npc_character(npc_character_id: int, db: Session = Depends(get_db)):
    npc_character = (
        db.query(NPCCharacter).filter(NPCCharacter.id == npc_character_id).first()
    )
    if not npc_character:
        raise HTTPException(status_code=404, detail="NPC character not found.")
    return {
        "id": npc_character.id,
        "name": npc_character.name,
        "description": npc_character.description,
        "information": npc_character.information,
        "active": npc_character.active,
        "alive": npc_character.alive,
        "armour_class": npc_character.armour_class,
        "image": npc_character.image,
        "race": npc_character.race,
        "subrace": npc_character.subrace,
        "size": npc_character.size,
        "type": npc_character.type_id,
        "creature_type": npc_character.creature_type,
        "parties": npc_character.parties,
        "classes": npc_character.classes,
        "subclasses": npc_character.subclasses,
        "resistances": npc_character.resistances,
        "immunities": npc_character.immunities,
        "vulnerabilities": npc_character.vulnerabilities,
    }
