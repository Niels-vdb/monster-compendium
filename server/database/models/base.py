from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CustomBase(Base):
    """
    Abstract base class all ORM models will inherit from.
    """

    __abstract__ = True

    def to_dict(self) -> dict[str, str | int]:
        """
        Convert model instance to a dictionary.
        """
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
