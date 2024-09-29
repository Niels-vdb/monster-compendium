from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class Attribute(CustomBase):
    """
    Table that holds all the attributes a character can have a advantage or disadvantage on.
    Like a dexterity check or a magic type.

    Parameters:
        - name (str): The name of the attribute (max 50 chars).
    """

    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # n-n relationships
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
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
