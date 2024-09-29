from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class Size(CustomBase):
    """
    Table that holds all sizes a character can have.

    Parameters:
        - name (str): The name of the size (max 50 chars).
    """

    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # 1-n relationships
    creatures = relationship("Creature", back_populates="size")

    # n-n relationships
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
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
