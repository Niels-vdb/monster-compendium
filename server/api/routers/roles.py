from pydantic import BaseModel, Field
from pydantic.types import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from server.api import get_db
from server.database.models.users import Role

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found."}},
)


class RolePostBase(BaseModel):
    role_name: Annotated[str, Field(min_length=1)]


class RolePutBase(BaseModel):
    role_name: str = None


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
def post_role(role: RolePostBase, db: Session = Depends(get_db)):
    try:
        new_role = Role(name=role.role_name)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return {
            "message": f"New role '{new_role.name}' has been added to the database.",
            "role": new_role,
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Role already exists.")


@router.put("/{role_id}")
def put_role(role_id: int, role: RolePutBase, db: Session = Depends(get_db)):
    updated_role = db.query(Role).filter(Role.id == role_id).first()
    if not updated_role:
        raise HTTPException(
            status_code=404,
            detail="The role you are trying to update does not exist.",
        )
    if role.role_name != None:
        updated_role.name = role.role_name
    db.commit()
    return {
        "message": f"Role '{updated_role.name}' has been updated.",
        "role": updated_role,
    }


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role you are trying to delete does not exist.",
        )
    db.delete(role)
    db.commit()
    return {"message": f"Role has been deleted."}
