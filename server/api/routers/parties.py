from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.users import Party

router = APIRouter(
    prefix="/api/parties",
    tags=["Parties"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_parties(db: Session = Depends(get_db)):
    parties = db.query(Party).all()
    if not parties:
        raise HTTPException(status_code=404, detail="No parties found")
    return {"parties": parties}


@router.get("/{party_id}")
def get_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(Party).filter(Party.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return {
        "id": party.id,
        "name": party.name,
        "users": party.users,
        "characters": party.characters,
    }
