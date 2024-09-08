from typing import Any, Dict

from sqlalchemy import Column, Integer, String, Text

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


class Effect(Base):
    """
    Table that holds all the effects a character can have a venerability,
    immunity or resistance to.

    Parameters:
        - name (str): The name of the effect.
    """

    __tablename__ = "effects"

    effect_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

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
