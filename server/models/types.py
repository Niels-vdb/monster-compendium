from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class Type(CustomBase):
    """

    Parameters:
        - name (str): The name of the type (max 50 chars).
    """

    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # 1-n relationships
    creatures = relationship("Creature", back_populates="creature_type")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Type instance.
        :rtype: str
        """
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
