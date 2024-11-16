import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from server.api import get_db
from server.api.auth.user_authentication import authenticate_user, create_access_token
from server.api.models.base_response import BaseResponse
from config.logger_config import logger
from server.models import User

router = APIRouter()

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found."}},
)


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Endpoint used for logging in to the application. When successful it set a cookie with the user id.

    - **Returns** BaseResponse: A dictionary holding a message.

    - **HTTPException**: If the username does not exist.
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
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    logger.info(f"Setting jwt token cookie of user '{user.id}'")
    response.set_cookie(key="user_token", value=access_token)

    return BaseResponse(
        message="Your logged in with valid credentials. Welcome.",
    )


@router.delete("/{user_id}", response_model=BaseResponse)
def logout_user(
    user_id: int, response: Response, db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Endpoint used for logging out to the application. When successful removes the user id cookie.

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

    logger.info(f"Removing user_id cookie of user '{logout_user.id}'")
    response.delete_cookie(key="user_id")

    return BaseResponse(
        message="Your logged out of the application. Goodbye.",
    )