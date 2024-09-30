from typing import Annotated
from pydantic import BaseModel, Field


class LoginModel(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=50)]
    password: Annotated[str, Field(min_length=1, max_length=50)] | None
