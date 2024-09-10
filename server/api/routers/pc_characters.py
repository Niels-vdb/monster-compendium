from fastapi import APIRouter

router = APIRouter()


@router.get("api/pc_characters")
def get_pc_characters():
    return {"message": "pc_characters router"}
