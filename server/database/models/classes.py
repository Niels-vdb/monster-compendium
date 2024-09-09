from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Class(Base):
    """
    Table that holds all classes a character can have.

    Parameters:
        - name (str): The name of the class.
    """

    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    subclasses = relationship(
        "Subclass", back_populates="parent_class", passive_deletes=True
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Class instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.class_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Class instance.
        :rtype: Dict[str, Any]
        """
        return {"class_id": self.class_id, "name": self.name}


class Subclass(Base):
    """
    Table that holds all subclasses that can belong to a class.

    Parameters:
        - name (str): The name of the subclass.
    """

    __tablename__ = "subclasses"

    subclass_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.class_id", ondelete="CASCADE"))

    parent_class = relationship("Class", back_populates="subclasses")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Subclass instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.subclass_id}',
                '{self.name}', '{self.class_id}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Subclass instance.
        :rtype: Dict[str, Any]
        """
        return {
            "subclass_id": self.class_id,
            "name": self.name,
            "class_id": self.class_id,
        }
