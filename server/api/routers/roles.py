from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db

from ...database.models.users import Role

router = APIRouter(
    prefix="/api/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    if not roles:
        raise HTTPException(status_code=404, detail="No roles found")
    return {"roles": roles}


@router.get("/{role_id}")
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"id": role.id, "name": role.name, "users": role.users}
