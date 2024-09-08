from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .base import Base

# Add resistances to race as FK


class Races(Base):
    """
    Table that holds all races a character can have.

    Parameters:
        - name (str): The name of the race.
        - size_id (int): FK to sizes table holding the PK of the size of this race.
    """

    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    size_id = Column(Integer, ForeignKey("sizes.size_id"))

    subrace = relationship(
        "Subraces", back_populates="parent_race", passive_deletes=True
    )
    resistances = relationship("Effects", secondary="race_resistances")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Race instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.race_id}', 
                '{self.name}', '{self.size_id}', '{self.subrace}', 
                '{self.resistances}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Race instance.
        :rtype: Dict[str, Any]
        """
        return {
            "race_id": self.race_id,
            "name": self.name,
            "size_id": self.size_id,
            "subrace": self.subrace,
            "resistances": self.resistances,
        }


class Subraces(Base):
    """
    Table that holds all subraces that a race can have.

    Parameters:
        - name (str): The name of the subrace.
        - race_id (int): FK to sizes table holding the PK of the race this subrace belongs to.
    """

    __tablename__ = "subraces"

    subrace_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    race_id = Column(Integer, ForeignKey("races.race_id", ondelete="CASCADE"))

    resistances = relationship("Effects", secondary="subrace_resistances")

    # Define relationships
    race = relationship("Races", backref="subraces")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Subrace instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.subrace_id}', 
                '{self.name}', '{self.race_id}', '{self.resistances}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Subrace instance.
        :rtype: Dict[str, Any]
        """
        return {
            "subrace_id": self.subrace_id,
            "name": self.name,
            "race_id": self.race_id,
            "resistances": self.resistances,
        }


# Cross-reference table holding the race and its resistances.
race_resistances = Table(
    "race_resistances",
    Base.metadata,
    Column("race_id", Integer, ForeignKey("races.race_id"), nullable=False),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
)

# Cross-reference table holding the subrace and its resistances.
subrace_resistances = Table(
    "subrace_resistances",
    Base.metadata,
    Column("race_id", Integer, ForeignKey("subraces.subrace_id"), nullable=False),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
)
