from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Table, Text
from .base import Base


class PlayableCharacters(Base):
    __tablename__ = "Playable_Characters"
    pc_id = Column("PC_id", Integer, primary_key=True)
    name = Column("Name", String(30), nullable=False)
    description = Column("Description", Text)
    information = Column("Information", Text)
    alive = Column("Alive", Boolean, nullable=False)
    active = Column("Visible", Boolean, nullable=True)
    image = Column("Image", BLOB, nullable=True)
    armour_class = Column("Armour_class", Integer)
    size_id = Column("Id_size", Integer, ForeignKey("Sizes.Size_id"))
    user_id = Column("Id_user", Integer, ForeignKey("Users.User_id"))
    race_id = Column("Race_id", Integer, ForeignKey("Races.Race_id"))


PCClasses = Table(
    "PC_Classes",
    Base.metadata,
    Column("PC_id", Integer, ForeignKey("Playable_Characters.PC_id")),
    Column("Class_id", Integer, ForeignKey("Classes.Class_id")),
    Column("Subclass_id", Integer, ForeignKey("Subclasses.Subclass_id")),
)

PCImmunities = Table(
    "PC Immunities",
    Base.metadata,
    Column("PC_id", Integer, ForeignKey("Playable_Characters.PC_id")),
    Column("Id", Integer, ForeignKey("Effects.Effect_id")),
)

PCResistances = Table(
    "PC_Resistances",
    Base.metadata,
    Column("PC_id", Integer, ForeignKey("Playable_Characters.PC_id")),
    Column("Id", Integer, ForeignKey("Effects.Effect_id")),
)

PCVulnerabilities = Table(
    "PC_Vulnerabilities",
    Base.metadata,
    Column("PC_id", Integer, ForeignKey("Playable_Characters.PC_id")),
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
)
