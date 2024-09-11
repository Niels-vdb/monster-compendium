from typing import Any, Dict

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base


class Effect(Base):
    """
    Table that holds all the effects a character can have a venerability, immunity or resistance to.

    Parameters:
        - name (str): The name of the effect.
    """

    __tablename__ = "effects"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    # Relationship references
    race_resistances = relationship(
        "Race",
        secondary="race_resistances",
        back_populates="resistances",
    )
    subrace_resistances = relationship(
        "Subrace",
        secondary="subrace_resistances",
        back_populates="resistances",
    )
    creature_resistances = relationship(
        "Creature",
        secondary="creature_resistances",
        back_populates="resistances",
    )
    creature_immunities = relationship(
        "Creature",
        secondary="creature_immunities",
        back_populates="immunities",
    )
    creature_vulnerabilities = relationship(
        "Creature",
        secondary="creature_vulnerabilities",
        back_populates="vulnerabilities",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Effect instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Effect instance.
        :rtype: Dict[str, Any]
        """
        return {"effect_id": self.id, "effect": self.name}
