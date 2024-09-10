from fastapi import APIRouter

router = APIRouter()


@router.get("/api/sizes")
def get_sizes():
    return {"message": "sizes router"}
