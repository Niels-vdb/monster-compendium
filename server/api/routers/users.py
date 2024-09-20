from typing import Any
from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from server.api import get_db
from server.database.models.player_characters import PlayerCharacter
from server.database.models.users import Party, Role, User

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    responses={404: {"description": "Not found."}},
)


class UserPostBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    username: Annotated[str, Field(min_length=1)]
    parties: list[int] = None
    roles: list[int] = None
    characters: list[int] = None


class UserPutBase(BaseModel):
    name: str = None
    username: str = None
    parties: list[int] = None
    roles: list[int] = None
    characters: list[int] = None


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return {"users": users}


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "image": user.image,
        "parties": user.parties,
        "roles": user.roles,
        "characters": user.characters,
    }


@router.post("/")
def post_user(user: UserPostBase, db: Session = Depends(get_db)):
    try:
        attributes: dict[str, Any] = {}
        if user.parties:
            attributes["parties"] = [
                db.query(Party).filter(Party.id == party).first()
                for party in user.parties
            ]
        if user.roles:
            attributes["roles"] = [
                db.query(Role).filter(Role.id == role).first() for role in user.roles
            ]
        if user.characters:
            attributes["characters"] = [
                db.query(PlayerCharacter)
                .filter(PlayerCharacter.id == character)
                .first()
                for character in user.characters
            ]

        new_user = User(username=user.username, name=user.name, **attributes)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": f"New user '{new_user.name}' has been added to the database.",
            "user": new_user,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="User already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=404,
            detail="The party, role or character you are trying to bind to this race does not exist.",
        )


@router.put("/{user_id}")
def put_user(user_id: int, user: UserPutBase, db: Session = Depends(get_db)):
    try:
        updated_user = db.query(User).filter(User.id == user_id).first()
        if not updated_user:
            raise HTTPException(
                status_code=404,
                detail="The user you are trying to update does not exist.",
            )
        if user.name != None:
            updated_user.name = user.name
        if user.username != None:
            updated_user.username = user.username
        if user.roles != None:
            roles: list = []
            for role in user.roles:
                new_role = db.query(Role).filter(Role.id == role).first()
                if not new_role:
                    raise HTTPException(
                        status_code=404,
                        detail="The role you are trying to link to this user does not exist.",
                    )
                roles.append(new_role)
            updated_user.roles = roles
        if user.parties != None:
            parties: list = []
            for party in user.parties:
                new_party = db.query(Party).filter(Party.id == party).first()
                if not new_party:
                    raise HTTPException(
                        status_code=404,
                        detail="The party you are trying to link to this user does not exist.",
                    )
                parties.append(new_party)
            updated_user.parties = parties
        if user.characters != None:
            characters: list[PlayerCharacter] = []
            for character in user.characters:
                new_character = (
                    db.query(PlayerCharacter)
                    .filter(PlayerCharacter.id == character)
                    .first()
                )
                if not new_character:
                    raise HTTPException(
                        status_code=404,
                        detail="The character you are trying to link to this user does not exist.",
                    )
                characters.append(new_character)
            updated_user.characters = characters
        db.commit()
        return {
            "message": f"User '{updated_user.name}' has been updated.",
            "user": updated_user,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The username you are trying to use already exists."
        )


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user you are trying to delete does not exist.",
        )
    db.delete(user)
    db.commit()
    return {"message": f"User has been deleted."}
