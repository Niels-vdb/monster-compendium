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


class SizeBase(BaseModel):
    size_name: Annotated[str, Field(min_length=1)]


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
def post_size(size: SizeBase, db: Session = Depends(get_db)):
    try:
        new_size = Size(name=size.size_name)
        db.add(new_size)
        db.commit()
        db.refresh(new_size)
        return {
            "message": f"New size '{new_size.name}' has been added tot he database.",
            "size": new_size,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Size already exists.")
