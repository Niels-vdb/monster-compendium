from fastapi import APIRouter

router = APIRouter()


@router.get("/api/classes")
def get_classes():
    return {"message": "classes router"}
