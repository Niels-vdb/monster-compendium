from typing import Any

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from server.config.logger_config import logger
from server.api.models.attribute import PostAttribute, PutAttribute
from server.api.models.creatures import PutClass, PutParty, PutSubclass
from server.api.models.damage_type import PostDamageType, PutDamageType
from server.models import Attribute
from server.models import (
    CreatureAdvantages,
    CreatureDisadvantages,
    CreatureImmunities,
    CreatureResistances,
    CreatureVulnerabilities,
)
from server.models import DamageType
from server.models import Party
from server.models import Size
from server.models import Type
from server.models import Class
from server.models import Subclass
from server.models import Race
from server.models import Subrace


class CreatureUtilities:
    def __init__(self, db: Session, entity: Any) -> None:
        """
        - **db** (Session): The database instance.
        - **entity** (Any): The entity that needs to be updated.
        """
        self.db = db
        self.entity = entity

    def _get_by_id(self, model: Any, object_id: int) -> Any:
        """
        Fetches an object by its ID.

        - **model** (Any): The database model.
        - **object_id** (int): The ID of the object.

        - **Returns**: The object if found, otherwise raises an HTTPException.
        """
        logger.debug(f"Getting {model.__name__} with id: {object_id}")
        object = self.db.get(model, object_id)

        if not object:
            model_name = (
                model.__name__ if model.__name__ != "DamageType" else "Damage type"
            )
            logger.error(
                f"No object found with id '{object_id}' in table '{model_name}'."
            )
            raise HTTPException(status_code=404, detail=f"{model_name} not found.")

        return object

    def update_race(self, race_id: int) -> None:
        """
        Updates an entity's race.

        - **race_id** (int): The id of the race
        """
        logger.debug(f"Trying to update race for '{self.entity.name}'")
        race = self._get_by_id(Race, race_id)
        self.entity.race_id = race.id

    def update_subrace(self, subrace_id: int) -> None:
        """
        Updates an entity's subrace.

        - **subrace_id** (int): The id of the subrace
        """
        logger.debug(f"Trying to update subrace for '{self.entity.name}'")
        subrace = self._get_by_id(Subrace, subrace_id)
        self.entity.subrace_id = subrace.id

    def update_size(self, size_id: int) -> Size:
        """
        Updates an entity's size.

        - **size_id** (int): The id of the size
        """
        logger.debug(f"Trying to update size for '{self.entity.name}'")
        size = self._get_by_id(Size, size_id)
        self.entity.size_id = size.id

    def update_type(self, type_id: int) -> None:
        """
        Updates an entity's type.

        - **type_id** (int): The id of the type
        """
        logger.debug(f"Trying to update type for '{self.entity.name}'")
        type = self._get_by_id(Type, type_id)
        self.entity.type_id = type.id

    def update_classes(self, classes: list[PutClass]) -> None:
        """
        Updates an entity's classes

        - **classes** (list[PutClass]): The classes that need to be changed formatted as:
        [
            {
                "class_id": int,
                "add_class": boolean,
            },
        ]
        """
        logger.debug(f"Trying to update classes for '{self.entity.name}'")
        for cls in classes:
            update_class = self._get_by_id(Class, cls.class_id)

            if cls.add_class:
                self.entity.classes += [update_class]
            else:
                if update_class in self.entity.classes:
                    self.entity.classes.remove(update_class)
        logger.debug(f"Changed classes of '{self.entity}'.")

    def update_subclasses(self, subclasses: list[PutSubclass]) -> None:
        """
        Updates an entity's subclasses

        - **subclasses** (list[PutSubclass]): The subclasses that need to be changed formatted as:
        [
            {
                "subclass_id": int,
                "add_subclass": boolean,
            },
        ]
        """
        logger.debug(f"Trying to update subclasses for '{self.entity.name}'")
        for subclass in subclasses:
            update_subclass = self._get_by_id(Subclass, subclass.subclass_id)

            if subclass.add_subclass:
                self.entity.subclasses += [update_subclass]
            else:
                if update_subclass in self.entity.subclasses:
                    self.entity.subclasses.remove(update_subclass)
        logger.debug(f"Changed subclasses of '{self.entity}'.")

    def update_parties(self, parties: list[PutParty]) -> None:
        """
        Updates an entity's parties

        - **parties** (list[PutParty]): The parties that need to be changed formatted as:
        [
            {
                "party_id": int,
                "add_party": boolean,
            },
        ]
        """
        logger.debug(f"Trying to update parties for '{self.entity.name}'")
        for party in parties:
            update_party = self._get_by_id(Party, party.party_id)

            if party.add_party:
                self.entity.parties += [update_party]
            else:
                if update_party in self.entity.parties:
                    logger.debug("Removing party")
                    self.entity.parties.remove(update_party)
        logger.debug(f"Changed parties of '{self.entity}'.")

    def update_immunities(self, immunities: list[PutDamageType]) -> None:
        """
        Updates an entity's immunities

        - **immunities** (list[PutDamageType]): The immunities that need to be
        changed formatted as:
        [
            {
                "damage_type_id": int,
                "add_damage_type": boolean,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to update immunities for '{self.entity.name}'")
        for immunity in immunities:
            damage_type = self._get_by_id(DamageType, immunity.damage_type_id)

            if immunity.add_damage_type:
                self._add_damage_type(
                    CreatureImmunities, damage_type.id, immunity.condition
                )
            else:
                self._delete_damage_type(CreatureImmunities, damage_type.id)
        logger.debug(f"Changed immunities of '{self.entity}'.")

    def add_immunities(self, immunities: list[PostDamageType]) -> None:
        """
        Creates an entity's immunities

        - **immunities** (list[PostDamageType]): The immunities that need to be
        added formatted as:
        [
            {
                "damage_type_id": int,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to add immunities to '{self.entity.name}'")
        for immunity in immunities:
            damage_type = self._get_by_id(DamageType, immunity.damage_type_id)

            self._add_damage_type(
                CreatureImmunities, damage_type.id, immunity.condition
            )
        logger.debug(f"Added immunities to '{self.entity}'.")

    def update_resistances(self, resistances: list[PutDamageType]) -> None:
        """
        Updates an entity's resistances

        - **resistances** (list[PutDamageType]): The resistances that need to be
        changed formatted as:
        [
            {
                "damage_type_id": int,
                "add_damage_type": boolean,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to update resistances for '{self.entity.name}'")
        for resistance in resistances:
            damage_type = self._get_by_id(DamageType, resistance.damage_type_id)

            if resistance.add_damage_type:
                self._add_damage_type(
                    CreatureResistances, damage_type.id, resistance.condition
                )
            else:
                self._delete_damage_type(CreatureResistances, damage_type.id)
        logger.debug(f"Changed resistances of '{self.entity}'.")

    def add_resistances(self, resistances: list[PostDamageType]) -> None:
        """
        Create an entity's resistances

        - **resistances** (list[PostDamageType]): The resistances that need to be
        added formatted as:
        [
            {
                "damage_type_id": int,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to add resistances to '{self.entity.name}'")
        for resistance in resistances:
            damage_type = self._get_by_id(DamageType, resistance.damage_type_id)

            self._add_damage_type(
                CreatureResistances, damage_type.id, resistance.condition
            )
        logger.debug(f"Added resistances to '{self.entity}'.")

    def update_vulnerabilities(self, vulnerabilities: list[PutDamageType]) -> None:
        """
        Updates an entity's vulnerabilities

        - **vulnerabilities** (list[PutDamageType]): The vulnerabilities that need to be
        changed formatted as:
        [
            {
                "damage_type_id": int,
                "add_damage_type": boolean,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to update vulnerabilities for '{self.entity.name}'")
        for vulnerability in vulnerabilities:
            damage_type = self._get_by_id(DamageType, vulnerability.damage_type_id)

            if vulnerability.add_damage_type:
                self._add_damage_type(
                    CreatureVulnerabilities, damage_type.id, vulnerability.condition
                )
            else:
                self._delete_damage_type(CreatureVulnerabilities, damage_type.id)
        logger.debug(f"Changed vulnerabilities of '{self.entity}'.")

    def add_vulnerabilities(self, vulnerabilities: list[PostDamageType]) -> None:
        """
        Creates an entity's vulnerabilities

        - **vulnerabilities** (list[PostDamageType]): The vulnerabilities that need to be
        added formatted as:
        [
            {
                "damage_type_id": int,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to add vulnerabilities to '{self.entity.name}'")
        for vulnerability in vulnerabilities:
            damage_type = self._get_by_id(DamageType, vulnerability.damage_type_id)

            self._add_damage_type(
                CreatureVulnerabilities, damage_type.id, vulnerability.condition
            )
        logger.debug(f"Changed vulnerabilities of '{self.entity}'.")

    def update_advantages(self, advantages: list[PutAttribute]) -> None:
        """
        Updates an entity's advantages

        - **advantages** (list[PutAttribute]): The advantages that need to be
        changed formatted as:
        [
            {
                "attribute_id": int,
                "add_attribute": boolean,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to update advantages for '{self.entity.name}'")
        for advantage in advantages:
            attribute = self._get_by_id(Attribute, advantage.attribute_id)

            if advantage.add_attribute:
                self._add_attribute(
                    CreatureAdvantages, attribute.id, advantage.condition
                )
            else:
                self._delete_attribute(CreatureAdvantages, attribute.id)
        logger.debug(f"Changed advantages of '{self.entity}'.")

    def add_advantages(self, advantages: list[PostAttribute]) -> None:
        """
        Creates an entity's advantages

        - **advantages** (list[PostAttribute]): The advantages that need to be
        added formatted as:
        [
            {
                "attribute_id": int,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to add advantages to '{self.entity.name}'")
        for advantage in advantages:
            attribute = self._get_by_id(Attribute, advantage.attribute_id)

            self._add_attribute(
                CreatureDisadvantages, attribute.id, advantage.condition
            )
        logger.debug(f"Added advantages of '{self.entity}'.")

    def update_disadvantages(self, disadvantages: list[PutAttribute]) -> None:
        """
        Updates an entity's disadvantages

        - **disadvantages** (list[PutAttribute]): The disadvantages that need to be
        changed formatted as:
        [
            {
                "attribute_id": int,
                "add_attribute": boolean,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to update disadvantages for '{self.entity.name}'")
        for disadvantage in disadvantages:
            attribute = self._get_by_id(Attribute, disadvantage.attribute_id)

            if disadvantage.add_attribute:
                self._add_attribute(
                    CreatureDisadvantages,
                    attribute.id,
                    disadvantage.condition,
                )
            else:
                self._delete_attribute(CreatureDisadvantages, attribute.id)
        logger.debug(f"Changed disadvantages of '{self.entity}'.")

    def add_disadvantages(self, disadvantages: list[PostAttribute]) -> None:
        """
        Creates an entity's disadvantages

        - **disadvantages** (list[PostAttribute]): The disadvantages that need to be
        added formatted as:
        [
            {
                "attribute_id": int,
                "condition": str
            },
        ]

        """
        logger.debug(f"Trying to add disadvantages to '{self.entity.name}'")
        for disadvantage in disadvantages:
            attribute = self._get_by_id(Attribute, disadvantage.attribute_id)

            self._add_attribute(
                CreatureAdvantages, attribute.id, disadvantage.condition
            )
        logger.debug(f"Added disadvantages of '{self.entity}'.")

    def _add_damage_type(
        self, model: Any, damage_type_id: int, condition: str = None
    ) -> None:
        """
        Adds a damage type to a creature

        - **model** (Any): The many to many model that holds the
                relationship between a creature and a damage type.
        - **damage_type_id** (int): The id of the damage type.

        - **condition** (str): The condition when this damage type is active (default: None)
        """
        new_damage_type = model(
            creature_id=self.entity.id,
            damage_type_id=damage_type_id,
            condition=condition,
        )
        self.db.add(new_damage_type)

    def _delete_damage_type(self, model: Any, damage_type_id: int) -> None:
        """
        Deletes a damage type from a creature

        - **model** (Any): The many to many model that holds the
                relationship between a creature and a damage type.
        - **damage_type_id** (int): The id of the damage type.
        """
        stmt = select(model).where(
            and_(
                model.creature_id == self.entity.id,
                model.damage_type_id == damage_type_id,
            )
        )
        old_damage_type = self.db.execute(stmt).scalar_one_or_none()
        self.db.delete(old_damage_type)

    def _add_attribute(
        self, model: Any, attribute_id: int, condition: str = None
    ) -> None:
        """
        Adds an attribute to a creature

        - **model** (Any): The many to many model that holds the
                relationship between a creature and an attribute.
        - **attribute_id** (int): The id of the attribute.

        - **condition** (str): The condition when this attribute is active (default: None)
        """
        new_disadvantage = model(
            creature_id=self.entity.id,
            attribute_id=attribute_id,
            condition=condition,
        )
        self.db.add(new_disadvantage)

    def _delete_attribute(self, model: Any, attribute_id: int) -> None:
        """
        Deletes an attribute from a creature

        - **model** (Any): The many to many model that holds the
                relationship between a creature and an attribute.
        - **attribute_id** (int): The id of the attribute.
        """
        stmt = select(model).where(
            and_(
                model.creature_id == self.entity.id,
                model.attribute_id == attribute_id,
            )
        )
        old_attribute = self.db.execute(stmt).scalar_one_or_none()
        self.db.delete(old_attribute)
