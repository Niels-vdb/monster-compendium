from typing import Any, Dict, List

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
        "Satyr": {"size": ["medium"], "resistance": ["magic"]},
        "Shifter": {"size": ["medium"], "resistance": [""]},
        "Tabaxi": {"size": ["medium", "small"], "resistance": [""]},
        "Tiefling": {"size": ["medium"], "resistance": [""]},
        "Thylean Centaur": {"size": ["medium"], "resistance": [""]},
        "Thylean Medusa": {"size": ["medium"], "resistance": [""]},
        "Thylean Minotaur": {"size": ["medium"], "resistance": [""]},
        "Thylean Nymph": {"size": ["medium"], "resistance": [""]},
        "Thylean Satyr": {"size": ["medium"], "resistance": [""]},
        "Thylean Siren": {"size": ["medium"], "resistance": [""]},
        "Tortle": {"size": ["medium", "small"], "resistance": [""]},
        "Triton": {"size": ["medium"], "resistance": ["cold"]},
        "Yuan-ti": {"size": ["medium", "small"], "resistance": ["poison", "magic"]},
    }


def initialize_subraces():
    """
    All initial subraces to be added to the database and linked to a race.
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
            "Abyssal Tiefling": {"resistance": ["fire"]},
            "Bloodline of Asmodeus": {"resistance": ["fire"]},
            "Bloodline of Baalzebul": {"resistance": ["fire"]},
            "Bloodline of Dispater": {"resistance": ["fire"]},
            "Bloodline of Fierna": {"resistance": ["fire"]},
            "Bloodline of Glasya": {"resistance": ["fire"]},
            "Bloodline of Levistus": {"resistance": ["fire"]},
            "Bloodline of Mammon": {"resistance": ["fire"]},
            "Bloodline of Mephistopheles": {"resistance": ["fire"]},
            "Bloodline of Zariel": {"resistance": ["fire"]},
            "Variant Tiefling": {"resistance": ["fire"]},
        },
        "Thylean Nymph": {
            "Aurae": {"resistance": [""]},
            "Dryad": {"resistance": [""]},
            "Naiad": {"resistance": [""]},
            "Nereid": {"resistance": [""]},
            "Oread": {"resistance": [""]},
        },
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
        "Magic" "Necrotic",
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
