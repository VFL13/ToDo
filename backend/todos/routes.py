from bson.objectid import ObjectId
from config.config import DB, CONF
from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from .models import ToDo, ToDoOnDB, ToDoState


todo_router = APIRouter()


def validate_object_id(id_: str):
    try:
        _id = ObjectId(id_)
    except Exception:
        if CONF["fastapi"].get("debug", False):
            logging.warning("Invalid Object ID")
        raise HTTPException(status_code=400)
    return _id


async def _get_todo_or_404(id_: str):
    _id = validate_object_id(id_)
    todo = await DB.todo.find_one({"_id": _id})
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="todo not found")


def fix_todo_id(todo):
    todo["id_"] = str(todo["_id"])
    return todo


@todo_router.get("/", response_model=List[ToDoOnDB])
async def get_all_todo(status: ToDoState = None, limit: int = 10, skip: int = 0):
    """[summary]
    Gets all todos.
    [description]
    Endpoint to retrieve todos.
    """
    if status is None:
        todo_cursor = DB.todo.find().skip(skip).limit(limit)
    else:
        todo_cursor = DB.todo.find({"status": status.value}).skip(skip).limit(limit)
    todos = await todo_cursor.to_list(length=limit)
    return list(map(fix_todo_id, todos))


@todo_router.post("/", response_model=ToDoOnDB)
async def add_todo(todo: ToDo):
    """[summary]
    Inserts a new todo on the DB.
    [description]
    Endpoint to add a new todo.
    """

    todo_op = await DB.todo.insert_one(todo.dict())
    if todo_op.inserted_id:
        todo = await _get_todo_or_404(todo_op.inserted_id)
        todo["id_"] = str(todo["_id"])
        return todo


@todo_router.get(
    "/{id_}",
    response_model=ToDoOnDB
)
async def get_todo_by_id(id_: ObjectId = Depends(validate_object_id)):
    """[summary]
    Get one todo by ID.
    [description]
    Endpoint to retrieve an specific todo.
    """
    todo = await DB.todo.find_one({"_id": id_})
    if todo:
        todo["id_"] = str(todo["_id"])
        return todo
    else:
        raise HTTPException(status_code=404, detail="todo not found")


@todo_router.delete(
    "/{id_}",
    dependencies=[Depends(_get_todo_or_404)],
    response_model=dict
)
async def delete_todo_by_id(id_: str):
    """[summary]
    Get one todo by ID.
    [description]
    Endpoint to retrieve an specific todo.
    """
    todo_op = await DB.todo.delete_one({"_id": ObjectId(id_)})
    if todo_op.deleted_count:
        return {"status": f"deleted count: {todo_op.deleted_count}"}


@todo_router.put(
    "/{id_}",
    dependencies=[Depends(validate_object_id), Depends(_get_todo_or_404)],
    response_model=ToDoOnDB
)
async def update_todo(id_: str, todo_data: ToDo):
    """[summary]
    Update a todo by ID.
    [description]
    Endpoint to update an specific todo with some or all fields.
    """
    todo_op = await DB.todo.update_one(
        {"_id": ObjectId(id_)}, {"$set": todo_data.dict()}
    )
    if todo_op.modified_count:
        todo = await _get_todo_or_404(id_)
        todo['id_'] = id_
        del todo['_id']
        return todo
    else:
        raise HTTPException(status_code=304)
