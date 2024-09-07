from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Table
from .base import Base


class NPCCharacters(Base):
    __tablename__ = "NPC_Characters"
    npc_id = Column("NPC_id", Integer, primary_key=True)
    name = Column("Name", String(30), nullable=False)
    alive = Column("Alive", Boolean, nullable=False)
    armour_class = Column("Armour_class", Integer, nullable=False)
    active = Column("Visible", Boolean, nullable=False)
    image = Column("Image", BLOB, nullable=False)
    race_id = Column("Race_id", Integer, ForeignKey("Races.Race_id"))
    size_id = Column("Id_size", Integer, ForeignKey("Sizes.Size_id"))


NPCClasses = Table(
    "NPC_Classes",
    Base.metadata,
    Column("NPC_id", Integer, ForeignKey("NPC_Characters.NPC_id")),
    Column("Class_id", Integer, ForeignKey("Classes.Class_id")),
    Column("Subclass_id", Integer, ForeignKey("Subclasses.Subclass_id")),
)

NPCImmunities = Table(
    "NPC_Immunities",
    Base.metadata,
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
    Column("NPC_id", Integer, ForeignKey("NPC_Characters.NPC_id")),
)

NPCResistances = Table(
    "NPC_Resistances",
    Base.metadata,
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
    Column("NPC_id", Integer, ForeignKey("NPC_Characters.NPC_id")),
)

NPCVulnerabilities = Table(
    "NPC_Vulnerabilities",
    Base.metadata,
    Column("Effect_id", Integer, ForeignKey("Effects.Effect_id")),
    Column("NPC_id", Integer, ForeignKey("NPC_Characters.NPC_id")),
)
