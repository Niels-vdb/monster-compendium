from typing import Annotated, Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.characteristics import Size, Type
from server.database.models.classes import Class, Subclass
from server.database.models.effects import Effect
from server.database.models.player_characters import PlayerCharacter
from server.database.models.races import Race, Subrace
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/player_characters",
    tags=["Player Characters"],
    responses={404: {"description": "Not found."}},
)


class PCBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: str = None
    information: str = None
    alive: bool = None
    active: bool = None
    armour_class: int = None
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


class PCPutBase(BaseModel):
    name: str = None
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

    classes: list[int] = None
    add_class: bool = None
    subclasses: list[int] = None
    add_subclass: bool = None
    parties: list[int] = None
    add_parties: bool = None
    immunities: list[int] = None
    add_immunities: bool = None
    resistances: list[int] = None
    add_resistances: bool = None
    vulnerabilities: list[int] = None
    add_vulnerabilities: bool = None


@router.get("/")
def get_pc_characters(db: Session = Depends(get_db)):
    pc_characters = db.query(PlayerCharacter).all()
    if not pc_characters:
        raise HTTPException(status_code=404, detail="No player characters found.")
    return {"player_characters": pc_characters}


@router.get("/{pc_id}")
def get_pc(pc_id: int, db: Session = Depends(get_db)):
    pc = db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_id).first()
    if not pc:
        raise HTTPException(status_code=404, detail="Player character not found.")
    return {
        "id": pc.id,
        "name": pc.name,
        "description": pc.description,
        "information": pc.information,
        "alive": pc.alive,
        "active": pc.active,
        "armour_class": pc.armour_class,
        "image": pc.image,
        "race": pc.race,
        "subrace": pc.subrace,
        "size": pc.size,
        "creature_type": pc.creature_type,
        "user": pc.user,
        "parties": pc.parties,
        "classes": pc.classes,
        "subclasses": pc.subclasses,
        "resistances": pc.resistances,
        "immunities": pc.immunities,
        "vulnerabilities": pc.vulnerabilities,
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
    if pc.armour_class:
        attributes["armour_class"] = pc.armour_class
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
            "message": f"New player character '{new_pc.name}' has been added to the database.",
            "player_character": new_pc,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An unexpected error occurred. Error: {str(e)}"
        )


@router.put("/{pc_id}")
def post_pc(pc_id: str, pc: PCPutBase, db: Session = Depends(get_db)):
    try:
        updated_pc = (
            db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_id).first()
        )
        if pc.name:
            updated_pc.name = pc.name
        if pc.description:
            updated_pc.description = pc.description
        if pc.information:
            updated_pc.information = pc.information
        if pc.alive != None:
            updated_pc.alive = pc.alive
        if pc.active != None:
            updated_pc.active = pc.active
        if pc.armour_class:
            updated_pc.armour_class = pc.armour_class
        if pc.image:
            updated_pc.image = pc.image
        if pc.race:
            race = db.query(Race).filter(Race.id == pc.race).first()
            if not race:
                raise HTTPException(
                    status_code=404, detail="Race with this id does not exist."
                )
            updated_pc.race = race.id
        if pc.subrace:
            subrace = db.query(Subrace).filter(Subrace.id == pc.subrace).first()
            if not subrace:
                raise HTTPException(
                    status_code=404, detail="Subrace with this id does not exist."
                )
            updated_pc.subrace = subrace.id
        if pc.size_id:
            size = db.query(Size).filter(Size.id == pc.size_id).first()
            if not size:
                raise HTTPException(
                    status_code=404, detail="Size with this id does not exist."
                )
            updated_pc.size_id = size.id
        if pc.type_id:
            creature_type = db.query(Type).filter(Type.id == pc.type_id).first()
            if not creature_type:
                raise HTTPException(
                    status_code=404, detail="Type with this id does not exist."
                )
            updated_pc.type_id = creature_type.id
        if pc.classes:
            classes = [
                db.query(Class).filter(Class.id == cls).first() for cls in pc.classes
            ]
            for cls in classes:
                if cls == None:
                    raise HTTPException(
                        status_code=404, detail="Class with this id does not exist."
                    )
            if pc.add_class:
                updated_pc.classes += classes
            else:
                for cls in classes:
                    if cls in updated_pc.classes:
                        updated_pc.classes.remove(cls)
        if pc.subclasses:
            subclasses = [
                db.query(Subclass).filter(Subclass.id == subclass).first()
                for subclass in pc.subclasses
            ]
            for subclass in subclasses:
                if subclass == None:
                    raise HTTPException(
                        status_code=404, detail="Subclass with this id does not exist."
                    )
            if pc.add_subclass:
                updated_pc.subclasses += subclasses
            else:
                for subclass in subclasses:
                    if subclass in updated_pc.subclasses:
                        updated_pc.subclasses.remove(subclass)
        if pc.parties:
            parties = [
                db.query(Party).filter(Party.id == party).first()
                for party in pc.parties
            ]
            for party in parties:
                if party == None:
                    raise HTTPException(
                        status_code=404, detail="Party with this id does not exist."
                    )
            if pc.add_parties:
                updated_pc.parties += parties
            else:
                for party in parties:
                    if party in updated_pc.parties:
                        updated_pc.parties.remove(party)
        if pc.immunities:
            immunities = [
                db.query(Effect).filter(Effect.id == immunity).first()
                for immunity in pc.immunities
            ]
            for immunity in immunities:
                if immunity == None:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
            if pc.add_immunities:
                updated_pc.immunities += immunities
            else:
                for immunity in immunities:
                    if immunity in updated_pc.immunities:
                        updated_pc.immunities.remove(immunity)
        if pc.resistances:
            resistances = [
                db.query(Effect).filter(Effect.id == resistance).first()
                for resistance in pc.resistances
            ]
            for resistance in resistances:
                if resistance == None:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
            if pc.add_resistances:
                updated_pc.resistances += resistances
            else:
                for resistance in resistances:
                    if resistance in updated_pc.resistances:
                        updated_pc.resistances.remove(resistance)
        if pc.vulnerabilities:
            vulnerabilities = [
                db.query(Effect).filter(Effect.id == vulnerability).first()
                for vulnerability in pc.vulnerabilities
            ]
            for vulnerability in vulnerabilities:
                if vulnerability == None:
                    raise HTTPException(
                        status_code=404, detail="Effect with this id does not exist."
                    )
            if pc.add_vulnerabilities:
                updated_pc.vulnerabilities += vulnerabilities
            else:
                for vulnerability in vulnerabilities:
                    if vulnerability in updated_pc.vulnerabilities:
                        updated_pc.vulnerabilities.remove(vulnerability)
        db.commit()
        return {
            "message": f"Player character '{updated_pc.name}' has been updated.",
            "player_character": updated_pc,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{pc_id}")
def delete_pc(pc_id: int, db: Session = Depends(get_db)):
    pc = db.query(PlayerCharacter).filter(PlayerCharacter.id == pc_id).first()
    if not pc:
        raise HTTPException(
            status_code=404,
            detail="The player character you are trying to delete does not exist.",
        )
    db.delete(pc)
    db.commit()
    return {"message": f"Player character has been deleted."}
