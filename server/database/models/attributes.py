from typing import Any, Dict

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Attribute(Base):
    """
    Table that holds all the attributes a character can have a advantage or disadvantage on.
    Like a dexterity check or a magic type.

    Parameters:
        - name (str): The name of the attribute.
    """

    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Relationship references
    race_advantages = relationship(
        "Race",
        secondary="race_advantages",
        back_populates="advantages",
    )
    race_disadvantages = relationship(
        "Race",
        secondary="race_disadvantages",
        back_populates="disadvantages",
    )
    subrace_advantages = relationship(
        "Subrace",
        secondary="subrace_advantages",
        back_populates="advantages",
    )
    subrace_disadvantages = relationship(
        "Subrace",
        secondary="subrace_disadvantages",
        back_populates="disadvantages",
    )
    creature_advantages = relationship(
        "Creature",
        secondary="creature_advantages",
        back_populates="advantages",
    )
    creature_disadvantages = relationship(
        "Creature",
        secondary="creature_disadvantages",
        back_populates="disadvantages",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Attribute instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Attribute instance.
        :rtype: Dict[str, Any]
        """
        return {"effect_id": self.id, "effect": self.name}
