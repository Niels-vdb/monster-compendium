from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.characteristics import Size

router = APIRouter(
    prefix="/api/sizes",
    tags=["Sizes"],
    responses={404: {"description": "Not found."}},
)


class SizePostBase(BaseModel):
    size_name: Annotated[str, Field(min_length=1)]


class SizePutBase(BaseModel):
    size_name: str = None


@router.get("/")
def get_sizes(db: Session = Depends(get_db)):
    sizes = db.query(Size).all()
    if not sizes:
        raise HTTPException(status_code=404, detail="No sizes found.")
    return {"sizes": sizes}


@router.get("/{size_id}")
def get_size(size_id: int, db: Session = Depends(get_db)):
    size = db.query(Size).filter(Size.id == size_id).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found.")
    return {
        "id": size.id,
        "name": size.name,
        "creatures": size.creatures,
        "races": size.races,
    }


@router.post("/")
def post_size(size: SizePostBase, db: Session = Depends(get_db)):
    try:
        new_size = Size(name=size.size_name)
        db.add(new_size)
        db.commit()
        db.refresh(new_size)
        return {
            "message": f"New size '{new_size.name}' has been added to the database.",
            "size": new_size,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Size already exists.")


@router.put("/{size_id}")
def put_size(size_id: int, size: SizePutBase, db: Session = Depends(get_db)):
    try:
        updated_size = db.query(Size).filter(Size.id == size_id).first()
        if not updated_size:
            raise HTTPException(
                status_code=404,
                detail="The size you are trying to update does not exist.",
            )
        if size.size_name != None:
            updated_size.name = size.size_name
        db.commit()
        return {
            "message": f"Size '{updated_size.name}' has been updated.",
            "size": updated_size,
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="The name you are trying to use already exists."
        )


@router.delete("/{size_id}")
def delete_size(size_id: int, db: Session = Depends(get_db)):
    size = db.query(Size).filter(Size.id == size_id).first()
    if not size:
        raise HTTPException(
            status_code=404,
            detail="The size you are trying to delete does not exist.",
        )
    db.delete(size)
    db.commit()
    return {"message": f"Size has been deleted."}
