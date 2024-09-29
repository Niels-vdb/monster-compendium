from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class Role(CustomBase):
    """
    Table that holds all roles that are able to be given to users using the application.

    Parameters:
        - name (str): The name of the role (max 50 chars).
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)

    # n-n relationships
    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the Role instance including all
        its attributes.

        :returns: A string representation of the Role instance.
        :rtype: str
        """
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
