from typing import Annotated, Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db
from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.effects import Effect
from server.database.models.non_player_characters import NPCCharacter
from server.database.models.races import Race, Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/non_player_characters",
    tags=["NPC characters"],
    responses={404: {"description": "Not found."}},
)


class NPCBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    armour_class: int = None
    image: bytes = None

    race: int = None
    subrace: int = None
    size_id: int = None
    type_id: int = None

    parties: list[int] = None
    classes: list[int] = None
    subclasses: list[int] = None
    immunities: list[int] = None
    resistances: list[int] = None
    vulnerabilities: list[int] = None


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


@router.post("/")
def post_npc(npc: NPCBase, db: Session = Depends(get_db)):
    attributes: dict[str, Any] = {}

    if npc.description:
        attributes["description"] = npc.description
    if npc.information:
        attributes["information"] = npc.information
    if npc.alive:
        attributes["alive"] = npc.alive
    if npc.active:
        attributes["active"] = npc.active
    if npc.armour_class:
        attributes["armour_class"] = npc.armour_class
    if npc.image:
        attributes["image"] = npc.image
    if npc.race:
        race = db.query(Race).filter(Race.id == npc.race).first()
        if not race:
            raise HTTPException(
                status_code=404, detail="Race with this id does not exist."
            )
        attributes["race"] = race.id
    if npc.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == npc.subrace).first()
        if not subrace:
            raise HTTPException(
                status_code=404, detail="Subrace with this id does not exist."
            )
        attributes["subrace"] = subrace.id
    if npc.size_id:
        size = db.query(Size).filter(Size.id == npc.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, detail="Size with this id does not exist."
            )
        attributes["size_id"] = size.id
    if npc.type_id:
        creature_type = db.query(Type).filter(Type.id == npc.type_id).first()
        if not creature_type:
            raise HTTPException(
                status_code=404, detail="Type with this id does not exist."
            )
        attributes["type_id"] = creature_type.id
    if npc.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in npc.parties
        ]
        for value in attributes["parties"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Party with this id does not exist."
                )
    if npc.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in npc.classes
        ]
        for value in attributes["classes"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Class with this id does not exist."
                )
    if npc.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in npc.subclasses
        ]
        for value in attributes["subclasses"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Subclass with this id does not exist."
                )
    if npc.immunities:
        attributes["immunities"] = [
            db.query(Effect).filter(Effect.id == immunity).first()
            for immunity in npc.immunities
        ]
        for value in attributes["immunities"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
    if npc.resistances:
        attributes["resistances"] = [
            db.query(Effect).filter(Effect.id == resistance).first()
            for resistance in npc.resistances
        ]
        for value in attributes["resistances"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
    if npc.vulnerabilities:
        attributes["vulnerabilities"] = [
            db.query(Effect).filter(Effect.id == vulnerability).first()
            for vulnerability in npc.vulnerabilities
        ]
        for value in attributes["vulnerabilities"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
    try:
        new_npc = NPCCharacter(name=npc.name, **attributes)
        db.add(new_npc)
        db.commit()
        db.refresh(new_npc)
        return {
            "message": f"New npc '{new_npc.name}' has been added to the database.",
            "npc_character": new_npc,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )
