from typing import Any, Dict

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Size(Base):
    """
    Table that holds all sizes a character can have.

    Parameters:
        - name (str): The name of the size.
    """

    __tablename__ = "sizes"

    size_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    creatures = relationship("Creature", back_populates="size")
    races = relationship("Race", back_populates="size")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Size instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.size_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Size instance.
        :rtype: Dict[str, Any]
        """
        return {"size_id": self.size_id, "size": self.name}


class Type(Base):
    """

    Parameters:
        - type (str): The name of the type
    """

    __tablename__ = "types"

    type_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    creatures = relationship("Creature", back_populates="creature_type")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Types instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.type_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Types instance.
        :rtype: Dict[str, Any]
        """
        return {"type_id": self.type_id, "type": self.name}


class Effect(Base):
    """
    Table that holds all the effects a character can have a venerability, immunity or resistance to.

    Parameters:
        - name (str): The name of the effect.
    """

    __tablename__ = "effects"

    effect_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

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
        return f"{self.__class__.__tablename__}('{self.effect_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Effect instance.
        :rtype: Dict[str, Any]
        """
        return {"effect_id": self.effect_id, "effect": self.name}
