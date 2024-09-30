from pydantic import BaseModel


class LogoutModel(BaseModel):
    user_id: int
