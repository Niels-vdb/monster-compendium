from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.api import get_db
from server.logger.logger import logger
from server.database.models.users import User
from server.api.models.base_response import BaseResponse


router = APIRouter(
    prefix="/logout",
    tags=["Authentication"],
    responses={404: {"description": "Not found."}},
)


@router.delete("/{user_id}", response_model=BaseResponse)
def logout_user(user_id: int, db: Session = Depends(get_db)) -> BaseResponse:
    """
    Endpoint used for logging out to the application.

    - `user_id`: An integer representing the user id (inclusive).

    - **Returns** BaseResponse: A dictionary holding a message.

    - **HTTPException**: If the user id does not exists.

    **Response Example**:
    ```json
    {
        "message": "Your logged out of the application. Goodbye.",
    }
    ```
    """
    logger.info(f"User trying to log out with user id: '{user_id}'.")
    logout_user = db.get(User, user_id)

    if not logout_user:
        logger.error(f"No user found with the following id: {user_id}.")
        raise HTTPException(
            status_code=404,
            detail="The id you try to log out with does not exist.",
        )
    return BaseResponse(
        message="Your logged out of the application. Goodbye.",
    )
