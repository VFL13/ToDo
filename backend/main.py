from fastapi import FastAPI
from todos.routes import todo_router
from config import config

app = FastAPI()


app.include_router(
    todo_router,
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)


@app.on_event("startup")
async def app_startup():
    """
    Do tasks related to app initialization. TODO SEND TO MESSAGE TO TELEGRAM
    """
    # This if fact does nothing its just an example.
    config.load_config()


@app.on_event("shutdown")
async def app_shutdown():
    """
    Do tasks related to app termination. TODO SEND TO MESSAGE TO TELEGRAM
    """
    # This does finish the DB driver connection.
    config.close_db_client()


@app.get("/status/")
async def get_all_actions():
    """[summary]
    Gets all gamer actions.
    [description]
    Endpoint for all actions.
    """
    return [{'status': 'send'}, ]
