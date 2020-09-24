from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class ToDoState(str, Enum):
    """
    [summary]
        Used to manage supported sms states.
    [description]
        Simple enumeration to link the sms state.
    """
    todo = "To Do"
    in_progress = "In Progress"
    Done = "Done"


class ToDo(BaseModel):
    """
    Simple To Do with title and  description
    """
    creator: str
    title: str
    description: str
    create_date: datetime = None
    status: ToDoState = "To Do"


class ToDoOnDB(ToDo):
    id_: str
