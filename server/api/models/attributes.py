from pydantic import BaseModel


class PostAttribute(BaseModel):
    attribute_id: int
    condition: str = None


class PutAttribute(BaseModel):
    attribute_id: int
    condition: str = None
    add_attribute: bool
