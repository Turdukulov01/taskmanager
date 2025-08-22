from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import TaskStatus
from app import crud
from app.schemas import TaskCreate, TaskUpdate, TaskOut


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    obj = crud.create_task(db, title=payload.title, description=payload.description)
    return obj


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: str, db: Session = Depends(get_db)):
    obj = crud.get_task(db, task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj


@router.get("", response_model=list[TaskOut])
def list_tasks(
    status: TaskStatus | None = Query(default=None, description="created | in_progress | completed"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return crud.list_tasks(db, status=status, limit=limit, offset=offset)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    obj = crud.get_task(db, task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")

    new_status = TaskStatus(payload.status) if payload.status is not None else None
    updated = crud.update_task(
        db,
        obj,
        title=payload.title,
        description=payload.description,
        status=new_status,
    )
    return updated


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    obj = crud.get_task(db, task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, obj)
    return None
