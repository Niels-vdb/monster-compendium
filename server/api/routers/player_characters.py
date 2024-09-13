from typing import Annotated, Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db
from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.effects import Effect
from server.database.models.player_characters import PlayerCharacter
from server.database.models.races import Race, Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/player_characters",
    tags=["PC characters"],
    responses={404: {"description": "Not found."}},
)


class PCBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    amour_class: int = None
    image: bytes = None

    user_id: int
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


@router.post("/")
def post_pc(pc: PCBase, db: Session = Depends(get_db)):
    attributes: dict[str, Any] = {}

    if pc.description:
        attributes["description"] = pc.description
    if pc.information:
        attributes["information"] = pc.information
    if pc.alive:
        attributes["alive"] = pc.alive
    if pc.active:
        attributes["active"] = pc.active
    if pc.amour_class:
        attributes["amour_class"] = pc.amour_class
    if pc.image:
        attributes["image"] = pc.image
    if pc.race:
        race = db.query(Race).filter(Race.id == pc.race).first()
        if not race:
            raise HTTPException(
                status_code=404, detail="Race with this id does not exist."
            )
        attributes["race"] = race.id
    if pc.subrace:
        subrace = db.query(Subrace).filter(Subrace.id == pc.subrace).first()
        if not subrace:
            raise HTTPException(
                status_code=404, detail="Subrace with this id does not exist."
            )
        attributes["subrace"] = subrace.id
    if pc.size_id:
        size = db.query(Size).filter(Size.id == pc.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, detail="Size with this id does not exist."
            )
        attributes["size_id"] = size.id
    if pc.type_id:
        creature_type = db.query(Type).filter(Type.id == pc.type_id).first()
        if not creature_type:
            raise HTTPException(
                status_code=404, detail="Type with this id does not exist."
            )
        attributes["type_id"] = creature_type.id
    if pc.parties:
        attributes["parties"] = [
            db.query(Party).filter(Party.id == party).first() for party in pc.parties
        ]
        for value in attributes["parties"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Party with this id does not exist."
                )
    if pc.classes:
        attributes["classes"] = [
            db.query(Class).filter(Class.id == cls).first() for cls in pc.classes
        ]
        for value in attributes["classes"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Class with this id does not exist."
                )
    if pc.subclasses:
        attributes["subclasses"] = [
            db.query(Subclass).filter(Subclass.id == subclass).first()
            for subclass in pc.subclasses
        ]
        for value in attributes["subclasses"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Subclass with this id does not exist."
                )
    if pc.immunities:
        attributes["immunities"] = [
            db.query(Effect).filter(Effect.id == immunity).first()
            for immunity in pc.immunities
        ]
        for value in attributes["immunities"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
    if pc.resistances:
        attributes["resistances"] = [
            db.query(Effect).filter(Effect.id == resistance).first()
            for resistance in pc.resistances
        ]
        for value in attributes["resistances"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
    if pc.vulnerabilities:
        attributes["vulnerabilities"] = [
            db.query(Effect).filter(Effect.id == vulnerability).first()
            for vulnerability in pc.vulnerabilities
        ]
        for value in attributes["vulnerabilities"]:
            if value == None:
                raise HTTPException(
                    status_code=404, detail="Effect with this id does not exist."
                )
    try:
        new_pc = PlayerCharacter(name=pc.name, user_id=pc.user_id, **attributes)
        db.add(new_pc)
        db.commit()
        db.refresh(new_pc)
        return {
            "message": f"New pc '{new_pc.name}' has been added to the database.",
            "pc_character": new_pc,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )
