from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.users import Party

router = APIRouter(
    prefix="/api/parties",
    tags=["Parties"],
    responses={404: {"description": "Not found."}},
)


class PartyBase(BaseModel):
    party_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_parties(db: Session = Depends(get_db)):
    parties = db.query(Party).all()
    if not parties:
        raise HTTPException(status_code=404, detail="No parties found.")
    return {"parties": parties}


@router.get("/{party_id}")
def get_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(Party).filter(Party.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found.")
    return {
        "id": party.id,
        "name": party.name,
        "users": party.users,
        "creatures": party.creatures,
    }


@router.post("/")
def post_party(party: PartyBase, db: Session = Depends(get_db)):
    try:
        new_party = Party(name=party.party_name)
        db.add(new_party)
        db.commit()
        db.refresh(new_party)
        return {
            "message": f"New party '{new_party.name}' has been added tot he database.",
            "party": new_party,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Party already exists.")
