from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from .base import Base


class Classes(Base):
    __tablename__ = "Classes"
    class_id = Column("Class_id", Integer, primary_key=True)


class Subclasses(Base):
    __tablename__ = "Subclasses"
    subclass_id = Column("Subclass_id", Integer, primary_key=True)
    class_id = Column("Class_id", Integer, ForeignKey("Classes.Class_id"))


class Races(Base):
    __tablename__ = "Races"
    race_id = Column("Race_id", Integer, primary_key=True)
    name = Column("Name", String(20), nullable=False)


class Subraces(Base):
    __tablename__ = "Subraces"
    subrace_id = Column("Subrace_id", Integer, primary_key=True)
    name = Column("Name", String, nullable=False)
    race_id = Column("Race_id", Integer, ForeignKey("Races.Race_id"))


class Sizes(Base):
    __tablename__ = "Sizes"
    size_id = Column("Size_id", Integer, primary_key=True)
    size = Column("Size", String(20), nullable=False)


class Effects(Base):
    __tablename__ = "Effects"
    effect_id = Column("Effect_id", Integer, primary_key=True)
    effect = Column("Effect", Text, nullable=False)
