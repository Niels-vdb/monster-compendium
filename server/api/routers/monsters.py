from fastapi import APIRouter

router = APIRouter()


@router.get("api/monsters")
def get_monsters():
    return {"message": "monsters router"}
