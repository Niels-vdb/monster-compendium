from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.races import Subrace

router = APIRouter(
    prefix="/api/subraces",
    tags=["Races"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_subraces(db: Session = Depends(get_db)):
    subraces = db.query(Subrace).all()
    if not subraces:
        raise HTTPException(status_code=404, detail="No subraces found")
    return {"subraces": subraces}


@router.get("/{subrace_id}")
def get_subrace(subrace_id: int, db: Session = Depends(get_db)):
    subrace = db.query(Subrace).filter(Subrace.id == subrace_id).first()
    if not subrace:
        raise HTTPException(status_code=404, detail="Subrace not found")
    return {
        "id": subrace.id,
        "name": subrace.name,
        "race": subrace.race,
        "resistances": subrace.resistances,
    }
