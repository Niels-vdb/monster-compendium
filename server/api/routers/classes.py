from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.classes import Class


router = APIRouter(
    prefix="/api/classes",
    tags=["Classes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    if not classes:
        raise HTTPException(status_code=404, detail="No classes found")
    return {"classes": classes}


@router.get("/{class_id}")
def get_class(class_id: int, db: Session = Depends(get_db)):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"id": cls.id, "name": cls.name, "subclasses": cls.subclasses}
