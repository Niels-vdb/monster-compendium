from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from ...database.models.users import Role

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found."}},
)


class RoleBase(BaseModel):
    role_name: Annotated[str, Field(min_length=1)]


@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    if not roles:
        raise HTTPException(status_code=404, detail="No roles found.")
    return {"roles": roles}


@router.get("/{role_id}")
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found.")
    return {"id": role.id, "name": role.name, "users": role.users}


@router.post("/")
def post_role(role: RoleBase, db: Session = Depends(get_db)):
    try:
        role = Role(name=role.role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
        return {
            "message": f"New role '{role.name}' has been added tot he database.",
            "role": role,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Role already exists.")
