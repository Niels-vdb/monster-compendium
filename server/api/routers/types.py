from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.characteristics import Type


router = APIRouter(
    prefix="/api/types",
    tags=["Types"],
    responses={404: {"description": "Not found."}},
)


class TypePostBase(BaseModel):
    type_name: Annotated[str, Field(min_length=1)]


class TypePutBase(BaseModel):
    type_name: str = None


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
def post_type(type: TypePostBase, db: Session = Depends(get_db)):
    try:
        new_type = Type(name=type.type_name)
        db.add(new_type)
        db.commit()
        db.refresh(new_type)
        return {
            "message": f"New type '{new_type.name}' has been added to the database.",
            "type": new_type,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Type already exists.")


@router.put("/{type_id}")
def put_type(type_id: int, type: TypePutBase, db: Session = Depends(get_db)):
    updated_type = db.query(Type).filter(Type.id == type_id).first()
    if not updated_type:
        raise HTTPException(
            status_code=404,
            detail="The type you are trying to update does not exist.",
        )
    if type.type_name != None:
        updated_type.name = type.type_name
    db.commit()
    return {
        "message": f"type '{updated_type.name}' has been updated.",
        "type": updated_type,
    }


@router.delete("/{type_id}")
def delete_type(type_id: int, db: Session = Depends(get_db)):
    type = db.query(Type).filter(Type.id == type_id).first()
    if not type:
        raise HTTPException(
            status_code=404,
            detail="The type you are trying to delete does not exist.",
        )
    db.delete(type)
    db.commit()
    return {"message": f"Type has been deleted."}
