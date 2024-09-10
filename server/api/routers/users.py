from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_users():
    return {"message": "users router"}
