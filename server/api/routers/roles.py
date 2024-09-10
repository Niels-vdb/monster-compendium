from fastapi import APIRouter

router = APIRouter()


@router.get("/api/roles")
def get_roles():
    return {"message": "roles router"}
