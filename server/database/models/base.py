from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Creature(Base):
    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False, default=True)
    active = Column(Boolean, nullable=False, default=True)
    armour_class = Column(Integer, nullable=True)
    image = Column(BLOB, nullable=True)

    # 1-n
    race = Column(Integer, ForeignKey("races.race_id"), nullable=True)
    subrace = Column(Integer, ForeignKey("subraces.subrace_id"), nullable=True)
    type_id = Column(Integer, ForeignKey("types.type_id"), nullable=True)
    size_id = Column(Integer, ForeignKey("sizes.size_id"), nullable=True)

    # n-n
    classes = relationship("Class", secondary="creature_classes")
    immunities = relationship("Effect", secondary="creature_immunities")
    resistances = relationship("Effect", secondary="creature_resistances")
    vulnerabilities = relationship("Effect", secondary="creature_vulnerabilities")

    # Relationships
    creature_type = relationship("Type", back_populates="creatures")
    size = relationship("Size", back_populates="creatures")

    # Polymorph variable
    creature = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "creatures",
        "polymorphic_on": creature,
    }


class CreatureClasses(Base):
    __tablename__ = "creature_classes"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    class_id = Column("class_id", Integer, ForeignKey("classes.class_id"))
    subclass_id = Column(
        "subclass_id",
        Integer,
        ForeignKey("subclasses.subclass_id"),
        nullable=True,
    )


class CreatureResistances(Base):
    __tablename__ = "creature_resistances"

    id = Column(Integer, primary_key=True)
    creature_id = Column(
        "creature_id", Integer, ForeignKey("creatures.id"), nullable=False
    )
    effect_id = Column(
        "effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False
    )


class CreatureImmunities(Base):
    __tablename__ = "creature_immunities"

    id = Column(Integer, primary_key=True)
    creature_id = Column(
        "creature_id", Integer, ForeignKey("creatures.id"), nullable=False
    )
    effect_id = Column(
        "effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False
    )


class CreatureVulnerabilities(Base):
    __tablename__ = "creature_vulnerabilities"

    id = Column(Integer, primary_key=True)
    creature_id = Column(
        "creature_id", Integer, ForeignKey("creatures.id"), nullable=False
    )
    effect_id = Column(
        "effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False
    )
