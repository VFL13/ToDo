from fastapi import FastAPI

from core.routes import core_router
from todos.routes import todo_router
from config import config

api_path = f"/api/{config.API_VERSION}"

app = FastAPI(
    title="VFL13 ToDoS",
    description="""
    ToDo list.
    """,
    version="0.1",
    openapi_url=f"{api_path}/openapi.json",
    docs_url=f"{api_path}/docs",
    redoc_url=None
)

app.include_router(
    todo_router,
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    core_router,
    tags=["core"],
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
