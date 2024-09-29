from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    """
    Response model for creating or retrieving an entity.

    - `message`: A descriptive message about the action performed.
    """

    message: str

    model_config = ConfigDict(from_attributes=True)
