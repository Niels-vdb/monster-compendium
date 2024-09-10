from fastapi import APIRouter

router = APIRouter()


@router.get("/api/effects")
def get_effects():
    return {"message": "effects router"}
