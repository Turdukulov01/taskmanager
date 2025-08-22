from typing import Iterable, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task, TaskStatus


def create_task(db: Session, *, title: str, description: str | None) -> Task:
    obj = Task(title=title, description=description, status=TaskStatus.created)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_task(db: Session, task_id: str) -> Task | None:
    return db.get(Task, task_id)


def list_tasks(
    db: Session,
    *,
    status: TaskStatus | None = None,
    limit: int = 50,
    offset: int = 0,
) -> Sequence[Task]:
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    stmt = stmt.order_by(Task.created_at.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


def update_task(
    db: Session,
    task: Task,
    *,
    title: str | None = None,
    description: str | None = None,
    status: TaskStatus | None = None,
) -> Task:
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
