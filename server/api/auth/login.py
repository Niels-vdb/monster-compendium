from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from server.api import get_db
from server.logger.logger import logger
from server.database.models.users import User
from server.api.models.login import LoginModel
from server.api.models.base_response import BaseResponse
from server.api.utils.user_utilities import verify_password


router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
    responses={404: {"description": "Not found."}},
)


@router.post("/", response_model=BaseResponse)
def login_user(
    user: LoginModel, response: Response, db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Endpoint used for logging in to the application. When successful it set a cookie with the user id.

    - **Returns** BaseResponse: A dictionary holding a message.

    - **HTTPException**: If the username does not exists.
    - **HTTPException**: If the password is incorrect.

    **Request Body Example**:
    ```json
    {
        "username": "example_username",
        "password": "example_password",
    }
    ```
    - `username`: A string between 1 and 50 characters long (inclusive).
    - `password`: A string between 1 and 50 characters long (optional).

    **Response Example**:
    ```json
    {
        "message": "Your logged in with valid credentials. Welcome.",
    }
    ```
    """
    try:
        logger.info(f"User trying to log in with username: '{user.username}'.")
        stmt = select(User).where(User.username == user.username)
        login_user = db.execute(stmt).scalar_one_or_none()

        if not login_user:
            logger.error(f"No user found with the following username: {user.username}.")
            raise HTTPException(
                status_code=404,
                detail="The username you try to log in with does not exist.",
            )

        if user.password:
            if verify_password(user.password, login_user.password):
                logger.info(f"Setting user_id cookie of user '{login_user.id}'")
                response.set_cookie(key="user_id", value=login_user.id)

                return BaseResponse(
                    message="Your logged in with valid credentials. Welcome.",
                )

    except VerifyMismatchError as e:
        logger.error(
            f"The password '{user.username}' tries to log in with is incorrect. Error {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The password you try to log in with is incorrect."
        )
