from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Classes(Base):
    """
    Table that holds all classes a character can have.

    Parameters:
        - name (str): The name of the class.
    """

    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    subclass = relationship(
        "Subclasses", back_populates="parent_class", passive_deletes=True
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Class instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.class_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Class instance.
        :rtype: Dict[str, Any]
        """
        return {"class_id": self.class_id, "name": self.name}


class Subclasses(Base):
    """
    Table that holds all subclasses that can belong to a class.

    Parameters:
        - name (str): The name of the subclass.
    """

    __tablename__ = "subclasses"

    subclass_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.class_id", ondelete="CASCADE"))

    parent_class = relationship("Classes", back_populates="subclass")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Subclass instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.subclass_id}', 
                '{self.name}', '{self.class_id}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Subclass instance.
        :rtype: Dict[str, Any]
        """
        return {
            "subclass_id": self.class_id,
            "name": self.name,
            "class_id": self.class_id,
        }


class Races(Base):
    """
    Table that holds all races a character can have.

    Parameters:
        - name (str): The name of the race.
        - size_id (int): FK to sizes table holding the PK of the size of this race.
    """

    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    size_id = Column(Integer, ForeignKey("sizes.size_id"))

    subrace = relationship(
        "Subraces", back_populates="parent_race", passive_deletes=True
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Race instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.race_id}', 
                '{self.name}', '{self.size_id}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Race instance.
        :rtype: Dict[str, Any]
        """
        return {"race_id": self.race_id, "name": self.name, "size_id": self.size_id}


class Subraces(Base):
    """
    Table that holds all subraces that a race can have.

    Parameters:
        - name (str): The name of the subrace.
        - race_id (int): FK to sizes table holding the PK of the race this subrace belongs to.
    """

    __tablename__ = "subraces"

    subrace_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    race_id = Column(Integer, ForeignKey("races.race_id", ondelete="CASCADE"))

    # Define relationships
    race = relationship("Races", backref="subraces")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Subrace instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}('{self.subrace_id}', 
                '{self.name}', '{self.race_id}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Subrace instance.
        :rtype: Dict[str, Any]
        """
        return {
            "subrace_id": self.subrace_id,
            "name": self.name,
            "race_id": self.race_id,
        }


class Sizes(Base):
    """
    Table that holds all sizes a character can have.

    Parameters:
        - name (str): The name of the size.
    """

    __tablename__ = "sizes"

    size_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Size instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.size_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Size instance.
        :rtype: Dict[str, Any]
        """
        return {"size_id": self.size_id, "size": self.name}


class Effects(Base):
    """
    Table that holds all the effects a character can have a venerability,
    immunity or resistance to.

    Parameters:
        - name (str): The name of the effect.
    """

    __tablename__ = "effects"

    effect_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Effect instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.effect_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Effect instance.
        :rtype: Dict[str, Any]
        """
        return {"effect_id": self.effect_id, "effect": self.name}
