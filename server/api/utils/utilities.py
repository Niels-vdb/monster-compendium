from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.logger.logger import logger


class Utilities:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, model: Any, object_id: int) -> Any:
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
