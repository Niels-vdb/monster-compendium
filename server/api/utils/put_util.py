from typing import Any
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.database.models.characteristics import Size, Type
from server.database.models.races import Race
from server.database.models.subraces import Subrace


class PutUtilities:
    def __init__(self, db: Session, entity: Any) -> None:
        """
        - **db** (Session): The database instance.
        - **entity** (Any): The entity that needs to be updated.
        """
        self.db = db
        self.entity = entity

    def _get_by_id(self, model: Any, obj_id: int) -> Any:
        """
        Fetches an object by its ID.

        - **model** (Any): The database model.
        - **object_id** (int): The ID of the object.

        - **Returns**: The object if found, otherwise raises an HTTPException.
        """
        stmt = select(model).where(model.id == obj_id)
        object = self.db.execute(stmt).scalar_one_or_none()
        if not object:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")

        return object

    def put_race(self, race_id: int) -> None:
        """
        Gets a race from the database by its id.

        - **race_id** (int): The id of the race
        """
        race = self._get_by_id(Race, race_id)
        self.entity.race_id = race.id

    def put_subrace(self, subrace_id: int) -> None:
        """
        Gets a subrace from the database by its id.

        - **subrace_id** (int): The id of the subrace
        """
        subrace = self._get_by_id(Subrace, subrace_id)
        self.entity.subrace_id = subrace.id

    def put_size(self, size_id: int) -> Size:
        """
        Gets a size from the database by its id.

        - **size_id** (int): The id of the size
        """
        size = self._get_by_id(Size, size_id)
        self.entity.size_id = size.id

    def put_type(self, type_id: int) -> None:
        """
        Gets a type from the database by its id.

        - **type_id** (int): The id of the type
        """
        type = self._get_by_id(Type, type_id)
        self.entity.type_id = type.id
