from fastapi import FastAPI

from .routers import (
    characteristics,
    classes,
    effects,
    monsters,
    npc_characters,
    pc_characters,
    parties,
    races,
    roles,
    users,
)

app = FastAPI()

app.include_router(characteristics.router)
app.include_router(classes.router)
app.include_router(effects.router)
app.include_router(monsters.router)
app.include_router(npc_characters.router)
app.include_router(pc_characters.router)
app.include_router(parties.router)
app.include_router(races.router)
app.include_router(roles.router)
app.include_router(users.router)


@app.get("/item/{item_id}")
async def root(item_id: int):
    """
    Gets an item

    :param item_id: The id for the given item
    :type item_id: int
    :return: dictionary containing a message and the item id
    :rtype: dict[str, Any]
    """
    return {"message": "Hello World", "item": item_id}
