from typing import Any, List
from eralchemy2 import render_er

from models.base import Base
from models.enemies import (
    Enemies,
    Monsters,
    EnemyClasses,
    EnemyImmunities,
    EnemyResistances,
    EnemyVulnerabilities,
    MonsterImmunities,
    MonsterResistances,
    MonsterVulnerabilities,
    Types,
)
from models.non_playable_characters import (
    NPCCharacters,
    NPCClasses,
    NPCImmunities,
    NPCResistances,
    NPCVulnerabilities,
)
from models.playable_characters import (
    PlayableCharacters,
    PCClasses,
    PCImmunities,
    PCResistances,
    PCVulnerabilities,
)
from models.characteristics import Classes, Subclasses, Races, Subraces, Effects, Sizes
from models.users import Users


def create_erd():
    """
    Uses the eralchemy2 package to create ERD's from the ORM classes
    """
    models: List[Any] = [
        Base,
        Enemies,
        Monsters,
        EnemyClasses,
        EnemyImmunities,
        EnemyResistances,
        EnemyVulnerabilities,
        MonsterImmunities,
        MonsterResistances,
        MonsterVulnerabilities,
        Types,
        NPCCharacters,
        NPCClasses,
        NPCImmunities,
        NPCResistances,
        NPCVulnerabilities,
        PlayableCharacters,
        PCClasses,
        PCImmunities,
        PCResistances,
        PCVulnerabilities,
        Classes,
        Subclasses,
        Races,
        Subraces,
        Effects,
        Sizes,
        Users,
    ]
    for model in models:
        render_er(input=model, output=f"docs/diagrams/erd.png")


create_erd()
