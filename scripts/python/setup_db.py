import os
import sys

from sqlalchemy import select

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from create_db import session
from config.logger_config import logger
from server.models.attributes import Attribute
from server.models.creatures import CreatureClasses
from server.models.enemies import Enemy
from server.models.player_characters import PlayerCharacter
from server.models.non_player_characters import NonPlayerCharacter
from server.models.races import Race, RaceAdvantages, RaceDisadvantages
from server.models.subraces import (
    Subrace,
    SubraceAdvantages,
    SubraceDisadvantages,
)
from server.models.classes import Class
from server.models.subclasses import Subclass
from server.models.sizes import Size
from server.models.types import Type
from server.models.damage_types import DamageType
from server.models.users import User
from server.models.parties import Party
from server.models.roles import Role


def initialize_party() -> None:
    """
    Creates initial "Murder Hobo Party" party in the parties table
    """
    party = "Murder Hobo Party"
    stmt = select(Party).where(Party.name == party)

    if not session.execute(stmt).scalar_one_or_none():
        logger.info(f"Adding '{party}' to parties table in database.")
        new_party = Party(name=party)
        session.add(new_party)

    session.commit()


def initialize_roles() -> None:
    """
    Creates the roles and add them to the roles table.
    """
    roles: list[str] = ["Admin", "Dungeon Master", "Player"]

    for role in roles:
        stmt = select(Role).where(Role.name == role)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{role}' to roles table in database.")
            new_role = Role(name=role)
            session.add(new_role)

    session.commit()


def initialize_users() -> None:
    """
    Create the initial user accounts and adds them to the users table.
    """
    users: dict[str, dict[str, str]] = {
        "admin": {
            "name": "Admin",
            "username": "admin",
            "roles": ["Admin", "Player"],
            "parties": ["Murder Hobo Party"],
        },
        "player": {
            "name": "Player",
            "username": "player",
            "roles": ["Player"],
            "parties": ["Murder Hobo Party"],
        },
        "dungeonmaster": {
            "name": "Dungeon Master",
            "username": "dungeonmaster",
            "roles": ["Dungeon Master"],
            "parties": ["Murder Hobo Party"],
        },
    }

    for user, info in users.items():
        stmt = select(User).where(User.username == info["username"])

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{user}' to users table in database.")

            info["roles"] = [
                session.execute(
                    select(Role).where(Role.name == role)
                ).scalar_one_or_none()
                for role in info["roles"]
            ]
            info["parties"] = [
                session.execute(
                    select(Party).where(Party.name == party)
                ).scalar_one_or_none()
                for party in info["parties"]
            ]

            new_user = User(**info)
            session.add(new_user)

    session.commit()


def initialize_sizes() -> None:
    """
    All initial sizes to be added to the sizes table.
    """
    sizes: list[str] = [
        "Tiny",
        "Small",
        "Medium",
        "Large",
        "Huge",
        "Gargantuan",
    ]

    for size in sizes:
        stmt = select(Size).where(Size.name == size)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{size}' to the sizes table.")
            new_size = Size(name=size)
            session.add(new_size)

        session.commit()


def initialize_damage_types() -> None:
    """
    All initial damage types and damage types to be added to the damage_types table.
    """
    damage_types: list[str] = [
        "Acid",
        "Bludgeoning",
        "Cold",
        "Fire",
        "Force",
        "Lightning",
        "Necrotic",
        "Piercing",
        "Poison",
        "Psychic",
        "Radiant",
        "Slashing",
        "Thunder",
    ]

    for damage_type in damage_types:
        stmt = select(DamageType).where(DamageType.name == damage_type)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{damage_type}' to the damage types table.")
            new_damage_type = DamageType(name=damage_type)
            session.add(new_damage_type)

    session.commit()


def initialize_attributes() -> None:
    """
    All initial attributes to be added to the attributes table.
    """
    attributes: list[str] = [
        "Acrobatics",
        "Animal Handling",
        "Arcana",
        "Athletics",
        "Attack rolls",
        "Blinded",
        "Charmed",
        "Charisma",
        "Constitution",
        "Deception",
        "Dexterity",
        "Exhaustion",
        "Frightened",
        "History",
        "Incapacitated",
        "Insight",
        "Intelligence",
        "Intimidation",
        "Investigation",
        "Invisible",
        "Magic",
        "Medicine",
        "Nature",
        "Paralyzed",
        "Perception",
        "Performance",
        "Persuasion",
        "Petrified",
        "Poisoned",
        "Prone",
        "Puzzles",
        "Religion",
        "Restrained",
        "Sleight of Hand",
        "Stealth",
        "Strength",
        "Stunned",
        "Survival",
        "Unconscious",
        "Wisdom",
    ]

    for attribute in attributes:
        stmt = select(Attribute).where(Attribute.name == attribute)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{attribute}' to the attributes table.")
            new_attribute = Attribute(name=attribute)
            session.add(new_attribute)

    session.commit()


def initialize_classes() -> None:
    """
    All initial classes to be added to the classes table.
    """
    classes: list[str] = [
        "Artificer",
        "Barbarian",
        "Bard",
        "Cleric",
        "Druid",
        "Fighter",
        "Monk",
        "Paladin",
        "Ranger",
        "Rogue",
        "Sorcerer",
        "Warlock",
        "Wizard",
    ]
    for cls in classes:
        stmt = select(Class).where(Class.name == cls)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{cls}' to the classes table.")
            new_class = Class(name=cls)
            session.add(new_class)

        session.commit()


def initialize_subclasses() -> None:
    """
    All initial subclasses to be added to the subclasses database and linked to classes.
    """
    new_subclasses: dict[str, list[str]] = {
        "Artificer": [
            "Alchemist",
            "Armourer",
            "Artillerist",
            "Battle Smith",
        ],
        "Barbarian": [
            "Ancestral Guardian",
            "Battlerager",
            "Beast",
            "Berserker",
            "Giant",
            "Herculean Path",
            "Storm Herald",
            "Totem Warrior",
            "Wild Magic",
            "Wild Soul",
            "Zealot",
        ],
        "Bard": [
            "College of Creation",
            "College of Eloquence",
            "College of Epic Poetry",
            "College of Glarmour",
            "College of Lore",
            "College of Spirits",
            "College of Swords",
            "College of Valor",
            "College of Whispers",
        ],
        "Cleric": [
            "Death Domain",
            "Forge Domain",
            "Grave Domain",
            "Knowledge Domain",
            "Life Domain",
            "Light Domain",
            "Nature Domain",
            "Order Domain",
            "Prophecy Domain",
            "Tasha Domain",
            "Peace Domain",
            "Tempest Domain",
            "Trickery Domain",
            "Twilight Domain",
            "War Domain",
        ],
        "Druid": [
            "Circle of Dreams",
            "Circle of Land",
            "Circle of Moon",
            "Circle of Sacrifice",
            "Circle of Shepherd",
            "Circle of Spores",
            "Circle of Tasha",
            "Circle of Stars",
            "Circle of Wildfire",
        ],
        "Fighter": [
            "Arcane Archer",
            "Banneret",
            "Battle Master",
            "Cavalier",
            "Champion",
            "Echo Knight",
            "Eldritch Knight",
            "Hoplite Soldier",
            "Psi Warrior",
            "Rune Knight",
            "Samurai",
        ],
        "Monk": [
            "Way of the Astral Self",
            "Way of the Ascendant Dragon",
            "Way of the Drunken Master",
            "Way of the Four Elements",
            "Way of the Kensei",
            "Way of the Long Death",
            "Way of the Mercy",
            "Way of the Open Hand",
            "Way of the Shadow",
            "Way of the Shield",
            "Way of the Sun Soul",
        ],
        "Paladin": [
            "Oath of the Ancients",
            "Oath of the Conquest",
            "Oath of the Crown",
            "Oath of the Devotion",
            "Oath of the Dragonlord",
            "Oath of the Tasha",
            "Oath of the Redemption",
            "Oath of the Vengeance",
            "Oath of the Watchers",
            "Oathbreaker",
        ],
        "Ranger": [
            "Amazonian Conclave",
            "Beast Master",
            "Fey Wanderer",
            "Gloom Stalker",
            "Horizon Walker",
            "Hunter",
            "Monster Slayer",
            "Swarmkeeper",
            "Drakewarden",
        ],
        "Rogue": [
            "The Odyssean",
            "Arcane Trickster",
            "Assassin",
            "Inquisitive",
            "Mastermind",
            "Phantom",
            "Scout",
            "Soulknife",
            "Swashbuckler",
            "Thief",
        ],
        "Sorcerer": [
            "Aberrant Mind",
            "Clockwork Soul",
            "Demigod Origin",
            "Draconic Bloodline",
            "Divine Soul",
            "Lunar Sorcery",
            "Shadow Magic",
            "Storm Sorcery",
            "Wild Magic",
        ],
        "Warlock": [
            "Patron: The Fates",
            "Patron: The Archfey",
            "Patron: The Celestial",
            "Patron: The Fathomless",
            "Patron: The Fiend",
            "Patron: The Genie",
            "Patron: The Great Old One",
            "Patron: The Hexblade",
            "Patron: The Undead",
            "Patron: The Undying",
        ],
        "Wizard": [
            "Academy Philosopher",
            "Abjuration",
            "Bladesinging",
            "Chronurgy",
            "Conjuration",
            "Divination",
            "Enchantment",
            "Evocation",
            "Graviturgy",
            "Illusion",
            "Necromancy",
            "Order of Scribes",
            "Transmutation",
            "War Magic",
        ],
    }
    for parent_class, subclasses in new_subclasses.items():
        cls = session.execute(
            select(Class).where(Class.name == parent_class)
        ).scalar_one_or_none()

        for subclass in subclasses:
            stmt = select(Subclass).where(Subclass.name == subclass)
            if not session.execute(stmt).scalar_one_or_none():
                logger.info(
                    f"Adding '{subclass}' to the subclasses table with '{parent_class}' as parent class."
                )
                new_subclass = Subclass(name=subclass, class_id=cls.id)
                session.add(new_subclass)

    session.commit()


def initialize_races() -> None:
    """
    All initial races to be added to the races table
    """
    races: dict[str, dict[str, list[str | dict[str, str] | None]]] = {
        "Aarakocra": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Aasimar": {
            "size": ["Medium", "Small"],
            "resistance": ["Necrotic", "Radiant"],
            "advantages": [],
            "disadvantages": [],
        },
        "Bugbear": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [{"attribute": "Charmed", "condition": None}],
            "disadvantages": [],
        },
        "Centaur": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Changeling": {
            "size": ["Medium", "Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Dragonborn": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Dwarf": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [{"attribute": "Poisoned", "condition": None}],
            "disadvantages": [],
        },
        "Elf": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [{"attribute": "Charmed", "condition": None}],
            "disadvantages": [],
        },
        "Gnome": {
            "size": ["Small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Intelligence", "condition": "Against magic"},
                {"attribute": "Wisdom", "condition": "Against magic"},
                {"attribute": "Charisma", "condition": "Against magic"},
            ],
            "disadvantages": [],
        },
        "Fairy": {
            "size": ["Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Firbolg": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Genasi": {
            "size": ["Medium", "Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Githyanki": {
            "size": ["Medium"],
            "resistance": ["Psychic"],
            "advantages": [],
            "disadvantages": [],
        },
        "Githzerai": {
            "size": ["Medium"],
            "resistance": ["Psychic"],
            "advantages": [
                {"attribute": "Charmed", "condition": None},
            ],
            "disadvantages": [],
        },
        "Goblin": {
            "size": ["Small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Charmed", "condition": None},
            ],
            "disadvantages": [],
        },
        "Goliath": {
            "size": ["Medium"],
            "resistance": ["Cold"],
            "advantages": [],
            "disadvantages": [],
        },
        "Half-Elf": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Half-Orc": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Halfling": {
            "size": ["Small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Frightened", "condition": None},
            ],
            "disadvantages": [],
        },
        "Harengon": {
            "size": ["Medium", "Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Hobgoblin": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Charmed", "condition": None},
            ],
            "disadvantages": [],
        },
        "Human": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Kenku": {
            "size": ["Medium", "Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Kobold": {
            "size": ["Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Lizard folk": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Minotaur": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Orc": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Satyr": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Magic", "condition": None},
            ],
            "disadvantages": [],
        },
        "Shifter": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Tabaxi": {
            "size": ["Medium", "Small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Tiefling": {
            "size": ["Medium"],
            "resistance": ["Fire"],
            "advantages": [],
            "disadvantages": [],
        },
        "Thylean Centaur": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Thylean Medusa": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Poisoned", "condition": "Against spells and abilities"},
            ],
            "disadvantages": [],
        },
        "Thylean Minotaur": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Perception", "condition": "On smells"},
                {"attribute": "Puzzles", "condition": "Maze like puzzles"},
            ],
            "disadvantages": [],
        },
        "Thylean Nymph": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Thylean Satyr": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Charmed", "condition": None},
            ],
            "disadvantages": [],
        },
        "Thylean Siren": {
            "size": ["Medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Performance", "condition": "When using your voice"},
                {"attribute": "Persuasion", "condition": "When using your voice"},
            ],
            "disadvantages": [],
        },
        "Tortle": {
            "size": ["Medium", "Small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Strength", "condition": "When in shell"},
                {"attribute": "Constitution", "condition": "When in shell"},
            ],
            "disadvantages": [
                {"attribute": "Dexterity", "condition": "When in shell"},
            ],
        },
        "Triton": {
            "size": ["Medium"],
            "resistance": ["Cold"],
            "advantages": [],
            "disadvantages": [],
        },
        "Yuan-ti": {
            "size": ["Medium", "Small"],
            "resistance": ["Poison"],
            "advantages": [
                {"attribute": "Magic", "condition": None},
                {"attribute": "Poisoned", "condition": None},
            ],
            "disadvantages": [],
        },
    }
    for race, values in races.items():
        stmt = select(Race).where(Race.name == race)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{race}' to the races table.")

            size_list = [
                session.execute(
                    select(Size).where(Size.name == size)
                ).scalar_one_or_none()
                for size in values["size"]
            ]
            resistance_list = [
                session.execute(
                    select(DamageType).where(DamageType.name == resistance)
                ).scalar_one_or_none()
                for resistance in values["resistance"]
            ]
            resistance_list = [
                resistance for resistance in resistance_list if resistance is not None
            ]

            new_race = Race(name=race, sizes=size_list, resistances=resistance_list)
            session.add(new_race)

            session.commit()
            session.refresh(new_race)

            # Adding of optional (dis)advantages to the race
            for advantage in values["advantages"]:
                attribute = session.execute(
                    select(Attribute).where(Attribute.name == advantage["attribute"])
                ).scalar_one_or_none()

                if not attribute:
                    logger.info(
                        f"Attribute not found for race '{new_race}', continuing."
                    )
                else:
                    advantage = RaceAdvantages(
                        race_id=new_race.id,
                        attribute_id=attribute.id,
                        condition=advantage["condition"],
                    )
                    session.add(advantage)

            for disadvantage in values["disadvantages"]:
                attribute = session.execute(
                    select(Attribute).where(Attribute.name == disadvantage["attribute"])
                ).scalar_one_or_none()

                if not attribute:
                    logger.info(
                        f"Attribute not found for race '{new_race}', continuing."
                    )
                else:
                    disadvantage = RaceDisadvantages(
                        race_id=new_race.id,
                        attribute_id=attribute.id,
                        condition=disadvantage["condition"],
                    )
                    session.add(disadvantage)

            session.commit()


def initialize_subraces() -> None:
    """
    All initial subraces to be added to the subraces table and linked to a race.
    """
    new_subraces: dict[str, dict[str, list[str | dict[str, str]]]] = {
        "Dragonborn": {
            "Black": {
                "resistances": ["Acid"],
                "advantages": [],
                "disadvantages": [],
            },
            "Blue": {
                "resistances": ["Lightning"],
                "advantages": [],
                "disadvantages": [],
            },
            "Brass": {
                "resistances": ["Fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Bronze": {
                "resistances": ["Lightning"],
                "advantages": [],
                "disadvantages": [],
            },
            "Copper": {
                "resistances": ["Acid"],
                "advantages": [],
                "disadvantages": [],
            },
            "Gold": {
                "resistances": ["Fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Green": {
                "resistances": ["Poison"],
                "advantages": [],
                "disadvantages": [],
            },
            "Red": {
                "resistances": ["Fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Silver": {
                "resistances": ["Cold"],
                "advantages": [],
                "disadvantages": [],
            },
            "White": {
                "resistances": ["Cold"],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Dwarf": {
            "Duergar": {
                "resistances": [],
                "advantages": [
                    {"attribute": "Charmed", "condition": None},
                    {"attribute": "Stunned", "condition": None},
                ],
                "disadvantages": [],
            },
            "Mountain": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Hill": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Elf": {
            "Astral": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Dark (Drow)": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [
                    {"attribute": "Attack rolls", "condition": "When in sunlight"},
                    {"attribute": "Perception", "condition": "When in sunlight"},
                ],
            },
            "Eladrin": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "High": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Sea Elf": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Shadar-kai": {
                "resistances": ["Necrotic"],
                "advantages": [],
                "disadvantages": [],
            },
            "Wood": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Genasi": {
            "Air": {
                "resistances": ["Lightning"],
                "advantages": [],
                "disadvantages": [],
            },
            "Earth": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Fire": {
                "resistances": ["Fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Water": {
                "resistances": ["Acid"],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Gnome": {
            "Deep": {
                "resistances": [],
                "advantages": [
                    {"attribute": "Dexterity", "condition": "When going into stealth"},
                ],
                "disadvantages": [],
            },
            "Forest": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Rock": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Halfling": {
            "Lightfoot": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Stout": {
                "resistances": ["Poison"],
                "advantages": [
                    {"attribute": "Poisoned", "condition": None},
                ],
                "disadvantages": [],
            },
        },
        "Human": {
            "Variant": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Tiefling": {
            "Abyssal Tiefling": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Asmodeus": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Baalzebul": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Dispater": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Fierna": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Glasya": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Levistus": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Mammon": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Mephistopheles": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Bloodline of Zariel": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Variant Tiefling": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Thylean Nymph": {
            "Aurae": {
                "resistances": [],
                "advantages": [
                    {
                        "attribute": "Survival",
                        "condition": "When navigating by the stars",
                    },
                ],
                "disadvantages": [],
            },
            "Dryad": {
                "resistances": [],
                "advantages": [
                    {"attribute": "Survival", "condition": "When in forested areas"},
                ],
                "disadvantages": [],
            },
            "Naiad": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Nereid": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Oread": {
                "resistances": [],
                "advantages": [
                    {
                        "attribute": "Survival",
                        "condition": "When in steppes, rocky islands, and mountainous regions",
                    },
                ],
                "disadvantages": [],
            },
        },
    }

    for race, subraces in new_subraces.items():
        stmt = select(Race).where(Race.name == race)
        parent_race = session.execute(stmt).scalar_one_or_none()

        if not parent_race:
            logger.info(f"Race '{race}' not found in database")

        for subrace in subraces:

            if not session.execute(
                select(Subrace).where(Subrace.name == subrace)
            ).scalar_one_or_none():
                logger.info(
                    f"Adding subrace '{subrace}' of race '{race}' to the subraces table."
                )

                resistances = list(subraces[subrace]["resistances"])
                resistance_list = [
                    session.execute(
                        select(DamageType).where(DamageType.name == resistance)
                    ).scalar_one_or_none()
                    for resistance in resistances
                ]

                new_subrace = Subrace(
                    name=subrace, race=parent_race, resistances=resistance_list
                )
                session.add(new_subrace)

                session.commit()
                session.refresh(new_subrace)

                # Adding of optional (dis)advantages to the subrace
                for advantage in subraces[subrace]["advantages"]:
                    attribute = session.execute(
                        select(Attribute).where(
                            Attribute.name == advantage["attribute"]
                        )
                    ).scalar_one_or_none()

                    if not attribute:
                        logger.info(
                            f"Advantage attribute '{advantage}' not found for subrace '{new_subrace.name}', continuing."
                        )
                    else:
                        advantage = SubraceAdvantages(
                            subrace_id=new_subrace.id,
                            attribute_id=attribute.id,
                            condition=advantage["condition"],
                        )
                        session.add(advantage)

                for disadvantage in subraces[subrace]["disadvantages"]:
                    attribute = session.execute(
                        select(Attribute).where(
                            Attribute.name == disadvantage["attribute"]
                        )
                    ).scalar_one_or_none()

                    if not attribute:
                        logger.info(
                            f"Disadvantage attribute '{disadvantage}' not found for subrace '{new_subrace.name}', continuing."
                        )
                    else:
                        disadvantage = SubraceDisadvantages(
                            subrace_id=new_subrace.id,
                            attribute_id=attribute.id,
                            condition=disadvantage["condition"],
                        )
                        session.add(disadvantage)

                session.commit()


def initialize_types() -> None:
    """
    All initial creature types to be added to the types table.
    """
    types: list[str] = [
        "Aberration",
        "Beast",
        "Celestial",
        "Construct",
        "Dragon",
        "Elemental",
        "Fey",
        "Fiend",
        "Giant",
        "Humanoid",
        "Monstrosity",
        "Ooze",
        "Plant",
        "Undead",
    ]
    for type in types:
        stmt = select(Type).where(Type.name == type)

        if not session.execute(stmt).scalar_one_or_none():
            logger.info(f"Adding '{type}' to the types table.")
            new_type = Type(name=type)
            session.add(new_type)

    session.commit()


def create_creatures() -> None:
    """
    Creates two player characters, 2 non player characters and two enemies with
    attributes and adds them to their associated table.
    """
    creatures: dict[str, dict[str, str]] = {
        "Rhoetus": {
            "creature_type": PlayerCharacter,
            "alive": True,
            "active": True,
            "size": "Medium",
            "description": "A centaur barbarian.",
            "information": "Some information about Rhoetus.",
            "armour_class": 17,
            "classes": ["Barbarian"],
            "subclasses": ["Herculean Path"],
            "race_id": "Thylean Centaur",
            "user": "player",
            "parties": ["Murder Hobo Party"],
        },
        "Electra": {
            "creature_type": PlayerCharacter,
            "alive": True,
            "active": True,
            "size": "Medium",
            "description": "A nymph fighter",
            "information": "Some information about Electra.",
            "armour_class": 18,
            "classes": ["Fighter"],
            "subclasses": ["Hoplite Soldier"],
            "race_id": "Thylean Nymph",
            "subrace_id": "Naiad",
            "user": "admin",
            "parties": ["Murder Hobo Party"],
        },
        "Endofyre": {
            "creature_type": NonPlayerCharacter,
            "alive": True,
            "active": True,
            "size": "Medium",
            "parties": ["Murder Hobo Party"],
        },
        "Fersi (Oracle)": {
            "creature_type": NonPlayerCharacter,
            "alive": True,
            "active": True,
            "type": "Celestial",
            "size": "Medium",
            "parties": ["Murder Hobo Party"],
        },
        "Giff": {
            "creature_type": Enemy,
            "alive": True,
            "active": True,
            "description": "A large hippo like creature",
            "information": "Some information about this big hippo, like his knowledge about firearms.",
            "armour_class": 16,
            "classes": ["Artificer", "Ranger"],
            "subclasses": ["Artillerist", "Amazonian Conclave"],
            "type": "Humanoid",
            "size": "Medium",
            "immunities": ["Fire"],
            "resistances": ["Cold"],
            "vulnerabilities": ["Acid"],
            "parties": ["Murder Hobo Party"],
        },
        "Froghemoth": {
            "creature_type": Enemy,
            "alive": True,
            "active": True,
            "description": "A huge frog like creature",
            "information": "Some information about this big froggy, like his size being that of an oliphant.",
            "armour_class": 19,
            "type": "Monstrosity",
            "size": "Huge",
            "resistances": ["Fire", "Lightning"],
        },
    }

    for creature, attributes in creatures.items():
        creature_type = attributes["creature_type"]
        del attributes["creature_type"]

        if not session.execute(
            select(creature_type).where(creature_type.name == creature)
        ).scalar_one_or_none():
            logger.info(
                f"Adding '{creature}' to the {creature_type.__tablename__} table."
            )

            attributes["size_id"] = (
                session.execute(select(Size).where(Size.name == attributes["size"]))
                .scalar_one_or_none()
                .id
            )
            del attributes["size"]

            if "type" in attributes.keys():
                attributes["type_id"] = (
                    session.execute(select(Type).where(Type.name == attributes["type"]))
                    .scalar_one_or_none()
                    .id
                )
                del attributes["type"]

            classes: list[Class] = None
            if "classes" in attributes.keys():
                classes = [
                    session.execute(
                        select(Class).where(Class.name == attribute)
                    ).scalar_one_or_none()
                    for attribute in attributes["classes"]
                ]
                del attributes["classes"]

            subclasses: list[Subclass] = None
            if "subclasses" in attributes.keys():
                subclasses = [
                    session.execute(
                        select(Subclass).where(Subclass.name == attribute)
                    ).scalar_one_or_none()
                    for attribute in attributes["subclasses"]
                ]
                del attributes["subclasses"]

            if "race_id" in attributes.keys():
                attributes["race_id"] = (
                    session.execute(
                        select(Race).where(Race.name == attributes["race_id"])
                    )
                    .scalar_one_or_none()
                    .id
                )

            if "subrace_id" in attributes.keys():
                attributes["subrace_id"] = (
                    session.execute(
                        select(Subrace).where(Subrace.name == attributes["subrace_id"])
                    )
                    .scalar_one_or_none()
                    .id
                )

            if "parties" in attributes.keys():
                attributes["parties"] = [
                    session.execute(
                        select(Party).where(Party.name == attribute)
                    ).scalar_one_or_none()
                    for attribute in attributes["parties"]
                ]

            if "user" in attributes.keys():
                attributes["user_id"] = (
                    session.execute(
                        select(User).where(User.username == attributes["user"])
                    )
                    .scalar_one_or_none()
                    .id
                )
                del attributes["user"]

            if "resistances" in attributes.keys():
                attributes["resistances"] = [
                    session.execute(
                        select(DamageType).where(DamageType.name == attribute)
                    ).scalar_one_or_none()
                    for attribute in attributes["resistances"]
                ]

            if "immunities" in attributes.keys():
                attributes["immunities"] = [
                    session.execute(
                        select(DamageType).where(DamageType.name == attribute)
                    ).scalar_one_or_none()
                    for attribute in attributes["immunities"]
                ]

            if "vulnerabilities" in attributes.keys():
                attributes["vulnerabilities"] = [
                    session.execute(
                        select(DamageType).where(DamageType.name == attribute)
                    ).scalar_one_or_none()
                    for attribute in attributes["vulnerabilities"]
                ]

            # Create the new PlayerCharacter
            new_creature = creature_type(name=creature, **attributes)
            session.add(new_creature)
            session.flush()

            # Adds classes and subclasses to CreatureClasses cross-reference table
            if classes:
                for cls in classes:
                    linked_subclasses = [
                        subclass
                        for subclass in subclasses
                        if subclass.class_id == cls.id
                    ]
                    if linked_subclasses:
                        for subclass in linked_subclasses:
                            creature_class_entry = CreatureClasses(
                                creature_id=new_creature.id,
                                class_id=cls.id,
                                subclass_id=subclass.id,
                            )
                            session.add(creature_class_entry)
                    else:
                        creature_class_entry = CreatureClasses(
                            creature_id=new_creature.id, class_id=cls.id
                        )
                        session.add(creature_class_entry)

    session.commit()


def main() -> None:
    """
    Main function that runs to add initial data to the database.
    """
    try:
        initialize_party()
        initialize_roles()
        initialize_users()
        initialize_sizes()
        initialize_damage_types()
        initialize_attributes()
        initialize_classes()
        initialize_subclasses()
        initialize_races()
        initialize_subraces()
        initialize_types()
        create_creatures()
    except Exception as e:
        logger.error(
            f"An error occurred while filling the database with initial data. Error: {str(e)}"
        )


if __name__ == "__main__":
    main()
