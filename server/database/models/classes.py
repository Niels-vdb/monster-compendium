from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Class(Base):
    """
    Table that holds all classes a character can have.

    Parameters:
        - name (str): The name of the class.
    """

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    # Relationship references
    subclasses = relationship(
        "Subclass",
        back_populates="parent_class",
        passive_deletes=True,
    )
    creatures = relationship(
        "Creature",
        secondary="creature_classes",
        back_populates="classes",
        overlaps="subclasses,creatures",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Class instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Class instance.
        :rtype: Dict[str, Any]
        """
        return {"class_id": self.id, "name": self.name}


class Subclass(Base):
    """
    Table that holds all subclasses that can belong to a class.

    Parameters:
        - name (str): The name of the subclass.
        - class_id (int): The class id of the class this subclass belongs to.
    """

    __tablename__ = "subclasses"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"))

    # n-1 relationships
    parent_class = relationship("Class", back_populates="subclasses")

    # Relationship references
    creatures = relationship(
        "Creature",
        secondary="creature_classes",
        back_populates="subclasses",
        overlaps="classes,creatures",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Subclass instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.id}',
                '{self.name}', '{self.class_id}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Subclass instance.
        :rtype: Dict[str, Any]
        """
        return {
            "subclass_id": self.id,
            "name": self.name,
            "class_id": self.class_id,
        }
