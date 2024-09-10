from fastapi import APIRouter

router = APIRouter(
    prefix="/api/types",
    tags=["types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_types():
    return {"message": "types router"}
