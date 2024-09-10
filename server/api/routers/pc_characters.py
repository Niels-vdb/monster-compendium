from fastapi import APIRouter

router = APIRouter(
    prefix="/api/pc_characters",
    tags=["pc_characters"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_pc_characters():
    return {"message": "pc_characters router"}
