from fastapi import APIRouter

router = APIRouter(
    prefix="/api/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_roles():
    return {"message": "roles router"}
