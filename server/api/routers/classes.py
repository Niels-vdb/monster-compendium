from fastapi import APIRouter

router = APIRouter(
    prefix="/api/classes",
    tags=["classes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_classes():
    return {"message": "classes router"}
