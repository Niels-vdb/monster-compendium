from fastapi import APIRouter

router = APIRouter()


@router.get("api/users")
def get_users():
    return {"message": "users router"}
