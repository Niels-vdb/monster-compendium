from fastapi import APIRouter

router = APIRouter()


@router.get("api/races")
def get_races():
    return {"message": "races router"}
