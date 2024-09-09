from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Race(Base):
    """
    Table that holds all races a character can have.

    Parameters:
        - name (str): The name of the race.
        - size_id (int): FK to sizes table holding the PK of the size of this race.
    """

    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    size_id = Column(Integer, ForeignKey("sizes.size_id"), nullable=False)

    size = relationship("Size", back_populates="races")
    subraces = relationship("Subrace", back_populates="race")
    resistances = relationship(
        "Effect",
        secondary="race_resistances",
        back_populates="race_resistances",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Race instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.race_id}', '{self.name}')"

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
            "resistances": self.resistances,
        }


class Subrace(Base):
    """
    Table that holds all subraces that a race can have.

    Parameters:
        - name (str): The name of the subrace.
        - race_id (int): FK to sizes table holding the PK of the race this subrace belongs to.
    """

    __tablename__ = "subraces"

    subrace_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    race_id = Column(
        Integer,
        ForeignKey("races.race_id", ondelete="CASCADE"),
    )

    race = relationship("Race", back_populates="subraces")
    resistances = relationship(
        "Effect",
        secondary="subrace_resistances",
        back_populates="subrace_resistances",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Subrace instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.subrace_id}',
                '{self.name}', '{self.race}', '{self.resistances}')"""

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
            "race_id": self.race,
            "resistances": self.resistances,
        }


class RaceResistances(Base):
    __tablename__ = "race_resistances"

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.race_id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.effect_id"))


class SubraceResistances(Base):
    __tablename__ = "subrace_resistances"

    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.subrace_id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.effect_id"))
