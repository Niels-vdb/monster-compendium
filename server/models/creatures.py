from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import CustomBase


class Creature(CustomBase):
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
        This method provides a readable string of the Enemy instance including all
        its attributes.

        :returns: A string representation of the Enemy instance.
        :rtype: str
        """

        return f"""{self.__class__.__name__}(id={self.id}, name={self.name!r}, 
            description={self.description!r}, information={self.information!r}, 
            alive={self.alive}, active={self.active}, 
            armour_class={self.armour_class}, image={self.image}, 
            race={self.race.name if self.race else 'None'}, 
            subrace={self.subrace.name if self.subrace else 'None'}, 
            size={self.size.name if self.size else 'None'}, 
            type={self.creature_type.name if self.creature_type else 'None'}, 
            parties={[party.name for party in self.parties]}, 
            classes={[cls.name for cls in self.classes]}, 
            subclasses={[subclass.name for subclass in self.subclasses]}, 
            immunities={[immunity.name for immunity in self.immunities]}, 
            resistances={[resistance.name for resistance in self.resistances]}, 
            vulnerabilities={[vul.name for vul in self.vulnerabilities]}
            )"""


class CreatureClasses(CustomBase):
    """
    Cross-reference table for many-to-many relationship between creature, class and subclass.

    Parameters:
        - creature_id: The creature itself.
        - class_id: The class of the creature.
        - subclass_id: The subclass of the creature (optional).
    """

    __tablename__ = "creature_classes"

    id = Column(Integer, primary_key=True)
    creature_id = Column(Integer, ForeignKey("creatures.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    subclass_id = Column(Integer, ForeignKey("subclasses.id"))

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureClasses instance including all
        its attributes.

        :returns: A string representation of the CreatureClasses instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id},
            class_id={self.class_id}, subclass_id={self.subclass_id})"""


class CreatureParties(CustomBase):
    """
    Cross-reference table for many-to-many relationship between creatures and parties.

    Parameters:
        - creature_id: The id of the creature.
        - party_id: The id of the party this creature encountered.
    """

    __tablename__ = "creature_parties"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    party_id = Column("party_id", Integer, ForeignKey("parties.id"))

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureParties instance including all
        its attributes.

        :returns: A string representation of the CreatureParties instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id},
            party_id={self.party_id})"""


class CreatureResistances(CustomBase):
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

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureResistances instance including all
        its attributes.

        :returns: A string representation of the CreatureResistances instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id},
            damage_type_id={self.damage_type_id}, condition={self.condition})"""


class CreatureImmunities(CustomBase):
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

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureImmunities instance including all
        its attributes.

        :returns: A string representation of the CreatureImmunities instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id}, 
            damage_type_id={self.damage_type_id}, condition={self.condition})"""


class CreatureVulnerabilities(CustomBase):
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

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureVulnerabilities instance including all
        its attributes.

        :returns: A string representation of the CreatureVulnerabilities instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id}, 
            damage_type_id={self.damage_type_id}, condition={self.condition})"""


class CreatureAdvantages(CustomBase):
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

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureAdvantages instance including all
        its attributes.

        :returns: A string representation of the CreatureAdvantages instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id}, 
            attribute_id={self.attribute_id}, condition={self.condition})"""


class CreatureDisadvantages(CustomBase):
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

    def __repr__(self) -> str:
        """
        This method provides a readable string of the CreatureDisadvantages instance including all
        its attributes.

        :returns: A string representation of the CreatureDisadvantages instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, creature_id={self.creature_id}, 
            attribute_id={self.attribute_id}, condition={self.condition})"""
