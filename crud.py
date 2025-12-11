from sqlmodel import select, or_
from models import Task
from database import get_session

def get_tasks(search="", status="", priority="", tag="", sort="due"):
    with next(get_session()) as session:
        query = select(Task)

        if search:
            query = query.where(Task.title.ilike(f"%{search}%"))
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "active":
            query = query.where(Task.completed == False)
        if priority:
            query = query.where(Task.priority == priority.capitalize())
        if tag:
            query = query.where(Task.tags.contains(tag))

        if sort == "due":
            query = query.order_by(Task.due.asc(), Task.priority.desc())
        elif sort == "priority":
            query = query.order_by(
                Task.priority == "High",
                Task.priority == "Medium",
                Task.priority == "Low"
            )
        else:
            query = query.order_by(Task.title)

        return session.exec(query).all()

def create_task(task_data: dict):
    with next(get_session()) as session:
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def update_task(task_id: int, updates: dict):
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        if not task:
            return None
        for key, value in updates.items():
            setattr(task, key, value)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def delete_task(task_id: int):
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        if task:
            session.delete(task)
            session.commit()
            return True
        return False