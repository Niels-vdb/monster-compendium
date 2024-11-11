from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class Party(CustomBase):
    """
    Table that holds all parties that players can belong to.

    Parameters:
        - name (str): The name of the party (max 100 chars).
    """

    __tablename__ = "parties"

    id = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False, unique=True)

    # n-n relationships
    users = relationship(
        "User",
        secondary="user_parties",
        back_populates="parties",
    )
    creatures = relationship(
        "Creature",
        secondary="creature_parties",
        back_populates="parties",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Party instance.
        :rtype: str
        """
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
