import os

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv

load_dotenv(override=True)

ph = PasswordHasher()

PEPPER = os.getenv("SECRET_KEY")


def hash_password(password: str) -> str:
    """Hashes the password with a pepper using Argon2."""
    peppered_password = password + PEPPER

    hashed_password = ph.hash(peppered_password)

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies the password by adding the pepper and checking the hash."""
    peppered_password = password + PEPPER

    try:
        return ph.verify(hashed_password, peppered_password)
    except VerifyMismatchError:
        raise VerifyMismatchError("Password verification failed.")
