from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db

from ...database.models.effects import Effect

router = APIRouter(
    prefix="/api/effects",
    tags=["Effects"],
    responses={404: {"description": "Not found."}},
)


class EffectBase(BaseModel):
    effect_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_effects(db: Session = Depends(get_db)):
    effects = db.query(Effect).all()
    if not effects:
        raise HTTPException(status_code=404, detail="No effects found.")
    return {"effects": effects}


@router.get("/{effect_id}")
def get_effect(effect_id: int, db: Session = Depends(get_db)):
    effect = db.query(Effect).filter(Effect.id == effect_id).first()
    if not effect:
        raise HTTPException(status_code=404, detail="Effect not found.")
    return {"id": effect.id, "name": effect.name}


@router.post("/")
def post_effect(effect: EffectBase, db: Session = Depends(get_db)):
    try:
        new_effect = Effect(name=effect.effect_name)
        db.add(new_effect)
        db.commit()
        db.refresh(new_effect)
        return {
            "message": f"New effect '{new_effect.name}' has been added tot he database.",
            "effect": new_effect,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Effect already exists.")
