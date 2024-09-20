from typing import Any
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from server.database.models.creatures import (
    CreatureAdvantages,
    CreatureDisadvantages,
    CreatureImmunities,
    CreatureResistances,
    CreatureVulnerabilities,
)

from ..main import app
from .. import get_db

from server.database.models.base import Base
from server.database.models.enemies import Enemy
from server.database.models.player_characters import PlayerCharacter
from server.database.models.non_player_characters import NonPlayerCharacter
from server.database.models.races import Race
from server.database.models.subraces import Subrace
from server.database.models.classes import Class, Subclass
from server.database.models.characteristics import Size, Type
from server.database.models.damage_types import DamageType
from server.database.models.attributes import Attribute
from server.database.models.users import User, Party, Role


SQLALCHEMY_DATABASE_URL = "sqlite://"


# Fixture to create a fresh in-memory database for each test
@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)  # Create tables before each test
    yield engine
    Base.metadata.drop_all(bind=engine)  # Drop tables after each test
    engine.dispose()


# Fixture to provide a fresh database session for each test
@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Override the dependency in FastAPI to use this session
@pytest.fixture(scope="function", autouse=True)
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = _override_get_db
    yield


@pytest.fixture
def create_party(db_session):
    new_party = Party(name="Murder Hobo Party")
    db_session.add(new_party)
    db_session.commit()
    return new_party


@pytest.fixture
def create_role(db_session):
    new_role = Role(name="Player")
    db_session.add(new_role)
    db_session.commit()
    return new_role


@pytest.fixture
def create_user(db_session, create_role, create_party):
    user = "test"
    username = "Test"
    new_user = User(
        username=username, name=user, roles=[create_role], parties=[create_party]
    )
    db_session.add(new_user)
    db_session.commit()

    return new_user


@pytest.fixture
def create_damage_type(db_session):
    new_damage_type = DamageType(name="Fire")
    db_session.add(new_damage_type)
    db_session.commit()
    return new_damage_type


@pytest.fixture
def create_attribute(db_session):
    new_attribute = Attribute(name="Charmed")
    db_session.add(new_attribute)
    db_session.commit()
    return new_attribute


@pytest.fixture
def create_size(db_session):
    new_type = Size(name="Tiny")
    db_session.add(new_type)
    db_session.commit()
    return new_type


@pytest.fixture
def create_class(db_session):
    new_class = Class(name="Artificer")
    db_session.add(new_class)
    db_session.commit()
    return new_class


@pytest.fixture
def create_subclass(create_class, db_session):
    new_subclass = Subclass(name="Alchemist", class_id=create_class.id)
    db_session.add(new_subclass)
    db_session.commit()
    return new_subclass


@pytest.fixture
def create_race(create_size, db_session):
    new_race = Race(name="Dwarf", sizes=[create_size])
    db_session.add(new_race)
    db_session.commit()
    return new_race


@pytest.fixture
def create_subrace(create_race, db_session):
    new_subrace = Subrace(name="Duergar", race_id=create_race.id)
    db_session.add(new_subrace)
    db_session.commit()
    return new_subrace


@pytest.fixture
def create_type(db_session):
    new_type = Type(name="Aberration")
    db_session.add(new_type)
    db_session.commit()
    return new_type


@pytest.fixture
def create_npc(
    create_size,
    create_party,
    create_class,
    create_subclass,
    create_damage_type,
    create_attribute,
    create_type,
    db_session,
):
    npc = "Fersi (Oracle)"
    attributes: dict[str, Any] = {}
    attributes["size_id"] = create_size.id
    attributes["type_id"] = create_type.id
    attributes["parties"] = [create_party]
    attributes["description"] = "A demigod female."
    attributes["information"] = "Some say she knows everything, but shares very little."
    attributes["armour_class"] = 16
    attributes["walking_speed"] = 30
    attributes["swimming_speed"] = 25
    attributes["flying_speed"] = 5
    attributes["classes"] = [create_class]
    attributes["subclasses"] = [create_subclass]
    attributes["size_id"] = create_size.id
    attributes["type_id"] = create_type.id

    new_npc = NonPlayerCharacter(name=npc, **attributes)
    db_session.add(new_npc)
    db_session.commit()

    immunity = CreatureImmunities(
        creature_id=new_npc.id,
        damage_type_id=create_damage_type.id,
        condition="When in rage",
    )
    resistance = CreatureResistances(
        creature_id=new_npc.id,
        damage_type_id=create_damage_type.id,
        condition="When wearing a shield",
    )
    vulnerability = CreatureVulnerabilities(
        creature_id=new_npc.id,
        damage_type_id=create_damage_type.id,
        condition="When wearing armour",
    )
    advantages = CreatureAdvantages(
        creature_id=new_npc.id,
        attribute_id=create_attribute.id,
        condition="When wearing armour",
    )
    disadvantages = CreatureDisadvantages(
        creature_id=new_npc.id,
        attribute_id=create_attribute.id,
        condition="When not wearing armour",
    )
    db_session.add_all(
        [
            immunity,
            resistance,
            vulnerability,
            advantages,
            disadvantages,
        ]
    )
    db_session.commit()

    return new_npc


@pytest.fixture
def create_pc(
    create_user,
    create_party,
    create_class,
    create_subclass,
    create_race,
    create_subrace,
    create_size,
    create_type,
    create_damage_type,
    create_attribute,
    db_session,
):
    pc = "Rhoetus"
    attributes: dict[str, Any] = {}
    attributes["user"] = create_user
    attributes["parties"] = [create_party]
    attributes["description"] = "A centaur barbarian."
    attributes["information"] = "Some information about Rhoetus."
    attributes["armour_class"] = 17
    attributes["walking_speed"] = 40
    attributes["swimming_speed"] = 10
    attributes["flying_speed"] = 0
    attributes["classes"] = [create_class]
    attributes["subclasses"] = [create_subclass]
    attributes["race"] = create_race.id
    attributes["subrace"] = create_subrace.id
    attributes["size_id"] = create_size.id
    attributes["type_id"] = create_type.id

    new_pc = PlayerCharacter(name=pc, **attributes)
    db_session.add(new_pc)
    db_session.commit()

    immunity = CreatureImmunities(
        creature_id=new_pc.id,
        damage_type_id=create_damage_type.id,
        condition="When in rage",
    )
    resistance = CreatureResistances(
        creature_id=new_pc.id,
        damage_type_id=create_damage_type.id,
        condition="When wearing a shield",
    )
    vulnerability = CreatureVulnerabilities(
        creature_id=new_pc.id,
        damage_type_id=create_damage_type.id,
        condition="When wearing armour",
    )
    advantages = CreatureAdvantages(
        creature_id=new_pc.id,
        attribute_id=create_attribute.id,
        condition="When wearing armour",
    )
    disadvantages = CreatureDisadvantages(
        creature_id=new_pc.id,
        attribute_id=create_attribute.id,
        condition="When not wearing armour",
    )
    db_session.add_all(
        [
            immunity,
            resistance,
            vulnerability,
            advantages,
            disadvantages,
        ]
    )
    db_session.commit()

    return new_pc


@pytest.fixture
def create_enemy(
    create_party,
    create_class,
    create_subclass,
    create_size,
    create_type,
    create_damage_type,
    create_attribute,
    db_session,
):
    enemy = "Giff"
    attributes: dict[str, Any] = {}
    attributes["parties"] = [create_party]
    attributes["description"] = "A large hippo like creature"
    attributes["information"] = (
        "Some information about this big hippo, like his knowledge about firearms."
    )
    attributes["armour_class"] = 16
    attributes["walking_speed"] = 30
    attributes["swimming_speed"] = 20
    attributes["flying_speed"] = 0
    attributes["classes"] = [create_class]
    attributes["subclasses"] = [create_subclass]
    attributes["size_id"] = create_size.id
    attributes["type_id"] = create_type.id

    new_enemy = Enemy(name=enemy, **attributes)
    db_session.add(new_enemy)
    db_session.commit()
    immunity = CreatureImmunities(
        creature_id=new_enemy.id,
        damage_type_id=create_damage_type.id,
        condition="When in rage",
    )
    resistance = CreatureResistances(
        creature_id=new_enemy.id,
        damage_type_id=create_damage_type.id,
        condition="When wearing a shield",
    )
    vulnerability = CreatureVulnerabilities(
        creature_id=new_enemy.id,
        damage_type_id=create_damage_type.id,
        condition="When wearing armour",
    )
    advantages = CreatureAdvantages(
        creature_id=new_enemy.id,
        attribute_id=create_attribute.id,
        condition="When wearing armour",
    )
    disadvantages = CreatureDisadvantages(
        creature_id=new_enemy.id,
        attribute_id=create_attribute.id,
        condition="When not wearing armour",
    )
    db_session.add_all(
        [
            immunity,
            resistance,
            vulnerability,
            advantages,
            disadvantages,
        ]
    )
    db_session.commit()
    return new_enemy
