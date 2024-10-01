from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher

from server.api import get_db
from server.logger.logger import logger
from server.database.models.player_characters import PlayerCharacter
from server.database.models.users import User
from server.database.models.roles import Role
from server.database.models.parties import Party
from server.api.models.delete_response import DeleteResponse
from server.api.models.user import UserModel, UserPostBase, UserPutBase, UserResponse
from server.api.utils.user_utilities import hash_password

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    responses={404: {"description": "Not found."}},
)


@router.get("/", response_model=list[UserModel])
def get_users(db: Session = Depends(get_db)) -> list[UserModel]:
    """
    Queries the users database table for all rows.

    - **Returns** list[UserModel]: All user instances in the database.

    **Response Example**:
    ```json
    [
        {
            "id": 1,
            "name": "Name 1",
            "username": "Username 1",
            "image": bytes | None,
            "parties": list[Parties] | None,
            "characters": list[PlayerCharacter] | None,
        },
        {
            "id": 2,
            "name": "Name 2",
            "username": "Username 2",
            "image": bytes | None,
            "parties": list[Parties] | None,
            "characters": list[PlayerCharacter] | None,
        },
    ]
    """
    logger.info("Querying users table for all results.")
    stmt = select(User)
    users = db.execute(stmt).scalars().all()

    logger.info(f"Returned {len(users)} from the users table.")
    return users


@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserModel:
    """
    Queries the users table in the database table for a specific row with the id of user_id.

    - **Returns** UserModel: The user instance queried for, otherwise 404 HTTPException.

    - **HTTPException**: If the queried user does not exist.

    **Response Example**:
    ```json
    {
        "id": 1,
        "name": "User 1",
        "username": "Username 1",
        "image": bytes | None,
        "parties": list[Parties] | None,
        "characters": list[PlayerCharacter] | None,
    }
    ```
    """
    logger.info(f"Querying users table for row with id '{user_id}'.")
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalars().first()

    if not user:
        logger.error(f"No user with the id of '{user_id}'.")
        raise HTTPException(status_code=404, detail="User not found.")

    logger.info(f"Returning user info with id of {user_id}.")
    return user


@router.post("/", response_model=UserResponse)
def post_user(user: UserPostBase, db: Session = Depends(get_db)) -> UserResponse:
    """
    Creates a new row in the users table.

    - **Returns** UserResponse: A dictionary holding a message and the new user.

    - **HTTPException**: If a user with this username already exists.

    **Request Body Example**:
    ```json
    {
        "name": "example_name",
        "username": "example_username",
        "image": image_uploaded,
        "password": "example_password",
        "parties": [example_party_id],
        "roles": [example_role_id],
    }
    ```
    - `name`: A string between 1 and 50 characters long (inclusive).
    - `username`: A string between 1 and 50 characters long (inclusive).
    - `image`: An image provided by the user (optional). NOT IMPLEMENTED YET!
    - `password`: A string between 1 and 50 characters long (optional).
    - `parties`: A list holding all party id's the user is part of (optional).
    - `roles`: A list holding all roll id's of the user (optional).

    **Response Example**:
    ```json
    {
        "message": "New user 'example_user' has been added to the database.",
        "user": {
            "id": 1,
            "name": "User 1",
            "username": "Username 1",
            "image": bytes | None,
            "parties": list[Parties] | None,
            "characters": [Empty list],
        }
    }
    ```
    """
    try:
        logger.info(f"Creating new user with name '{user.username}'.")
        attributes: dict[str, Any] = {}
        attributes["id"] = str(uuid.uuid4())
        attributes["name"] = user.name
        attributes["username"] = user.username
        attributes["image"] = user.image if user.image else None

        if user.password:
            attributes["password"] = hash_password(user.password)
        if user.parties:
            logger.debug(f"Adding parties with ids '{user.parties}' to new user.")

            stmt = select(Party).where(Party.id.in_(user.parties))
            parties = db.execute(stmt).scalars().all()

            missing_parties = set(user.parties) - {party.id for party in parties}
            if missing_parties:
                logger.error(f"No party found for the following ids: {missing_parties}")
                raise HTTPException(
                    status_code=404, detail="One or more parties not found."
                )
            logger.debug(f"Found parties: '{parties}'")

            attributes["parties"] = parties
        if user.roles:
            logger.debug(f"Adding roles with ids '{user.roles}' to new user.")

            stmt = select(Role).where(Role.id.in_(user.roles))
            roles = db.execute(stmt).scalars().all()

            missing_roles = set(user.roles) - {role.id for role in roles}
            if missing_roles:
                logger.error(f"No role found for the following ids: {missing_roles}")
                raise HTTPException(
                    status_code=404, detail="One or more roles not found."
                )
            logger.debug(f"Found roles: '{roles}'")

            attributes["roles"] = roles

        new_user = User(**attributes)
        db.add(new_user)

        db.commit()
        db.refresh(new_user)
        logger.debug(
            f"Committed new user with username '{new_user.username}' to the database."
        )

        return UserResponse(
            message=f"New user '{new_user.name}' has been added to the database.",
            user=new_user,
        )

    except IntegrityError as e:
        logger.error(
            f"User with the username '{user.username}' already exists. Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail="Username already exists.")


@router.put("/{user_id}", response_model=UserResponse)
def put_user(
    user_id: str, user: UserPutBase, db: Session = Depends(get_db)
) -> UserResponse:
    """
    Updates an user in the database by its unique id.

    - **Returns** UserResponse: A message and the updated user.

    - **HTTPException**: When the user id does not exist.
    - **HTTPException**: When the username of the user already exists in the database.
    - **HTTPException**: When a party, character or role does not exists.

    **Request Body Example**:
    ```json
    {
        "name": "updated_name",
        "username": "updated_username",
        "image": bytes,
        "password": "updated_password",
        "roles": [
            {
                "role_id": id_int,
                "add_role": boolean,
            },
        ],
        "parties": [
            {
                "party_id": id_int,
                "add_party": boolean,
            },
        ],
        "characters": [
            {
                "character_id": id_int,
                "add_character": boolean,
            },
        ],
    }
    ```
    - `username`: A string between 1 and 50 characters long (optional).
    - `name`: A string between 1 and 50 characters long (optional).
    - `image`: A bytes object containing the image of the user (optional).
    - `password`: A new password (optional).
    - `roles`: List containing roles to be added or deleted (optional).
    - `parties`: List containing parties to be added or deleted (optional).
    - `characters`: List containing characters to be added or deleted (optional).

    **Response Example**:
    ```json
    {
        "message": "User 'updated_user' has been updated.",
        "user": {
            "id": 1,
            "name": "User 1",
            "username": "Username 1",
            "image": bytes | None,
            "parties": list[Parties] | None,
            "characters": list[PlayerCharacter] | None
        }
    }
    ```
    """
    try:
        updated_user = db.get(User, user_id)
        if not updated_user:
            logger.error(f"No user found with id '{user_id}'.")
            raise HTTPException(
                status_code=404,
                detail="The user you are trying to update does not exist.",
            )

        if user.name:
            logger.debug(f"Updating name of user with id '{user_id}'.")
            updated_user.name = user.name
        if user.username:
            logger.debug(f"Updating username of user with id '{user_id}'.")
            updated_user.username = user.username
        if user.password:
            logger.debug(f"Updating password of user with id '{user_id}'.")
            hasher = PasswordHasher()
            hash = hasher.hash(user.password)
            updated_user.password = hash
        if user.roles:
            logger.debug(f"Updating roles of user with id: '{user_id}'.")

            for update_role in user.roles:
                stmt = select(Role).where(Role.id == update_role.role_id)
                found_role = db.execute(stmt).scalars().first()

                if not found_role:
                    logger.error(f"No role found with id '{update_role}'.")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Role with id '{update_role.role_id}' not found.",
                    )

                elif update_role.add_role:
                    logger.debug(f"Adding role with name '{found_role.name}' to user.")
                    if found_role not in updated_user.roles:
                        updated_user.roles.append(found_role)
                else:
                    logger.debug(
                        f"Removing role with name '{found_role.name}' to user."
                    )
                    if found_role in updated_user.roles:
                        updated_user.roles.remove(found_role)
        if user.parties:
            logger.debug(f"Updating parties for user with id: '{user_id}'.")

            for update_party in user.parties:
                stmt = select(Party).where(Party.id == update_party.party_id)
                found_party = db.execute(stmt).scalars().first()

                if not found_party:
                    logger.error(f"No role party with id '{update_party}'.")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Party with id '{update_party.party_id}' not found.",
                    )

                elif update_party.add_party:
                    logger.debug(
                        f"Adding party with name '{found_party.name}' to user."
                    )
                    if found_party not in updated_user.parties:
                        updated_user.parties.append(found_party)
                else:
                    logger.debug(
                        f"Removing party with name '{found_party.name}' to user."
                    )
                    if found_party in updated_user.parties:
                        updated_user.parties.remove(found_party)
        if user.characters:
            logger.debug(f"Updating characters for user with id: '{user_id}'.")

            for update_character in user.characters:
                stmt = select(PlayerCharacter).where(
                    PlayerCharacter.id == update_character.character_id
                )
                found_character = db.execute(stmt).scalars().first()

                if not found_character:
                    logger.error(f"No character found with id '{update_character}'.")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Character with id '{update_character.character_id}' not found.",
                    )

                elif update_character.add_character:
                    logger.debug(
                        f"Adding character with name '{found_character.name}' to user."
                    )
                    if found_character not in updated_user.characters:
                        updated_user.characters.append(found_character)
                else:
                    logger.debug(
                        f"Removing character with name '{found_character.name}' to user."
                    )
                    if found_character in updated_user.characters:
                        updated_user.characters.remove(found_character)

        db.commit()
        logger.info(f"Committed changes to the database for user with id: '{user_id}'")

        return UserResponse(
            message=f"User '{updated_user.name}' has been updated.",
            user=updated_user,
        )

    except IntegrityError as e:
        logger.error(f"The username '{user.username}' already exists. Error: {str(e)}")
        raise HTTPException(
            status_code=400, detail="The username you are trying to use already exists."
        )


@router.delete("/{user_id}", response_model=DeleteResponse)
def delete_user(user_id: str, db: Session = Depends(get_db)) -> DeleteResponse:
    """
    Deletes a user from the database.

    - **Returns** DeleteResponse: A dictionary holding the confirmation message.

    - **HTTPException**: Raised when the id does not exist in the database.

    **Response Example**:
    ```json
    {
        "message": "User has been deleted.",
    }
    ```
    """
    user = db.get(User, user_id)
    logger.info(f"Deleting user with the id '{user_id}'.")

    if not user:
        logger.error(f"User with id '{user_id}' not found.")
        raise HTTPException(
            status_code=404,
            detail="The user you are trying to delete does not exist.",
        )

    db.delete(user)
    db.commit()

    logger.info(f"User with id '{user_id}' deleted.")
    return DeleteResponse(message="User has been deleted.")
