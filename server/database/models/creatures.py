from typing import Any
from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Creature(Base):
    """
    Base table all creature types inherit from.

    Parameters:
        - name (str): The name of the monster.
        - description (str): Description about how the monster looks like (optional).
        - information (str): Notes and extra information about the monster (optional).
        - alive (bool): Boolean check if monster is alive (True), or dead (False).
        - active (bool): Boolean check if the monster is visible for party (True) or not (False).
        - armour_class (int): The armour class the monster has (optional).
        - image (BLOB): An image of the monster (optional).

        - race (int): The race of the creature, FK to id of the races table (optional).
        - subrace (int): The race of the creature, FK to id of the subraces table (optional).
        - size_id (int): The size of the creature, FK to id of the sizes table.
        - type_id (int): The type of the creature, FK to id of the types table (optional).

        - parties (List[Party]): The party(s) this creature belongs to. Linked to actual model, can be multiple (optional).
        - classes (List[Class]): The classes the creature belongs to, can be multiple (optional).
        - immunities (List[Effect]): The conditions the creature is immune to, can be multiple (optional).
        - resistances (List[Effect]): The conditions the creature is resistance to, can be multiple (optional).
        - vulnerabilities (List[Effect]): The conditions the creature is vulnerable to, can be multiple (optional).
    """

    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False, default=True)
    active = Column(Boolean, nullable=False, default=True)
    armour_class = Column(Integer, nullable=True)
    walking_speed = Column(Integer, nullable=True)
    swimming_speed = Column(Integer, nullable=True)
    flying_speed = Column(Integer, nullable=True)
    climbing_speed = Column(Integer, nullable=True)
    image = Column(BLOB, nullable=True)

    # n-1 relationships
    race_id = Column(Integer, ForeignKey("races.id"), nullable=True)
    subrace_id = Column(Integer, ForeignKey("subraces.id"), nullable=True)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=True)
    size_id = Column(Integer, ForeignKey("sizes.id"), nullable=True)

    # n-n relationships
    parties = relationship(
        "Party",
        secondary="creature_parties",
        back_populates="creatures",
    )
    classes = relationship(
        "Class",
        secondary="creature_classes",
        back_populates="creatures",
        overlaps="subclasses",
    )
    subclasses = relationship(
        "Subclass",
        secondary="creature_classes",
        back_populates="creatures",
        overlaps="classes",
    )
    immunities = relationship("DamageType", secondary="creature_immunities")
    resistances = relationship("DamageType", secondary="creature_resistances")
    vulnerabilities = relationship("DamageType", secondary="creature_vulnerabilities")
    advantages = relationship("Attribute", secondary="creature_advantages")
    disadvantages = relationship("Attribute", secondary="creature_disadvantages")

    # Relationship references
    race = relationship("Race", back_populates="creatures")
    subrace = relationship("Subrace", back_populates="creatures")
    creature_type = relationship("Type", back_populates="creatures")
    size = relationship("Size", back_populates="creatures")

    # Polymorph variable
    creature = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "creatures",
        "polymorphic_on": creature,
    }

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the enemy instance.
        :rtype: str
        """

        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, name={self.name!r}, "
            f"description={self.description!r}, information={self.information!r}, "
            f"alive={self.alive}, active={self.active}, "
            f"armour_class={self.armour_class}, image={self.image}, "
            # f"race={self.race.name if self.race else 'None'}, "
            # f"subrace={self.subrace.name if self.subrace else 'None'}, "
            # f"size={self.size.name if self.size else 'None'}, "
            # f"type={self.creature_type.name if self.creature_type else 'None'}, "
            f"parties={[party.name for party in self.parties]}, "
            f"classes={[cls.name for cls in self.classes]}, "
            f"subclasses={[subclass.name for subclass in self.subclasses]}, "
            f"immunities={[immunity.name for immunity in self.immunities]}, "
            f"resistances={[resistance.name for resistance in self.resistances]}, "
            f"vulnerabilities={[vul.name for vul in self.vulnerabilities]}"
            ")"
        )

    def to_dict(self) -> dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the enemy instance.
        :rtype: Dict[str, Any]
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "race": self.race,
            "subrace": self.subrace,
            "size": self.size,
            "type": self.type_id,
            "parties": self.parties,
            "classes": [cls.to_dict() for cls in self.classes],
            "subclasses": [subcls.to_dict() for subcls in self.subclasses],
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }


class CreatureClasses(Base):
    """
    Cross-reference table for many-to-many relationship between creature, class and subclass.
    """

    __tablename__ = "creature_classes"

    id = Column(Integer, primary_key=True)
    creature_id = Column(Integer, ForeignKey("creatures.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    subclass_id = Column(Integer, ForeignKey("subclasses.id"))


class CreatureParties(Base):
    """
    Cross-reference table for many-to-many relationship between creatures and parties.
    """

    __tablename__ = "creature_parties"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    party_id = Column("party_id", Integer, ForeignKey("parties.id"))


class CreatureResistances(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its resistances.

    Parameters:
        - creature_id: The id of the creature.
        - damage_type_id: The id of the condition
        - condition: The condition when this resistance is active (optional).
    """

    __tablename__ = "creature_resistances"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))


class CreatureImmunities(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its immunities.

    Parameters:
        - creature_id: The id of the creature.
        - damage_type_id: The id of the condition
        - condition: The condition when this immunity is active (optional).
    """

    __tablename__ = "creature_immunities"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))


class CreatureVulnerabilities(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its vulnerabilities.

    Parameters:
        - creature_id: The id of the creature.
        - damage_type_id: The id of the condition
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "creature_vulnerabilities"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    damage_type_id = Column("damage_type_id", Integer, ForeignKey("damage_types.id"))
    condition = Column("condition", String(100))


class CreatureAdvantages(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its advantages.

    Parameters:
        - creature_id: The id of the creature.
        - attribute_id: The id of the attribute
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "creature_advantages"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    attribute_id = Column("attribute_id", Integer, ForeignKey("attributes.id"))
    condition = Column("condition", String(100))


class CreatureDisadvantages(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its disadvantages.

    Parameters:
        - creature_id: The id of the creature.
        - attribute_id: The id of the attribute
        - condition: The condition when this vulnerability is active (optional).
    """

    __tablename__ = "creature_disadvantages"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    attribute_id = Column("attribute_id", Integer, ForeignKey("attributes.id"))
    condition = Column("condition", String(100))
