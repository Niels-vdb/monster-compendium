from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db

from ...database.models.attributes import Attribute

router = APIRouter(
    prefix="/api/attributes",
    tags=["Attributes"],
    responses={404: {"description": "Not found."}},
)


class AttributePostBase(BaseModel):
    attribute_name: Annotated[str, Field(min_length=1)]


class AttributePutBase(BaseModel):
    attribute_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_attributes(db: Session = Depends(get_db)):
    attributes = db.query(Attribute).all()
    if not attributes:
        raise HTTPException(status_code=404, detail="No attributes found.")
    return {"attributes": attributes}


@router.get("/{attribute_id}")
def get_attribute(attribute_id: int, db: Session = Depends(get_db)):
    attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not attribute:
        raise HTTPException(status_code=404, detail="Damage type not found.")
    return {"id": attribute.id, "name": attribute.name}


@router.post("/")
def post_attribute(attribute: AttributePostBase, db: Session = Depends(get_db)):
    try:
        new_attribute = Attribute(name=attribute.attribute_name)
        db.add(new_attribute)
        db.commit()
        db.refresh(new_attribute)
        return {
            "message": f"New attribute '{new_attribute.name}' has been added to the database.",
            "attribute": new_attribute,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Damage type already exists.")


@router.put("/{attribute_id}")
def put_attribute(
    attribute_id: int, attribute: AttributePutBase, db: Session = Depends(get_db)
):
    try:
        updated_attribute = (
            db.query(Attribute).filter(Attribute.id == attribute_id).first()
        )
        if not updated_attribute:
            raise HTTPException(
                status_code=404,
                detail="The attribute you are trying to update does not exist.",
            )
        if attribute.attribute_name != None:
            updated_attribute.name = attribute.attribute_name
        db.commit()
        return {
            "message": f"Damage type '{updated_attribute.name}' has been updated.",
            "attribute": updated_attribute,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{attribute_id}")
def delete_attribute(attribute_id: int, db: Session = Depends(get_db)):
    attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not attribute:
        raise HTTPException(
            status_code=404,
            detail="The attribute you are trying to delete does not exist.",
        )
    db.delete(attribute)
    db.commit()
    return {"message": f"Damage type has been deleted."}
