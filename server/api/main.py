from fastapi import FastAPI

from .routers import (
    classes,
    effects,
    monsters,
    non_player_characters,
    parties,
    player_characters,
    races,
    roles,
    sizes,
    subclasses,
    subraces,
    types,
    users,
)

tags_metadata = [
    {
        "name": "Classes",
        "description": "All operations with classes can be done here.",
    },
    {
        "name": "Effects",
        "description": "All operations with effects can be done here.",
    },
    {
        "name": "Monsters",
        "description": "All operations with monsters can be done here.",
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

app.include_router(classes.router)
app.include_router(effects.router)
app.include_router(monsters.router)
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
