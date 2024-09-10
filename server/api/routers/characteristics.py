from fastapi import APIRouter

router = APIRouter()


@router.get("/api/characteristics")
def get_characteristics():
    return {"message": "characteristics router"}
