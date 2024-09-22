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

        - resistances (List[DamageType]): The resistances this race has (optional).
    """

    __tablename__ = "races"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # n-n relationships
    sizes = relationship(
        "Size",
        secondary="race_sizes",
        back_populates="races",
    )
    resistances = relationship(
        "DamageType",
        secondary="race_resistances",
        back_populates="race_resistances",
    )
    immunities = relationship(
        "DamageType",
        secondary="race_immunities",
        back_populates="race_immunities",
    )
    vulnerabilities = relationship(
        "DamageType",
        secondary="race_vulnerabilities",
        back_populates="race_vulnerabilities",
    )
    advantages = relationship(
        "Attribute",
        secondary="race_advantages",
        back_populates="race_advantages",
    )
    disadvantages = relationship(
        "Attribute",
        secondary="race_disadvantages",
        back_populates="race_disadvantages",
    )

    # 1-n relationships
    subraces = relationship("Subrace", back_populates="race")
    creatures = relationship("Creature", back_populates="race")

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

    Parameters:
        - race_id: The id of the race.
        - damage_type_id: The id of the damage type
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "race_resistances"
    __table_args__ = (
        UniqueConstraint("race_id", "damage_type_id", name="_race_id_damage_type_uc"),
    )

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""RaceResistances('{self.race_id}', '{self.damage_type_id}')"""


class RaceVulnerabilities(Base):
    """
    Cross-reference table for many-to-many relationship between a race and it's vulnerabilities.

    Parameters:
        - race_id: The id of the race.
        - damage_type_id: The id of the damage type
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "race_vulnerabilities"
    __table_args__ = (
        UniqueConstraint("race_id", "damage_type_id", name="_race_id_damage_type_uc"),
    )

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""RaceVulnerabilities('{self.race_id}', '{self.damage_type_id}')"""


class RaceImmunities(Base):
    """
    Cross-reference table for many-to-many relationship between a race and it's immunities.

    Parameters:
        - race_id: The id of the race.
        - damage_type_id: The id of the damage type
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "race_immunities"
    __table_args__ = (
        UniqueConstraint("race_id", "damage_type_id", name="_race_id_damage_type_uc"),
    )

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""RaceImmunities('{self.race_id}', '{self.damage_type_id}')"""


class RaceAdvantages(Base):
    """
    Cross-reference table for many-to-many relationship between race and its advantages.

    Parameters:
        - race_id: The id of the race.
        - attribute_id: The id of the attribute
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "race_advantages"
    __table_args__ = (
        UniqueConstraint("race_id", "attribute_id", name="_race_id_attribute_uc"),
    )

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    attribute_id = Column("attribute_id", Integer, ForeignKey("attributes.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""RaceAdvantages('{self.race_id}', '{self.attribute_id}', 
        '{self.condition}')"""


class RaceDisadvantages(Base):
    """
    Cross-reference table for many-to-many relationship between race and its disadvantages.

    Parameters:
        - race_id: The id of the race.
        - attribute_id: The id of the attribute
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "race_disadvantages"
    __table_args__ = (
        UniqueConstraint("race_id", "attribute_id", name="_race_id_attribute_uc"),
    )

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    attribute_id = Column("attribute_id", Integer, ForeignKey("attributes.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""RaceDisadvantages('{self.race_id}', '{self.attribute_id}', 
        '{self.condition}')"""
