from fastapi import APIRouter

router = APIRouter()


@router.get("/api/types")
def get_types():
    return {"message": "types router"}
