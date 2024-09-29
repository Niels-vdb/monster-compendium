from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class User(CustomBase):
    """
    Table that holds all users that are able to log in to the application.

    Parameters:
        - name (str): The name of the user.
        - password (str): The hashes password of the user (optional).
        - image (BLOB): An image of the user (optional).
        - roles (list[Role]): The roles a user has, can be multiple.
        - parties (list[Party]): The parties a user belongs to, can be multiple (optional).
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
        This method provides a readable string of the User instance including all
        its attributes.

        :returns: A string representation of the User instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, name={self.name}, 
            username={self.username}, image={self.image}, roles={self.roles}, 
            parties={self.parties}, characters={self.characters})"""


class UserParties(CustomBase):
    """
    Cross-reference table for many-to-many relationship between users and parties.
    """

    __tablename__ = "user_parties"

    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    party_id = Column("party_id", Integer, ForeignKey("parties.id"))

    def __repr__(self) -> str:
        """
        This method provides a readable string of the UserParties instance including all
        its attributes.

        :returns: A string representation of the UserParties instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, user_id={self.user_id}, 
            party_id={self.party_id})"""


class UserRoles(CustomBase):
    """
    Cross-reference table for many-to-many relationship between users and roles.
    """

    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    role_id = Column("role_id", Integer, ForeignKey("roles.id"))

    def __repr__(self) -> str:
        """
        This method provides a readable string of the UserRoles instance including all
        its attributes.

        :returns: A string representation of the UserRoles instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, user_id={self.user_id}, 
            party_id={self.role_id})"""
