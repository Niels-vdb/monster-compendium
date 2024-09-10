from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.characteristics import Type

router = APIRouter(
    prefix="/api/types",
    tags=["Types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_types(db: Session = Depends(get_db)):
    types = db.query(Type).all()
    if not types:
        raise HTTPException(status_code=404, detail="No types found")
    return {"types": types}


@router.get("/{type_id}")
def get_type(type_id: int, db: Session = Depends(get_db)):
    type = db.query(Type).filter(Type.id == type_id).first()
    if not type:
        raise HTTPException(status_code=404, detail="Type not found")
    return {"id": type.id, "name": type.name, "creatures": type.creatures}
