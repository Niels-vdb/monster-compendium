from typing import Any, Dict

from sqlalchemy import Column, Integer, ForeignKey

from .creatures import Creature


class Enemy(Creature):
    """
    Table that holds all enemies the party has fought along their travels.
    Table inherits from Creature table.

    Parameters:
        - name (str): The name of the enemy.
        - description (str): Description about how the enemy looks like (optional).
        - information (str): Notes and extra information about the enemy (optional).
        - alive (bool): Boolean check if enemy is alive (True), or dead (False).
        - active (bool): Boolean check if the enemy is visible for party (True) or not (False).
        - armour_class (int): The armour class the enemy has (optional).
        - image (BLOB): An image of the enemy (optional).

        - race (int): The race of the creature, FK to id of the races table (optional).
        - subrace (int): The race of the creature, FK to id of the subraces table (optional).
        - size_id (int): The size of the creature, FK to id of the sizes table.
        - type_id (int): The type of the creature, FK to id of the types table (optional).

        - parties (List[Party]): The party(s) this creature belongs to. Linked to actual model, can be multiple (optional).
        - classes (List[Class]): The classes the creature belongs to, can be multiple (optional).
        - immunities (List[Effect]): The effects the creature is immune to, can be multiple (optional).
        - resistances (List[Effect]): The effects the creature is resistance to, can be multiple (optional).
        - vulnerabilities (List[Effect]): The effects the creature is vulnerable to, can be multiple (optional).
    """

    __tablename__ = "enemies"
    __mapper_args__ = {"polymorphic_identity": "enemies"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the enemy instance.
        :rtype: str
        """

        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, name={self.name!r}, "
            f"description={self.description!r}, information={self.information!r}, "
            f"alive={self.alive}, active={self.active}, "
            f"armour_class={self.armour_class}, image={self.image}, "
            f"race={self.race.name if self.race else 'None'}, "
            f"subrace={self.subrace.name if self.subrace else 'None'}, "
            f"size={self.size.name if self.size else 'None'}, "
            f"type={self.creature_type.name if self.creature_type else 'None'}, "
            f"parties={[party.name for party in self.parties]}, "
            f"classes={[cls.name for cls in self.classes]}, "
            f"subclasses={[subclass.name for subclass in self.subclasses]}, "
            f"immunities={[immunity.name for immunity in self.immunities]}, "
            f"resistances={[resistance.name for resistance in self.resistances]}, "
            f"vulnerabilities={[vul.name for vul in self.vulnerabilities]}"
            ")"
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the enemy instance.
        :rtype: Dict[str, Any]
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "race": self.race,
            "subrace": self.subrace,
            "size": self.size,
            "type": self.type_id,
            "parties": self.parties,
            "classes": [cls.to_dict() for cls in self.classes],
            "subclasses": [subcls.to_dict() for subcls in self.subclasses],
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }
