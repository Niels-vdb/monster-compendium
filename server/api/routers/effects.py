from fastapi import APIRouter

router = APIRouter(
    prefix="/api/effects",
    tags=["effects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_effects():
    return {"message": "effects router"}
