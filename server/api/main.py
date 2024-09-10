from fastapi import FastAPI

from .routers import (
    classes,
    effects,
    monsters,
    npc_characters,
    pc_characters,
    parties,
    races,
    roles,
    sizes,
    subclasses,
    subraces,
    types,
    users,
)

app = FastAPI()

app.include_router(classes.router)
app.include_router(effects.router)
app.include_router(monsters.router)
app.include_router(npc_characters.router)
app.include_router(pc_characters.router)
app.include_router(parties.router)
app.include_router(races.router)
app.include_router(roles.router)
app.include_router(sizes.router)
app.include_router(subclasses.router)
app.include_router(subraces.router)
app.include_router(types.router)
app.include_router(users.router)
