from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


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
    name = Column(String(50), nullable=False)
    race_id = Column(
        Integer,
        ForeignKey("races.id", ondelete="CASCADE"),
    )
    # 1-n relationships
    creatures = relationship("Creature", back_populates="subrace")

    # n-1 relationships
    race = relationship("Race", back_populates="subraces")

    # n-n relationships
    resistances = relationship(
        "DamageType",
        secondary="subrace_resistances",
        back_populates="subrace_resistances",
    )
    immunities = relationship(
        "DamageType",
        secondary="subrace_immunities",
        back_populates="subrace_immunities",
    )
    vulnerabilities = relationship(
        "DamageType",
        secondary="subrace_vulnerabilities",
        back_populates="subrace_vulnerabilities",
    )
    advantages = relationship(
        "Attribute",
        secondary="subrace_advantages",
        back_populates="subrace_advantages",
    )
    disadvantages = relationship(
        "Attribute",
        secondary="subrace_disadvantages",
        back_populates="subrace_disadvantages",
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


class SubraceResistances(Base):
    """
    Cross-reference table for many-to-many relationship between a subrace and it's resistances.
    """

    __tablename__ = "subrace_resistances"
    __table_args__ = (
        UniqueConstraint(
            "subrace_id", "damage_type_id", name="_subrace_id_damage_type_uc"
        ),
    )

    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""SubraceVulnerabilities('{self.subrace_id}', '{self.damage_type_id}', 
                '{self.condition}')"""


class SubraceVulnerabilities(Base):
    """
    Cross-reference table for many-to-many relationship between a subrace and it's vulnerabilities.

    Parameters:
        - subrace_id: The id of the subrace.
        - damage_type_id: The id of the damage type
    """

    __tablename__ = "subrace_vulnerabilities"
    __table_args__ = (
        UniqueConstraint(
            "subrace_id", "damage_type_id", name="_subrace_id_damage_type_uc"
        ),
    )
    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""SubraceVulnerabilities('{self.subrace_id}', '{self.damage_type_id}', 
                '{self.condition}')"""


class SubraceImmunities(Base):
    """
    Cross-reference table for many-to-many relationship between a subrace and it's immunities.

    Parameters:
        - subrace_id: The id of the subrace.
        - damage_type_id: The id of the damage type
    """

    __tablename__ = "subrace_immunities"
    __table_args__ = (
        UniqueConstraint(
            "subrace_id", "damage_type_id", name="_subrace_id_damage_type_uc"
        ),
    )
    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""SubraceImmunities('{self.subrace_id}', '{self.damage_type_id}', 
                '{self.condition}')"""


class SubraceAdvantages(Base):
    """
    Cross-reference table for many-to-many relationship between subrace and its advantages.

    Parameters:
        - subrace_id: The id of the subrace.
        - attribute_id: The id of the attribute
        - attribute: The attribute when this vulnerability is active (optional).
    """

    __tablename__ = "subrace_advantages"
    __table_args__ = (
        UniqueConstraint("subrace_id", "attribute_id", name="_subrace_id_attribute_uc"),
    )

    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.id"))
    attribute_id = Column("attribute_id", Integer, ForeignKey("attributes.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""SubraceAdvantages('{self.subrace_id}', '{self.attribute_id}', 
                '{self.condition}')"""


class SubraceDisadvantages(Base):
    """
    Cross-reference table for many-to-many relationship between subrace and its disadvantages.

    Parameters:
        - subrace_id: The id of the subrace.
        - attribute_id: The id of the attribute
        - attribute: The attribute when this vulnerability is active (optional).
    """

    __tablename__ = "subrace_disadvantages"
    __table_args__ = (
        UniqueConstraint("subrace_id", "attribute_id", name="_subrace_id_attribute_uc"),
    )

    id = Column(Integer, primary_key=True)
    subrace_id = Column("subrace_id", Integer, ForeignKey("subraces.id"))
    attribute_id = Column("attribute_id", Integer, ForeignKey("attributes.id"))
    condition = Column("condition", String(100))

    def __repr__(self) -> str:
        return f"""SubraceDisadvantages('{self.subrace_id}', '{self.attribute_id}', 
                '{self.condition}')"""
