from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.api import get_db
from ...database.models.classes import Class
from ...database.models.classes import Subclass


router = APIRouter(
    prefix="/api/subclasses",
    tags=["Classes"],
    responses={404: {"description": "Not found."}},
)


class SubclassBase(BaseModel):
    subclass_name: Annotated[str, Field(min_length=1)]
    class_id: int


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


@router.post("/")
def post_class(subclass: SubclassBase, db: Session = Depends(get_db)):
    try:
        if not db.query(Class).filter(Class.id == subclass.class_id).first():
            raise HTTPException(
                status_code=400,
                detail="The class you are trying to add a subclass to does not exists.",
            )

        new_subclass = Subclass(name=subclass.subclass_name, class_id=subclass.class_id)
        db.add(new_subclass)
        db.commit()
        db.refresh(new_subclass)
        return {
            "message": f"New subclass '{new_subclass.name}' has been added to the database.",
            "class": new_subclass,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Subclass already exists.")
