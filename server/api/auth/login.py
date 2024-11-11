from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
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
    login_model: LoginModel, response: Response, db: Session = Depends(get_db)
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
        logger.info(f"User trying to log in with username: '{login_model.username}'.")
        stmt = select(User).where(User.username == login_model.username)
        user = db.execute(stmt).scalar_one_or_none()

        if not user:
            logger.error(
                f"No user found with the following username: {login_model.username}."
            )
            raise HTTPException(
                status_code=404,
                detail="The username you try to log in with does not exist.",
            )

        if login_model.password:
            verify_password(login_model.password, user.password)

        logger.info(f"Setting jwt token cookie of user '{user.id}'")

        # response.set_cookie(key="user_token", value=jwt_token)

        logger.info(f"Setting user_id cookie of user '{user.id}'")
        response.set_cookie(key="user_id", value=user.id)

        return BaseResponse(
            message="Your logged in with valid credentials. Welcome.",
        )

    except VerifyMismatchError as e:
        logger.error(
            f"The password '{login_model.username}' tries to log in with is incorrect. Error {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="The password you try to log in with is incorrect."
        )
