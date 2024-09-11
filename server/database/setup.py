from typing import Dict, List

from server.database.create import session
from server.database.models.creatures import CreatureClasses
from server.database.models.monsters import Monster
from server.database.models.player_characters import PlayerCharacter
from server.database.models.non_player_characters import NPCCharacter
from server.database.models.races import Race, Subrace
from server.database.models.classes import Class, Subclass
from server.database.models.characteristics import Size, Type
from server.database.models.effects import Effect
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
            "name": "admin",
            "roles": ["Admin", "Player"],
            "parties": ["Murder Hobo Party"],
        },
        "player": {
            "name": "player",
            "roles": ["Player"],
            "parties": ["Murder Hobo Party"],
        },
        "dungeonmaster": {
            "name": "dungeonmaster",
            "roles": ["Dungeon Master"],
            "parties": ["Murder Hobo Party"],
        },
    }

    for user, info in users.items():
        if not session.query(User).filter(User.name == user).first():
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


def initialize_effects() -> None:
    """
    All initial conditions and damage types to be added to the effects table.
    """
    effects: List[str] = [
        "Acid",
        "Blinded",
        "Bludgeoning",
        "Cold",
        "Charmed",
        "Deafened",
        "Fire",
        "Frightened",
        "Force",
        "Grappled",
        "Incapacitated",
        "Invisible",
        "Lightning",
        "Magic",
        "Necrotic",
        "Paralyzed",
        "Piercing",
        "Petrified",
        "Poison",
        "Poisoned",
        "Prone",
        "Psychic",
        "Radiant",
        "Restrained",
        "Slashing",
        "Stunned",
        "Thunder",
        "Unconscious",
        "Exhaustion",
    ]

    for effect in effects:
        if not session.query(Effect).filter(Effect.name == effect).first():
            print(f"Adding '{effect}' to the effects table in the database.")
            new_effect = Effect(name=effect)
            session.add(new_effect)
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
            "College of Glamour",
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
        "Aarakocra": {"size": ["medium"], "resistance": [""]},
        "Aasimar": {"size": ["medium", "small"], "resistance": [""]},
        "Bugbear": {"size": ["medium"], "resistance": [""]},
        "Centaur": {"size": ["medium"], "resistance": [""]},
        "Changeling": {"size": ["medium", "small"], "resistance": [""]},
        "Dragonborn": {"size": ["medium"], "resistance": [""]},
        "Dwarf": {"size": ["medium"], "resistance": [""]},
        "Elf": {"size": ["medium"], "resistance": [""]},
        "Gnome": {"size": ["small"], "resistance": [""]},
        "Fairy": {"size": ["small"], "resistance": [""]},
        "Firbolg": {"size": ["medium"], "resistance": [""]},
        "Genasi": {"size": ["medium", "small"], "resistance": [""]},
        "Githyanki": {"size": ["medium"], "resistance": ["psychic"]},
        "Githzerai": {"size": ["medium"], "resistance": ["psychic"]},
        "Goblin": {"size": ["small"], "resistance": [""]},
        "Goliath": {"size": ["medium"], "resistance": ["cold"]},
        "Half-Elf": {"size": ["medium"], "resistance": [""]},
        "Half-Orc": {"size": ["medium"], "resistance": [""]},
        "Halfling": {"size": ["small"], "resistance": [""]},
        "Harengon": {"size": ["medium", "small"], "resistance": [""]},
        "Hobgoblin": {"size": ["medium"], "resistance": [""]},
        "Human": {"size": ["medium"], "resistance": [""]},
        "Kenku": {"size": ["medium", "small"], "resistance": [""]},
        "Kobold": {"size": ["small"], "resistance": [""]},
        "Lizard folk": {"size": ["medium"], "resistance": [""]},
        "Minotaur": {"size": ["medium"], "resistance": [""]},
        "Orc": {"size": ["medium"], "resistance": [""]},
        "Satyr": {"size": ["medium"], "resistance": [""]},
        "Shifter": {"size": ["medium"], "resistance": [""]},
        "Tabaxi": {"size": ["medium", "small"], "resistance": [""]},
        "Tiefling": {"size": ["medium"], "resistance": ["fire"]},
        "Thylean Centaur": {"size": ["medium"], "resistance": [""]},
        "Thylean Medusa": {"size": ["medium"], "resistance": [""]},
        "Thylean Minotaur": {"size": ["medium"], "resistance": [""]},
        "Thylean Nymph": {"size": ["medium"], "resistance": [""]},
        "Thylean Satyr": {"size": ["medium"], "resistance": [""]},
        "Thylean Siren": {"size": ["medium"], "resistance": [""]},
        "Tortle": {"size": ["medium", "small"], "resistance": [""]},
        "Triton": {"size": ["medium"], "resistance": ["cold"]},
        "Yuan-ti": {"size": ["medium", "small"], "resistance": ["poison"]},
    }
    for race, values in races.items():
        if not session.query(Race).filter(Race.name == race).first():
            print(f"Adding '{race}' to the races table in the database.")
            size_list = [
                session.query(Size).filter(Size.name == size.capitalize()).first()
                for size in values["size"]
            ]
            resistance_list = [
                session.query(Effect)
                .filter(Effect.name == resistance.capitalize())
                .first()
                for resistance in values["resistance"]
            ]
            resistance_list = [
                resistance for resistance in resistance_list if resistance is not None
            ]
            for size in size_list:
                new_race = Race(name=race, size_id=size.id, resistances=resistance_list)
                session.add(new_race)
        session.commit()


def initialize_subraces() -> None:
    """
    All initial subraces to be added to the subraces table and linked to a race.
    """
    subraces: Dict[str, Dict[str, List[str]]] = {
        "Dragonborn": {
            "Black": {"resistance": ["acid"]},
            "Blue": {"resistance": ["lightning"]},
            "Brass": {"resistance": ["fire"]},
            "Bronze": {"resistance": ["lightning"]},
            "Copper": {"resistance": ["acid"]},
            "Gold": {"resistance": ["fire"]},
            "Green": {"resistance": ["poison"]},
            "Red": {"resistance": ["fire"]},
            "Silver": {"resistance": ["cold"]},
            "White": {"resistance": ["cold"]},
        },
        "Dwarf": {
            "Duergar": {"resistance": ["charmed", "stunned", "poison"]},
            "Mountain": {"resistance": ["poison"]},
            "Hill": {"resistance": ["poison"]},
        },
        "Elf": {
            "Astral": {"resistance": [""]},
            "Bishtahar/Tirahar": {"resistance": [""]},
            "Dark": {"resistance": [""]},
            "Eladrin": {"resistance": [""]},
            "High": {"resistance": [""]},
            "Sea Elf": {"resistance": [""]},
            "Shadar-kai": {"resistance": ["necrotic", "charmed"]},
            "Pallid": {"resistance": [""]},
            "Vahadar": {"resistance": [""]},
            "Wood": {"resistance": [""]},
            "Zendikar": {"resistance": [""]},
        },
        "Genasi": {
            "Air": {"resistance": ["lightning"]},
            "Earth": {"resistance": [""]},
            "Fire": {"resistance": ["fire"]},
            "Water": {"resistance": ["acid"]},
        },
        "Gnome": {
            "Deep": {"resistance": [""]},
            "Forest": {"resistance": [""]},
            "Rock": {"resistance": [""]},
        },
        "Halfling": {
            "Ghostwise": {"resistance": [""]},
            "Lightfoot": {"resistance": [""]},
            "Lotusden": {"resistance": [""]},
            "Stout": {"resistance": ["poison"]},
        },
        "Human": {
            "Variant": {"resistance": [""]},
        },
        "Tiefling": {
            "Abyssal Tiefling": {"resistance": [""]},
            "Bloodline of Asmodeus": {"resistance": [""]},
            "Bloodline of Baalzebul": {"resistance": [""]},
            "Bloodline of Dispater": {"resistance": [""]},
            "Bloodline of Fierna": {"resistance": [""]},
            "Bloodline of Glasya": {"resistance": [""]},
            "Bloodline of Levistus": {"resistance": [""]},
            "Bloodline of Mammon": {"resistance": [""]},
            "Bloodline of Mephistopheles": {"resistance": [""]},
            "Bloodline of Zariel": {"resistance": [""]},
            "Variant Tiefling": {"resistance": [""]},
        },
        "Thylean Nymph": {
            "Aurae": {"resistance": [""]},
            "Dryad": {"resistance": [""]},
            "Naiad": {"resistance": [""]},
            "Nereid": {"resistance": [""]},
            "Oread": {"resistance": [""]},
        },
    }

    for race, subraces in subraces.items():
        parent_race = session.query(Race).filter(Race.name == race.title()).first()

        for subrace in subraces:
            if not session.query(Subrace).filter(Subrace.name == subrace).first():
                print(
                    f"Adding subrace '{subrace}' of race '{race}' to the subraces table in the database."
                )
                resistances = list(subraces[subrace].values())
                resistance_list = [
                    session.query(Effect)
                    .filter(Effect.name == resistance[0].capitalize())
                    .first()
                    for resistance in resistances
                ]
                resistance_list = [
                    resistance
                    for resistance in resistance_list
                    if resistance is not None
                ]

                new_subrace = Subrace(
                    name=subrace, race=parent_race, resistances=resistance_list
                )
                session.add(new_subrace)
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
    Creates two player characters with attributes and adds them to the pc_characters table.
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
            "race": "Thylean Centaur",
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
            "race": "Thylean Nymph",
            "subrace": "Naiad",
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
            if "race" in attributes.keys():
                attributes["race"] = (
                    session.query(Race)
                    .filter(Race.name == attributes["race"])
                    .first()
                    .id
                )
            if "subrace" in attributes.keys():
                attributes["subrace"] = (
                    session.query(Subrace)
                    .filter(Subrace.name == attributes["subrace"])
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
                    .filter(User.name == attributes["user"])
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
    Creates two non player characters with attributes and adds them to the npc_characters table.
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
        if not session.query(NPCCharacter).filter(NPCCharacter.name == npc).first():
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

            new_npc = NPCCharacter(name=npc, **attributes)
            session.add(new_npc)
    session.commit()


def create_monsters() -> None:
    """
    Creates two monster characters with attributes and adds them to the monsters table.
    """
    monsters: Dict[str, dict[str, str]] = {
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

    for monster, attributes in monsters.items():
        if not session.query(Monster).filter(Monster.name == monster).first():
            print(
                f"Adding '{monster}' to monsters table in the database with the following attributes: {attributes}."
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
                    session.query(Effect).filter(Effect.name == attribute).first()
                    for attribute in attributes["resistances"]
                ]
            if "immunities" in attributes.keys():
                attributes["immunities"] = [
                    session.query(Effect).filter(Effect.name == attribute).first()
                    for attribute in attributes["immunities"]
                ]
            if "vulnerabilities" in attributes.keys():
                attributes["vulnerabilities"] = [
                    session.query(Effect).filter(Effect.name == attribute).first()
                    for attribute in attributes["vulnerabilities"]
                ]
            if "parties" in attributes.keys():
                attributes["parties"] = [
                    session.query(Party).filter(Party.name == attribute).first()
                    for attribute in attributes["parties"]
                ]

            new_monster = Monster(name=monster, **attributes)
            session.add(new_monster)
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
                                creature_id=new_monster.id,
                                class_id=cls.id,
                                subclass_id=subclass.id,
                            )
                            session.add(creature_class_entry)
                    else:
                        creature_class_entry = CreatureClasses(
                            creature_id=new_monster.id, class_id=cls.id
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
    initialize_effects()
    initialize_classes()
    initialize_subclasses()
    initialize_races()
    initialize_subraces()
    initialize_types()
    create_pcs()
    create_npcs()
    create_monsters()


if __name__ == "__main__":
    main()
