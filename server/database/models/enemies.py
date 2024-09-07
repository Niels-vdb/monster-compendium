from sqlalchemy import BLOB, Boolean, Column, Integer, String, Table, Text, ForeignKey
from .base import Base


class Enemies(Base):
    __tablename__ = "Enemies"
    enemy_id = Column("Enemy_id", Integer, primary_key=True)
    name = Column("Name", String, nullable=False)
    description = Column("Description", Text)
    information = Column("Information", Text)
    race_id = Column("Race_id", Integer, ForeignKey("Races.Race_id"))


class Monsters(Base):
    __tablename__ = "Monsters"
    monster_id = Column("Monster_id", Integer, primary_key=True)
    name = Column("Name", String, nullable=False)
    description = Column("Description", Text)
    armour_class = Column("Armour_class", Integer)
    alive = Column("Alive", Boolean, nullable=True)
    active = Column("Visible", Boolean, nullable=True)
    image = Column("Image", BLOB, nullable=True)
    size_id = Column("Id_size", Integer, ForeignKey("Sizes.Size_id"))
    type_id = Column("Id_Type", Integer, ForeignKey("Types.Type_id"))


class Types(Base):
    __tablename__ = "Types"
    type_id = Column("Type_id", Integer, primary_key=True)
    type = Column("Type", Text, nullable=False)


EnemyClasses = Table(
    "Enemy_Classes",
    Base.metadata,
    Column("Class_id", Integer, ForeignKey("Classes.Class_id")),
    Column("Enemy_id", Integer, ForeignKey("Enemies.Enemy_id")),
    Column("Subclass_id", Integer, ForeignKey("Subclasses.Subclass_id")),
)

EnemyImmunities = Table(
    "Enemy_Immunities",
    Base.metadata,
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
    Column("Enemy_id", Integer, ForeignKey("Enemies.Enemy_id")),
)

EnemyResistances = Table(
    "Enemy_Resistances",
    Base.metadata,
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
    Column("Enemy_id", Integer, ForeignKey("Enemies.Enemy_id")),
)

EnemyVulnerabilities = Table(
    "Enemy_Vulnerabilities",
    Base.metadata,
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
    Column("Enemy_id", Integer, ForeignKey("Enemies.Enemy_id")),
)

MonsterImmunities = Table(
    "Monster_Immunities",
    Base.metadata,
    Column("Monster_id", Integer, ForeignKey("Monsters.Monster_id")),
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
)

MonsterResistances = Table(
    "Monster_Resistances",
    Base.metadata,
    Column("Monster_id", Integer, ForeignKey("Monsters.Monster_id")),
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
)

MonsterVulnerabilities = Table(
    "Monster_Vulnerabilities",
    Base.metadata,
    Column("Monster_id", Integer, ForeignKey("Monsters.Monster_id")),
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
)
