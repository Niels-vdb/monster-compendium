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


class PartyPostBase(BaseModel):
    party_name: Annotated[str, Field(min_length=1)]


class PartyPutBase(BaseModel):
    party_name: str = None


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
def post_party(party: PartyPostBase, db: Session = Depends(get_db)):
    try:
        new_party = Party(name=party.party_name)
        db.add(new_party)
        db.commit()
        db.refresh(new_party)
        return {
            "message": f"New party '{new_party.name}' has been added to the database.",
            "party": new_party,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Party already exists.")


@router.put("/{party_id}")
def put_party(party_id: int, party: PartyPutBase, db: Session = Depends(get_db)):
    updated_party = db.query(Party).filter(Party.id == party_id).first()
    if not updated_party:
        raise HTTPException(
            status_code=404,
            detail="The party you are trying to update does not exist.",
        )
    if party.party_name != None:
        updated_party.name = party.party_name
    db.commit()
    return {
        "message": f"Party '{updated_party.name}' has been updated.",
        "party": updated_party,
    }


@router.delete("/{party_id}")
def delete_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(Party).filter(Party.id == party_id).first()
    if not party:
        raise HTTPException(
            status_code=404,
            detail="The party you are trying to delete does not exist.",
        )
    db.delete(party)
    db.commit()
    return {"message": "Party has been deleted."}
