from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import CustomBase


class Subclass(CustomBase):
    """
    Table that holds all subclasses that can belong to a class.
    Subclass names cannot be repeated with the same class_id FK.

    Parameters:
        - name (str): The name of the subclass (max 100 chars).
        - class_id (int): The class id of the class this subclass belongs to.
    """

    __tablename__ = "subclasses"
    __table_args__ = (UniqueConstraint("name", "class_id", name="_name_class_id_uc"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"))

    # n-1 relationships
    parent_class = relationship("Class", back_populates="subclasses")

    # n-n relationships
    creatures = relationship(
        "Creature",
        secondary="creature_classes",
        back_populates="subclasses",
        overlaps="classes,creatures",
    )

    def __repr__(self) -> str:
        """
        This method provides a readable string of the Subclass instance including
        all its attributes.

        :returns: A string representation of the Subclass instance.
        :rtype: str
        """
        return f"""{self.__class__.__tablename__}(id={self.id},
            name={self.name}, parent_class={self.parent_class})"""
