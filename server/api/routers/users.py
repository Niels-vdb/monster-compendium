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


class UserBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    username: Annotated[str, Field(min_length=1)]
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
def post_user(user: UserBase, db: Session = Depends(get_db)):
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
            "message": f"New user '{new_user.name}' has been added tot he database.",
            "user": new_user,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="User already exists.")
    except FlushError as e:
        raise HTTPException(
            status_code=404,
            detail="The party, role or character you are trying to bind to this race does not exist.",
        )
