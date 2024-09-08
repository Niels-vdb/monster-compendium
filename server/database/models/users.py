from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .base import Base


class Users(Base):
    """
    Table that holds all users that are able to log in to the application.

    Parameters:
        - name (str): The name of the user.
        - password (str): The hashes password of the user.
        - role_id (int): FK to the "roles" table holding the PK of the role given to the user.
        - party_id (int): FK to the "parties" table holding the PK of the party the user belongs to (optional).
    """

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)

    party = relationship("Parties", secondary="user_parties")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Role instance.
        :rtype: str
        """
        return (
            f"User('{self.user_id}', '{self.name}', '{self.role_id}', '{self.party}')"
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Role instance.
        :rtype: Dict[str, Any]
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role_id,
            "party": self.party,
        }


class Roles(Base):
    """
    Table that holds all roles that are able to be given to users using the application.

    Parameters:
        - name (str): The name of the role.
    """

    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    name: str = Column(String(20), nullable=False, unique=True)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Role instance.
        :rtype: str
        """
        return f"Role('{self.role_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Role instance.
        :rtype: Dict[str, Any]
        """
        return {"role_id": self.role_id, "name": self.name}


class Parties(Base):
    """
    Table that holds all parties that players can belong to.

    Parameters:
        - name (str): The name of the party.
    """

    __tablename__ = "parties"
    party_id = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Party instance.
        :rtype: str
        """
        return f"Party('{self.party_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Party instance.
        :rtype: Dict[str, Any]
        """
        return {"party_id": self.party_id, "name": self.name}


user_parties = Table(
    "user_parties",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), nullable=True),
    Column("party_id", Integer, ForeignKey("parties.party_id"), nullable=True),
)
