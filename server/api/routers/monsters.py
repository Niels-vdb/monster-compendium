from fastapi import APIRouter

router = APIRouter(
    prefix="/api/monsters",
    tags=["monsters"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_monsters():
    return {"message": "monsters router"}
