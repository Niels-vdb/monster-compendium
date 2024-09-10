from fastapi import APIRouter

router = APIRouter()


@router.get("api/nps_characters")
def get_nps_characters():
    return {"message": "nps_characters router"}
