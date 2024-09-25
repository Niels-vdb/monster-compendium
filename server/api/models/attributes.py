from pydantic import BaseModel


class PostAttribute(BaseModel):
    """
    Schema used for adding an attribute to a newly created creature, race or subrace.

    - `attribute_id`: The id of the attribute.
    - `condition`: Optional information for when this attribute is active.
    """

    attribute_id: int
    condition: str | None = None


class PutAttribute(BaseModel):
    """
    Schema used for updating an attribute to a creature, race or subrace.

    - `attribute_id`: The id of the attribute.
    - `add_attribute`: Boolean for adding (True) or deleting (False) the attribute.
    - `condition`: Optional information for when this attribute is active.
    """

    attribute_id: int
    add_attribute: bool
    condition: str | None = None
