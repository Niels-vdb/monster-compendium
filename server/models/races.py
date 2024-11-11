from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import CustomBase


class Race(CustomBase):
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
        This method provides a readable string of the Race instance including all
        its attributes.

        :returns: A string representation of the Race instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, name={self.name!r}
            sizes={self.sizes}, resistances={self.resistances},
            immunities={self.immunities}, vulnerabilities={self.vulnerabilities})"""


class RaceSizes(CustomBase):
    """
    Cross-reference table for many-to-many relationship between a race and it's sizes.

    Parameters:
        - race_id: The id of the race.
        - size_id: The id of the size.
    """

    __tablename__ = "race_sizes"

    id = Column(Integer, primary_key=True)
    race_id = Column("race_id", Integer, ForeignKey("races.id"))
    size_id = Column("size_id", Integer, ForeignKey("sizes.id"))

    def __repr__(self) -> str:
        """
        This method provides a readable string of the RaceSizes instance including all
        its attributes.

        :returns: A string representation of the RaceSizes instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, race_id={self.race_id},
            size_id={self.size_id})"""


class RaceResistances(CustomBase):
    """
    Cross-reference table for many-to-many relationship between a race and it's resistances.

    Parameters:
        - race_id: The id of the race.
        - damage_type_id: The id of the damage type.
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
        """
        This method provides a readable string of the RaceResistances instance including all
        its attributes.

        :returns: A string representation of the RaceResistances instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, race_id={self.race_id},
            damage_type_id={self.damage_type_id}, condition={self.condition})"""


class RaceVulnerabilities(CustomBase):
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
        """
        This method provides a readable string of the RaceVulnerabilities instance including all
        its attributes.

        :returns: A string representation of the RaceVulnerabilities instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, race_id={self.race_id}, 
            damage_type_id={self.damage_type_id}, condition={self.condition})"""


class RaceImmunities(CustomBase):
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
        """
        This method provides a readable string of the RaceImmunities instance including all
        its attributes.

        :returns: A string representation of the RaceImmunities instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, race_id={self.race_id}, 
            damage_type_id={self.damage_type_id}, condition={self.condition})"""


class RaceAdvantages(CustomBase):
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
        """
        This method provides a readable string of the RaceAdvantages instance including all
        its attributes.

        :returns: A string representation of the RaceAdvantages instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, race_id={self.race_id}, 
            attribute_id={self.attribute_id}, condition={self.condition})"""


class RaceDisadvantages(CustomBase):
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
        """
        This method provides a readable string of the RaceDisadvantages instance including all
        its attributes.

        :returns: A string representation of the RaceDisadvantages instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, race_id={self.race_id}, 
            attribute_id={self.attribute_id}, condition={self.condition})"""
