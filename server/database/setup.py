from typing import Dict, List

from server.database.create import session
from server.database.models.attributes import Attribute
from server.database.models.creatures import CreatureClasses
from server.database.models.enemies import Enemy
from server.database.models.player_characters import PlayerCharacter
from server.database.models.non_player_characters import NonPlayerCharacter
from server.database.models.races import (
    Race,
    RaceAdvantages,
    RaceDisadvantages,
    RaceImmunities,
    RaceResistances,
    RaceVulnerabilities,
)
from server.database.models.subraces import (
    Subrace,
    SubraceAdvantages,
    SubraceDisadvantages,
    SubraceImmunities,
    SubraceResistances,
    SubraceVulnerabilities,
)

from server.database.models.classes import Class, Subclass
from server.database.models.characteristics import Size, Type
from server.database.models.damage_types import DamageType
from server.database.models.users import User, Party, Role


def initialize_party() -> None:
    """
    Creates initial "Murder Hobo Party" party in the parties table
    """
    party = "Murder Hobo Party"

    if not session.query(Party).filter(Party.name == party).first():
        print(f"Adding '{party}' to parties table in database.")
        new_party = Party(name=party)
        session.add(new_party)
    session.commit()


def initialize_roles() -> None:
    """
    Creates the roles and add them to the roles table.
    """
    roles: List[str] = ["Admin", "Dungeon Master", "Player"]

    for role in roles:
        if not session.query(Role).filter(Role.name == role).first():
            print(f"Adding '{role}' to roles table in database.")
            new_role = Role(name=role)
            session.add(new_role)
    session.commit()


def initialize_users() -> None:
    """
    Create the initial user accounts and adds them to the users table.
    """
    users: Dict[str, Dict[str, str]] = {
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
        if not session.query(User).filter(User.username == info["username"]).first():
            print(f"Adding '{user}' to users table in database.")
            info["roles"] = [
                session.query(Role).filter(Role.name == role).first()
                for role in info["roles"]
            ]
            info["parties"] = [
                session.query(Party).filter(Party.name == party).first()
                for party in info["parties"]
            ]

            new_user = User(**info)
            session.add(new_user)
    session.commit()


def initialize_sizes() -> None:
    """
    All initial sizes to be added to the sizes table.
    """
    sizes: List[str] = [
        "Tiny",
        "Small",
        "Medium",
        "Large",
        "Huge",
        "Gargantuan",
    ]

    for size in sizes:
        if not session.query(Size).filter(Size.name == size).first():
            print(f"Adding {size} to the sizes table in the database.")
            new_size = Size(name=size)
            session.add(new_size)
        session.commit()


def initialize_damage_types() -> None:
    """
    All initial damage_types and damage types to be added to the damage_types table.
    """
    damage_types: List[str] = [
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
        if not session.query(DamageType).filter(DamageType.name == damage_type).first():
            print(f"Adding '{damage_type}' to the damage_types table in the database.")
            new_damage_type = DamageType(name=damage_type)
            session.add(new_damage_type)
    session.commit()


def initialize_attributes() -> None:
    """
    All initial attributes to be added to the attributes table.
    """
    attributes: List[str] = [
        "Acrobatics",
        "Animal Handling",
        "Arcana",
        "Athletics",
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
        if not session.query(Attribute).filter(Attribute.name == attribute).first():
            print(f"Adding '{attribute}' to the conditions table in the database.")
            new_attribute = Attribute(name=attribute)
            session.add(new_attribute)
    session.commit()


def initialize_classes() -> None:
    """
    All initial classes to be added to the classes table.
    """
    classes: List[str] = [
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
        if not session.query(Class).filter(Class.name == cls).first():
            print(f"Adding {cls} to the classes table.")
            new_class = Class(name=cls)
            session.add(new_class)
        session.commit()


def initialize_subclasses() -> None:
    """
    All initial subclasses to be added to the subclasses database and linked to classes.
    """
    subclasses: Dict[str, str] = {
        "Artificer": [
            "Alchemist",
            "Armorer",
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
    for parent_class in subclasses.keys():
        cls = session.query(Class).filter(Class.name == parent_class).first()
        for subclass in subclasses[parent_class]:
            if not session.query(Subclass).filter(Subclass.name == subclass).first():
                print(
                    f"Adding '{subclass}' to the subclasses table with '{parent_class}' as parent class."
                )
                new_subclass = Subclass(name=subclass, class_id=cls.id)
                session.add(new_subclass)
    session.commit()


def initialize_races() -> None:
    """
    All initial races to be added to the races table
    """
    races: Dict[str, Dict[str, List[str]]] = {
        "Aarakocra": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Aasimar": {
            "size": ["medium", "small"],
            "resistance": ["necrotic", "radiant"],
            "advantages": [],
            "disadvantages": [],
        },
        "Bugbear": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [{"attribute": "Charmed", "attribute": ""}],
            "disadvantages": [],
        },
        "Centaur": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Changeling": {
            "size": ["medium", "small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Dragonborn": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Dwarf": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [{"attribute": "Poisoned", "condition": ""}],
            "disadvantages": [],
        },
        "Elf": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [{"attribute": "Charmed", "condition": ""}],
            "disadvantages": [],
        },
        "Gnome": {
            "size": ["small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Intelligence", "condition": "Against magic"},
                {"attribute": "Wisdom", "condition": "Against magic"},
                {"attribute": "Charisma", "condition": "Against magic"},
            ],
            "disadvantages": [],
        },
        "Fairy": {
            "size": ["small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Firbolg": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Genasi": {
            "size": ["medium", "small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Githyanki": {
            "size": ["medium"],
            "resistance": ["psychic"],
            "advantages": [],
            "disadvantages": [],
        },
        "Githzerai": {
            "size": ["medium"],
            "resistance": ["psychic"],
            "advantages": [
                {"attribute": "Charmed", "condition": ""},
            ],
            "disadvantages": [],
        },
        "Goblin": {
            "size": ["small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Charmed", "condition": ""},
            ],
            "disadvantages": [],
        },
        "Goliath": {
            "size": ["medium"],
            "resistance": ["cold"],
            "advantages": [],
            "disadvantages": [],
        },
        "Half-Elf": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Half-Orc": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Halfling": {
            "size": ["small"],
            "resistance": [],
            "advantages": [
                {"attribute": "Frightened", "condition": ""},
            ],
            "disadvantages": [],
        },
        "Harengon": {
            "size": ["medium", "small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Hobgoblin": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Charmed", "condition": ""},
            ],
            "disadvantages": [],
        },
        "Human": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Kenku": {
            "size": ["medium", "small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Kobold": {
            "size": ["small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Lizard folk": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Minotaur": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Orc": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Satyr": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Magic", "condition": ""},
            ],
            "disadvantages": [],
        },
        "Shifter": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Tabaxi": {
            "size": ["medium", "small"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Tiefling": {
            "size": ["medium"],
            "resistance": ["fire"],
            "advantages": [],
            "disadvantages": [],
        },
        "Thylean Centaur": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Thylean Medusa": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Poisoned", "condition": "Against spells and abilities"},
            ],
            "disadvantages": [],
        },
        "Thylean Minotaur": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Perception", "condition": "On smells"},
                {"attribute": "Puzzles", "condition": "Maze like puzzles"},
            ],
            "disadvantages": [],
        },
        "Thylean Nymph": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [],
            "disadvantages": [],
        },
        "Thylean Satyr": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Charmed", "condition": ""},
            ],
            "disadvantages": [],
        },
        "Thylean Siren": {
            "size": ["medium"],
            "resistance": [],
            "advantages": [
                {"attribute": "Performance", "condition": "When using your voice"},
                {"attribute": "Persuasion", "condition": "When using your voice"},
            ],
            "disadvantages": [],
        },
        "Tortle": {
            "size": ["medium", "small"],
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
            "size": ["medium"],
            "resistance": ["cold"],
            "advantages": [],
            "disadvantages": [],
        },
        "Yuan-ti": {
            "size": ["medium", "small"],
            "resistance": ["poison"],
            "advantages": [
                {"attribute": "Magic", "condition": ""},
                {"attribute": "Poisoned", "condition": ""},
            ],
            "disadvantages": [],
        },
    }
    for race, values in races.items():
        if not session.query(Race).filter(Race.name == race).first():
            print(f"Adding '{race}' to the races table in the database.")
            size_list = [
                session.query(Size).filter(Size.name == size.capitalize()).first()
                for size in values["size"]
            ]
            resistance_list = [
                session.query(DamageType)
                .filter(DamageType.name == resistance.capitalize())
                .first()
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
                attribute = (
                    session.query(Attribute)
                    .filter(Attribute.name == advantage["attribute"].capitalize())
                    .first()
                )
                if not attribute:
                    print(f"Attribute not found for race '{new_race}', continuing.")
                else:
                    advantage = RaceAdvantages(
                        race_id=new_race.id,
                        attribute_id=attribute.id,
                        condition=advantage["condition"],
                    )
                    session.add(advantage)
            for disadvantage in values["disadvantages"]:
                attribute = (
                    session.query(Attribute)
                    .filter(Attribute.name == disadvantage["attribute"].capitalize())
                    .first()
                )
                if not attribute:
                    print(f"Attribute not found for race '{new_race}', continuing.")
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
    subraces: dict[str, dict[str, list[str | dict[str, str]]]] = {
        "Dragonborn": {
            "Black": {
                "resistances": ["acid"],
                "advantages": [],
                "disadvantages": [],
            },
            "Blue": {
                "resistances": ["lightning"],
                "advantages": [],
                "disadvantages": [],
            },
            "Brass": {
                "resistances": ["fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Bronze": {
                "resistances": ["lightning"],
                "advantages": [],
                "disadvantages": [],
            },
            "Copper": {
                "resistances": ["acid"],
                "advantages": [],
                "disadvantages": [],
            },
            "Gold": {
                "resistances": ["fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Green": {
                "resistances": ["poison"],
                "advantages": [],
                "disadvantages": [],
            },
            "Red": {
                "resistances": ["fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Silver": {
                "resistances": ["cold"],
                "advantages": [],
                "disadvantages": [],
            },
            "White": {
                "resistances": ["cold"],
                "advantages": [],
                "disadvantages": [],
            },
        },
        "Dwarf": {
            "Duergar": {
                "resistances": [],
                "advantages": [
                    {"attribute": "Charmed", "condition": ""},
                    {"attribute": "Stunned", "condition": ""},
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
                "resistances": ["necrotic"],
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
                "resistances": ["lightning"],
                "advantages": [],
                "disadvantages": [],
            },
            "Earth": {
                "resistances": [],
                "advantages": [],
                "disadvantages": [],
            },
            "Fire": {
                "resistances": ["fire"],
                "advantages": [],
                "disadvantages": [],
            },
            "Water": {
                "resistances": ["acid"],
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
                "resistances": ["poison"],
                "advantages": [
                    {"attribute": "Poison", "condition": ""},
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

    for race, subraces in subraces.items():
        parent_race = session.query(Race).filter(Race.name == race.title()).first()
        if not parent_race:
            print(f"Race '{race}' not found in database")

        for subrace in subraces:
            if not session.query(Subrace).filter(Subrace.name == subrace).first():
                print(
                    f"Adding subrace '{subrace}' of race '{race}' to the subraces table in the database."
                )
                resistances = list(subraces[subrace]["resistances"])
                resistance_list = [
                    session.query(DamageType)
                    .filter(DamageType.name == resistance.capitalize())
                    .first()
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
                    attribute = (
                        session.query(Attribute)
                        .filter(Attribute.name == advantage["attribute"].capitalize())
                        .first()
                    )
                    if not attribute:
                        print(
                            f"Attribute not found for subrace '{new_subrace}', continuing."
                        )
                    else:
                        advantage = SubraceAdvantages(
                            subrace_id=new_subrace.id,
                            attribute_id=attribute.id,
                            condition=advantage["condition"],
                        )
                        session.add(advantage)
                for disadvantage in subraces[subrace]["disadvantages"]:
                    attribute = (
                        session.query(Attribute)
                        .filter(
                            Attribute.name == disadvantage["attribute"].capitalize()
                        )
                        .first()
                    )
                    if not attribute:
                        print(
                            f"Attribute not found for subrace '{new_subrace}', continuing."
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
    types: List[str] = [
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
        if not session.query(Type).filter(Type.name == type).first():
            print(f"Adding '{type}' to the types table in the database.")
            new_type = Type(name=type)
            session.add(new_type)
    session.commit()


def create_pcs() -> None:
    """
    Creates two player characters with attributes and adds them to the player_characters table.
    """
    pcs: Dict[str, dict[str, str]] = {
        "Rhoetus": {
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
    }

    for pc, attributes in pcs.items():
        if (
            not session.query(PlayerCharacter)
            .filter(PlayerCharacter.name == pc)
            .first()
        ):
            print(
                f"Adding '{pc}' to player_characters table in the database with the following attributes: {attributes}."
            )

            attributes["size_id"] = (
                session.query(Size).filter(Size.name == attributes["size"]).first().id
            )
            del attributes["size"]

            if "type" in attributes.keys():
                attributes["type_id"] = (
                    session.query(Type)
                    .filter(Type.name == attributes["type"])
                    .first()
                    .id
                )
                del attributes["type"]

            classes: List[Class] = None
            subclasses: List[Subclass] = None
            if "classes" in attributes.keys():
                classes = [
                    session.query(Class).filter(Class.name == attribute).first()
                    for attribute in attributes["classes"]
                ]
                del attributes["classes"]
            if "subclasses" in attributes.keys():
                subclasses = [
                    session.query(Subclass).filter(Subclass.name == attribute).first()
                    for attribute in attributes["subclasses"]
                ]
                del attributes["subclasses"]
            if "race_id" in attributes.keys():
                attributes["race_id"] = (
                    session.query(Race)
                    .filter(Race.name == attributes["race_id"])
                    .first()
                    .id
                )
            if "subrace_id" in attributes.keys():
                attributes["subrace_id"] = (
                    session.query(Subrace)
                    .filter(Subrace.name == attributes["subrace_id"])
                    .first()
                    .id
                )
            if "parties" in attributes.keys():
                attributes["parties"] = [
                    session.query(Party).filter(Party.name == attribute).first()
                    for attribute in attributes["parties"]
                ]
            if "user" in attributes.keys():
                attributes["user_id"] = (
                    session.query(User)
                    .filter(User.username == attributes["user"])
                    .first()
                    .id
                )
                del attributes["user"]

            # Create the new PlayerCharacter
            new_pc = PlayerCharacter(name=pc, **attributes)
            session.add(new_pc)
            session.flush()

            # Adds classes and subclasses to CreatureClasses cross-reference table
            if classes:
                for cls in classes:
                    linked_subclasses = [
                        sc for sc in subclasses if sc.class_id == cls.id
                    ]
                    if linked_subclasses:
                        for subclass in linked_subclasses:
                            creature_class_entry = CreatureClasses(
                                creature_id=new_pc.id,
                                class_id=cls.id,
                                subclass_id=subclass.id,
                            )
                            session.add(creature_class_entry)
                    else:
                        creature_class_entry = CreatureClasses(
                            creature_id=new_pc.id, class_id=cls.id
                        )
                        session.add(creature_class_entry)

    session.commit()


def create_npcs() -> None:
    """
    Creates two non player characters with attributes and adds them to the non_player_characters table.
    """
    npcs: Dict[str, dict[str, str]] = {
        "Endofyre": {
            "alive": True,
            "active": True,
            "size": "Medium",
            "parties": ["Murder Hobo Party"],
        },
        "Fersi (Oracle)": {
            "alive": True,
            "active": True,
            "type": "Celestial",
            "size": "Medium",
            "parties": ["Murder Hobo Party"],
        },
    }

    for npc, attributes in npcs.items():
        if (
            not session.query(NonPlayerCharacter)
            .filter(NonPlayerCharacter.name == npc)
            .first()
        ):
            print(
                f"Adding '{npc}' to npc_characters table in the database with the following attributes: {attributes}."
            )
            attributes["size_id"] = (
                session.query(Size).filter(Size.name == attributes["size"]).first().id
            )
            del attributes["size"]

            if "type" in attributes.keys():
                attributes["type_id"] = (
                    session.query(Type)
                    .filter(Type.name == attributes["type"])
                    .first()
                    .id
                )
                del attributes["type"]
            if "parties" in attributes.keys():
                attributes["parties"] = [
                    session.query(Party).filter(Party.name == attribute).first()
                    for attribute in attributes["parties"]
                ]

            new_npc = NonPlayerCharacter(name=npc, **attributes)
            session.add(new_npc)
    session.commit()


def create_enemies() -> None:
    """
    Creates two monster characters with attributes and adds them to the enemies table.
    """
    enemies: Dict[str, dict[str, str]] = {
        "Giff": {
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

    for enemy, attributes in enemies.items():
        if not session.query(Enemy).filter(Enemy.name == enemy).first():
            print(
                f"Adding '{enemy}' to monsters table in the database with the following attributes: {attributes}."
            )
            attributes["size_id"] = (
                session.query(Size).filter(Size.name == attributes["size"]).first().id
            )
            del attributes["size"]

            if "type" in attributes.keys():
                attributes["type_id"] = (
                    session.query(Type)
                    .filter(Type.name == attributes["type"])
                    .first()
                    .id
                )
                del attributes["type"]
            classes: List[Class] = None
            subclasses: List[Subclass] = None
            if "classes" in attributes.keys():
                print("Classes")
                classes = [
                    session.query(Class).filter(Class.name == attribute).first()
                    for attribute in attributes["classes"]
                ]
                del attributes["classes"]
            if "subclasses" in attributes.keys():
                subclasses = [
                    session.query(Subclass).filter(Subclass.name == attribute).first()
                    for attribute in attributes["subclasses"]
                ]
                del attributes["subclasses"]
            if "resistances" in attributes.keys():
                attributes["resistances"] = [
                    session.query(DamageType)
                    .filter(DamageType.name == attribute)
                    .first()
                    for attribute in attributes["resistances"]
                ]
            if "immunities" in attributes.keys():
                attributes["immunities"] = [
                    session.query(DamageType)
                    .filter(DamageType.name == attribute)
                    .first()
                    for attribute in attributes["immunities"]
                ]
            if "vulnerabilities" in attributes.keys():
                attributes["vulnerabilities"] = [
                    session.query(DamageType)
                    .filter(DamageType.name == attribute)
                    .first()
                    for attribute in attributes["vulnerabilities"]
                ]
            if "parties" in attributes.keys():
                attributes["parties"] = [
                    session.query(Party).filter(Party.name == attribute).first()
                    for attribute in attributes["parties"]
                ]

            new_enemy = Enemy(name=enemy, **attributes)
            session.add(new_enemy)
            session.flush()

            # Adds classes and subclasses to CreatureClasses cross-reference table
            if classes:
                for cls in classes:
                    linked_subclasses = [
                        sc for sc in subclasses if sc.class_id == cls.id
                    ]
                    if linked_subclasses:
                        for subclass in linked_subclasses:
                            creature_class_entry = CreatureClasses(
                                creature_id=new_enemy.id,
                                class_id=cls.id,
                                subclass_id=subclass.id,
                            )
                            session.add(creature_class_entry)
                    else:
                        creature_class_entry = CreatureClasses(
                            creature_id=new_enemy.id, class_id=cls.id
                        )
                        session.add(creature_class_entry)
    session.commit()


def main() -> None:
    """
    Main function that runs to add initial data to the database.
    """
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
    create_pcs()
    create_npcs()
    create_enemies()


if __name__ == "__main__":
    main()
