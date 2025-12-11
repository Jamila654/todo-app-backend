from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
    priority: str = "Medium"  # High / Medium / Low
    due: Optional[date] = None
    tags: str = ""  # comma separated, e.g. "work,urgent"