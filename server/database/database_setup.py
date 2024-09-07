from typing import Dict, List

import bcrypt

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


def initialize_roles():
    """
    Creates the roles and add them to the database.
    """
    roles: List[str] = ["Admin", "Player"]


def create_admin():
    """
    Create an initial admin account to the database.
    """
    username = "admin"
    password = b"password"
    encrypted_psw = bcrypt.hashpw(password, bcrypt.gensalt())
    # Get admin ID from Roles table.


def initialize_classes():
    """
    All initial classes to be added to the database.
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


def initialize_subclasses():
    """
    All initial subclasses to be added to the database and linked to classes.
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


def initialize_races():
    """
    All initial races to be added to the database
    """
    races: List[str] = [
        "Aarakocra",
        "Aasimar",
        "Bugbear",
        "Centaur",
        "Changeling",
        "Dragonborn",
        "Dwarf",
        "Elf",
        "Gnome",
        "Fairy",
        "Firbolg",
        "Genasi",
        "Githyanki",
        "Githzerai",
        "Goblin",
        "Goliath",
        "Half-Elf",
        "Half-Orc",
        "Halfling",
        "Harengon",
        "Hobgoblin",
        "Human",
        "Kenku",
        "Kobold",
        "Lizard folk",
        "Minotaur",
        "Orc",
        "Satyr",
        "Shifter",
        "Tabaxi",
        "Tiefling",
        "Thylean Centaur",
        "Thylean Medusa",
        "Thylean Minotaur",
        "Thylean Nymph",
        "Thylean Satyr",
        "Thylean Siren",
        "Tortle",
        "Triton",
        "Yuan-ti",
    ]


def initialize_subraces():
    """
    All initial subraces to be added to the database and linked to a race.
    """
    subraces: Dict[str, str] = {
        "Dragonborn": [
            "Black",
            "Blue",
            "Brass",
            "Bronze",
            "Copper",
            "Gold",
            "Green",
            "Red",
            "Silver",
            "White",
        ],
        "Dwarf": [
            "Duergar",
            "Mountain",
            "Hill",
        ],
        "Elf": [
            "Astral",
            "Bishtahar/Tirahar",
            "Dark",
            "Eladrin",
            "High",
            "Sea Elf",
            "Shadar-kai",
            "Pallid",
            "Vahadar",
            "Wood",
            "Zendikar",
        ],
        "Genasi": [
            "Air",
            "Earth",
            "Fire",
            "Water",
        ],
        "Gnome": [
            "Deep",
            "Forest",
            "Rock",
        ],
        "Halfling": [
            "Ghostwise",
            "Lightfoot",
            "Lotusden",
            "Stout",
        ],
        "Human": [
            "Variant",
        ],
        "Tiefling": [
            "Abyssal Tiefling",
            "Bloodline of Asmodeus",
            "Bloodline of Baalzebul",
            "Bloodline of Dispater",
            "Bloodline of Fierna",
            "Bloodline of Glasya",
            "Bloodline of Levistus",
            "Bloodline of Mammon",
            "Bloodline of Mephistopheles",
            "Bloodline of Zariel",
            "Variant Tiefling",
        ],
        "Thylean Nymph": [
            "Aurae",
            "Dryad",
            "Naiad",
            "Nereid",
            "Oread",
        ],
    }


def initialize_sizes():
    """
    All initial sizes to be added to the database.
    """
    sizes: List[str] = [
        "Tiny",
        "Small",
        "Medium",
        "Large",
        "Huge",
        "Gargantuan",
    ]


def initialize_effects():
    """
    All initial conditions and damage types to be added to the database.
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


def initialize_types():
    """
    All initial monster types to be added to the database.
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


def main():
    """
    Main function that runs to add initial data to the database.
    """
    initialize_classes()
    initialize_subclasses()
    initialize_races()
    initialize_subraces()
    initialize_sizes()
    initialize_effects()


if __name__ == "__main__":
    main()
