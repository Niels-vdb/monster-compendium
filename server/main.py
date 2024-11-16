from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

from server.api.middleware.logger import log_middleware

from server.api.routers import (
    attributes,
    classes,
    damage_types,
    enemies,
    non_player_characters,
    parties,
    player_characters,
    races,
    roles,
    sizes,
    subclasses,
    subraces,
    types,
    users, auth,
)
from server.api.auth import user_authentication

tags_metadata = [
    {
        "name": "Authentication",
        "description": "All log in and log out operation can be done here.",
    },
    {
        "name": "Attributes",
        "description": "All operations with attributes can be done here.",
    },
    {
        "name": "Classes",
        "description": "All operations with classes can be done here.",
    },
    {
        "name": "Damage Types",
        "description": "All operations with effects can be done here.",
    },
    {
        "name": "Enemies",
        "description": "All operations with enemies can be done here.",
    },
    {
        "name": "Non Player Characters",
        "description": "All operations with NPC characters can be done here.",
    },
    {
        "name": "Player Characters",
        "description": "All operations with PC characters can be done here.",
    },
    {
        "name": "Parties",
        "description": "All operations with parties can be done here.",
    },
    {
        "name": "Races",
        "description": "All operations with creature races can be done here.",
    },
    {
        "name": "Roles",
        "description": "All operations with user roles can be done here.",
    },
    {
        "name": "Sizes",
        "description": "All operations with creature sizes can be done here.",
    },
    {
        "name": "Types",
        "description": "All operations with creature types can be done here.",
    },
    {
        "name": "Users",
        "description": "All operations with users can be done here.",
    },
]

app = FastAPI(openapi_tags=tags_metadata, title="DnD Creature Compendium")
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(auth.router)

app.include_router(attributes.router)
app.include_router(classes.router)
app.include_router(damage_types.router)
app.include_router(enemies.router)
app.include_router(non_player_characters.router)
app.include_router(player_characters.router)
app.include_router(parties.router)
app.include_router(races.router)
app.include_router(roles.router)
app.include_router(sizes.router)
app.include_router(subclasses.router)
app.include_router(subraces.router)
app.include_router(types.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)