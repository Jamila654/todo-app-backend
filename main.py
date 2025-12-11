from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from .crud import get_tasks, create_task, update_task, delete_task
from .models import Task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/tasks")
def read_tasks(search: str = "", status: str = "", priority: str = "", tag: str = "", sort: str = "due"):
    return get_tasks(search, status, priority, tag, sort)

@app.post("/tasks")
def add_task(task: Task):
    return create_task(task.model_dump())

@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, updates: dict):
    task = update_task(task_id, updates)
    return task or {"error": "not found"}

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    return {"deleted": delete_task(task_id)}