import os
from datetime import timedelta, timezone, datetime
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.api import get_db
from server.api.models.token_data import TokenData
from server.api.models.user import UserInDB
from server.api.auth.security import oauth2_scheme
from server.models.users import User

load_dotenv(override=True)

ph = PasswordHasher()

PEPPER = os.getenv("SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password: str) -> str:
    """Hashes the password with a pepper string using Argon2."""
    peppered_password = password + PEPPER

    hashed_password = ph.hash(peppered_password)

    return hashed_password

def verify_password(plain_password, hashed_password) -> bool:
    """Checks if peppered plain password is the same as hashed password in database using Argon2."""
    peppered_password = plain_password + PEPPER

    return ph.verify(hashed_password, peppered_password)


def get_user(db, username: str) -> UserInDB:
    """
    Gets user from database using username

    Returns a UserInDB object if user exists.
    """
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalar_one_or_none()

    if user:
        return UserInDB(id=user.id, name=user.name, username=user.username, hashed_password=user.password)


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | bool:
    """
    Authenticates if user exists by first checking by username and then checks if password is correct.

    Returns False if no user or false password, else returns the user
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    creates a JWT access token for accessing the API after user has logged in successfully.

    Returns the encoded JWT as a string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> UserInDB:
    """
    Uses the JWT to check if the user that is trying to connect to the API is a valid user.

    Raises HTTPException if JWT is invalid or if the user credentials are incorrect.

    Returns UserInDB if all checks are met.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception
        token_data = TokenData(id=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.id)
    if not user:
        raise credentials_exception

    return user
