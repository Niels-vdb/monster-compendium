from fastapi import APIRouter

router = APIRouter(
    prefix="/api/parties",
    tags=["parties"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_parties():
    return {"message": "parties router"}
