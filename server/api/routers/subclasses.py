from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.classes import Subclass


router = APIRouter(
    prefix="/api/subclasses",
    tags=["Classes"],
    responses={404: {"description": "Not found."}},
)


@router.get("/")
def get_subclasses(db: Session = Depends(get_db)):
    subclasses = db.query(Subclass).all()
    if not subclasses:
        raise HTTPException(status_code=404, detail="No subclasses found.")
    return {"subclasses": subclasses}


@router.get("/{subclass_id}")
def get_subclass(subclass_id: int, db: Session = Depends(get_db)):
    subclass = db.query(Subclass).filter(Subclass.id == subclass_id).first()
    if not subclass:
        raise HTTPException(status_code=404, detail="Subclass not found.")
    return {
        "id": subclass.id,
        "name": subclass.name,
        "classes": subclass.parent_class,
    }
