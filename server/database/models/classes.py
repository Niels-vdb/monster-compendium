from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class Class(CustomBase):
    """
    Table that holds all classes a character can have.

    Parameters:
        - name (str): The name of the class (max 50 chars).
    """

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # 1-n relationships
    subclasses = relationship(
        "Subclass",
        back_populates="parent_class",
        passive_deletes=True,
    )

    # n-n relationships
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

        return f"{self.__class__.__tablename__}(id={self.id}, name={self.name!r})"
