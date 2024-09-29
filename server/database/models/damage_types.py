from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import CustomBase


class DamageType(CustomBase):
    """
    Table that holds all the damage types a character can have a vulnerability, immunity or resistance to.
    Like a melee attack type such as slashing or a damage type like fire.

    Parameters:
        - name (str): The name of the damage type (max 50 chars).
    """

    __tablename__ = "damage_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # n-n relationships
    race_resistances = relationship(
        "Race",
        secondary="race_resistances",
        back_populates="resistances",
    )
    race_immunities = relationship(
        "Race",
        secondary="race_immunities",
        back_populates="immunities",
    )
    race_vulnerabilities = relationship(
        "Race",
        secondary="race_vulnerabilities",
        back_populates="vulnerabilities",
    )
    subrace_resistances = relationship(
        "Subrace",
        secondary="subrace_resistances",
        back_populates="resistances",
    )
    subrace_immunities = relationship(
        "Subrace",
        secondary="subrace_immunities",
        back_populates="immunities",
    )
    subrace_vulnerabilities = relationship(
        "Subrace",
        secondary="subrace_vulnerabilities",
        back_populates="vulnerabilities",
    )
    creature_resistances = relationship(
        "Creature",
        secondary="creature_resistances",
        back_populates="resistances",
    )
    creature_immunities = relationship(
        "Creature",
        secondary="creature_immunities",
        back_populates="immunities",
    )
    creature_vulnerabilities = relationship(
        "Creature",
        secondary="creature_vulnerabilities",
        back_populates="vulnerabilities",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the DamageType instance.
        :rtype: str
        """
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"
