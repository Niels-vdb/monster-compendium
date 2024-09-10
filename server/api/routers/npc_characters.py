from fastapi import APIRouter

router = APIRouter()


@router.get("/api/npc_characters")
def get_npc_characters():
    return {"message": "npc_characters router"}
