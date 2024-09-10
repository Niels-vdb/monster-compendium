from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.effects import Effect

router = APIRouter(
    prefix="/api/effects",
    tags=["effects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_effects(db: Session = Depends(get_db)):
    effects = db.query(Effect).all()
    if not effects:
        raise HTTPException(status_code=404, detail="No effects found")
    return {"effects": effects}


@router.get("/{effect_id}")
def get_effect(effect_id: int, db: Session = Depends(get_db)):
    effect = db.query(Effect).filter(Effect.id == effect_id).first()
    if not effect:
        raise HTTPException(status_code=404, detail="Effect not found")
    return {"id": effect.id, "name": effect.name}
