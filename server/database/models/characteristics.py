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

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Relationship references
    creatures = relationship("Creature", back_populates="size")
    races = relationship(
        "Race",
        secondary="race_sizes",
        back_populates="sizes",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Size instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Size instance.
        :rtype: Dict[str, Any]
        """
        return {"size_id": self.id, "size": self.name}


class Type(Base):
    """

    Parameters:
        - type (str): The name of the type
    """

    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Relationship references
    creatures = relationship("Creature", back_populates="creature_type")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Types instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Types instance.
        :rtype: Dict[str, Any]
        """
        return {"type_id": self.id, "type": self.name}
