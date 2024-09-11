from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Race(Base):
    """
    Table that holds all races a character can have.

    Parameters:
        - name (str): The name of the race.
        - size_id (int): FK to sizes table holding the PK of the size of this race.

        - resistances (List[Effect]): The resistances this race has (optional).
    """

    __tablename__ = "races"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    # n-n relationships
    sizes = relationship(
        "Size",
        secondary="race_sizes",
        back_populates="races",
    )
    resistances = relationship(
        "Effect",
        secondary="race_resistances",
        back_populates="race_resistances",
    )

    # Relationships
    subraces = relationship("Subrace", back_populates="race")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Race instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.id}',
                '{self.name}', '{self.sizes}', '{self.resistances}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Race instance.
        :rtype: Dict[str, Any]
        """
        return {
            "race_id": self.id,
            "name": self.name,
            "size": self.sizes,
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
    __table_args__ = (UniqueConstraint("name", "race_id", name="_name_race_id_uc"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    race_id = Column(
        Integer,
        ForeignKey("races.id", ondelete="CASCADE"),
    )

    # n-1 relationships
    race = relationship("Race", back_populates="subraces")

    # n-n relationships
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
        return f"""{self.__class__.__tablename__}('{self.id}',
                '{self.name}', '{self.race}', '{self.resistances}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Subrace instance.
        :rtype: Dict[str, Any]
        """
        return {
            "subrace_id": self.id,
            "name": self.name,
            "race_id": self.race,
            "resistances": self.resistances,
        }


class RaceSizes(Base):
    """
    Cross-reference table for many-to-many relationship between a race and it's sizes.
    """

    __tablename__ = "race_sizes"

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    size_id = Column("size_id", Integer, ForeignKey("sizes.id"))


class RaceResistances(Base):
    """
    Cross-reference table for many-to-many relationship between a race and it's resistances.
    """

    __tablename__ = "race_resistances"

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.id"))


class SubraceResistances(Base):
    """
    Cross-reference table for many-to-many relationship between a subrace and it's resistances.
    """

    __tablename__ = "subrace_resistances"

    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.id"))
