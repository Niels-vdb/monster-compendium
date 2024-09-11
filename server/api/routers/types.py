from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from server.api import get_db
from server.database.models.characteristics import Type


router = APIRouter(
    prefix="/api/types",
    tags=["Types"],
    responses={404: {"description": "Not found."}},
)


class TypeBase(BaseModel):
    type_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_types(db: Session = Depends(get_db)):
    types = db.query(Type).all()
    if not types:
        raise HTTPException(status_code=404, detail="No types found.")
    return {"types": types}


@router.get("/{type_id}")
def get_type(type_id: int, db: Session = Depends(get_db)):
    type = db.query(Type).filter(Type.id == type_id).first()
    if not type:
        raise HTTPException(status_code=404, detail="Type not found.")
    return {"id": type.id, "name": type.name, "creatures": type.creatures}


@router.post("/")
def post_type(type: TypeBase, db: Session = Depends(get_db)):
    try:
        new_type = Type(name=type.type_name)
        db.add(new_type)
        db.commit()
        db.refresh(new_type)
        return {
            "message": f"New type '{new_type.name}' has been added tot he database.",
            "type": new_type,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Type already exists.")
