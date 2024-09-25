from typing import Any, Dict

from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """
    Table that holds all users that are able to log in to the application.

    Parameters:
        - name (str): The name of the user.
        - password (str): The hashes password of the user (optional).
        - image (BLOB): An image of the user (optional).
        - roles (List[Role]): The roles a user has, can be multiple.
        - parties (List[Party]): The parties a user belongs to, can be multiple (optional).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    password = Column(String(80), nullable=True)
    image = Column(BLOB, nullable=True)

    # 1-n relationships
    characters = relationship("PlayerCharacter", back_populates="user")

    # n-n relationships
    parties = relationship(
        "Party",
        secondary="user_parties",
        back_populates="users",
    )
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Role instance.
        :rtype: str
        """
        return f"""User('{self.id}', '{self.name}', '{self.username}', 
                    '{self.image}', '{self.roles}', '{self.parties}', 
                    '{self.characters}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Role instance.
        :rtype: Dict[str, Any]
        """
        return {
            "user_id": self.id,
            "name": self.name,
            "image": self.image,
            "username": self.username,
            "roles": self.roles,
            "parties": self.parties,
            "characters": self.characters,
        }


class Party(Base):
    """
    Table that holds all parties that players can belong to.

    Parameters:
        - name (str): The name of the party.
    """

    __tablename__ = "parties"

    id = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False, unique=True)

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
        return f"Party('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Party instance.
        :rtype: Dict[str, Any]
        """
        return {"party_id": self.id, "name": self.name}


class Role(Base):
    """
    Table that holds all roles that are able to be given to users using the application.

    Parameters:
        - name (str): The name of the role.
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
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Role instance.
        :rtype: str
        """
        return f"Role('{self.id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Role instance.
        :rtype: Dict[str, Any]
        """
        return {"role_id": self.id, "name": self.name}


class UserParties(Base):
    """
    Cross-reference table for many-to-many relationship between users and parties.
    """

    __tablename__ = "user_parties"

    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    party_id = Column("party_id", Integer, ForeignKey("parties.id"))


class UserRoles(Base):
    """
    Cross-reference table for many-to-many relationship between users and roles.
    """

    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    role_id = Column("role_id", Integer, ForeignKey("roles.id"))
