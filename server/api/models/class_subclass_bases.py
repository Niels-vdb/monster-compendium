from pydantic import BaseModel, ConfigDict


class ClassBase(BaseModel):
    """
    Represents a class entity.

    - `id`: Unique identifier of the class.
    - `name`: Name of the class.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SubclassBase(BaseModel):
    """
    Represents a subclass entity.

    - `id`: Unique identifier of the subclass.
    - `name`: Name of the subclass.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
