from pydantic import BaseModel


class DeleteResponse(BaseModel):
    """
    Response model used when delete endpoint is returned.
    """

    message: str
