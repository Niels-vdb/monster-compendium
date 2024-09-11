from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.api import get_db
from ...database.models.classes import Class


router = APIRouter(
    prefix="/api/classes",
    tags=["Classes"],
    responses={404: {"description": "Not found."}},
)


class ClassBase(BaseModel):
    class_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    if not classes:
        raise HTTPException(status_code=404, detail="No classes found.")
    return {"classes": classes}


@router.get("/{class_id}")
def get_class(class_id: int, db: Session = Depends(get_db)):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found.")
    return {"id": cls.id, "name": cls.name, "subclasses": cls.subclasses}


@router.post("/")
def post_class(cls: ClassBase, db: Session = Depends(get_db)):
    try:
        new_class = Class(name=cls.class_name)
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return {
            "message": f"New class '{new_class.name}' has been added tot he database.",
            "class": new_class,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Class already exists.")
