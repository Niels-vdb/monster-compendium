from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.characteristics import Size

router = APIRouter(
    prefix="/api/sizes",
    tags=["Sizes"],
    responses={404: {"description": "Not found."}},
)


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
