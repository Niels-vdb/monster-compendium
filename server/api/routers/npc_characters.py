from fastapi import APIRouter

router = APIRouter(
    prefix="/api/npc_characters",
    tags=["npc_characters"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_npc_characters():
    return {"message": "npc_characters router"}
