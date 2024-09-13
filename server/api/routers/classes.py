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


class ClassPostBase(BaseModel):
    class_name: Annotated[str, Field(min_length=1)]


class ClassPutBase(BaseModel):
    class_name: str = None


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
def post_class(cls: ClassPostBase, db: Session = Depends(get_db)):
    try:
        new_class = Class(name=cls.class_name)
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return {
            "message": f"New class '{new_class.name}' has been added to the database.",
            "class": new_class,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Class already exists.")


@router.put("/{class_id}")
def put_race(class_id: int, cls: ClassPutBase, db: Session = Depends(get_db)):
    updated_class = db.query(Class).filter(Class.id == class_id).first()
    if not updated_class:
        raise HTTPException(
            status_code=404,
            detail="The class you are trying to update does not exist.",
        )
    if cls.class_name != None:
        updated_class.name = cls.class_name
    db.commit()
    return {
        "message": f"Class '{updated_class.name}' has been updated.",
        "race": updated_class,
    }


@router.delete("/{class_id}")
def delete_race(class_id: int, db: Session = Depends(get_db)):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(
            status_code=404,
            detail="The class you are trying to delete does not exist.",
        )
    db.delete(cls)
    db.commit()
    return {"message": "Class has been deleted."}
