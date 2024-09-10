from fastapi import APIRouter

router = APIRouter()


@router.get("/api/parties")
def get_parties():
    return {"message": "parties router"}
