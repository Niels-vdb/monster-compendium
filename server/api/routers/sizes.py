from fastapi import APIRouter

router = APIRouter(
    prefix="/api/sizes",
    tags=["sizes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_sizes():
    return {"message": "sizes router"}
