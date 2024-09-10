from fastapi import APIRouter

router = APIRouter(
    prefix="/api/races",
    tags=["races"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_races():
    return {"message": "races router"}
