import uuid
from datetime import datetime
from enum import StrEnum
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Text, DateTime
from sqlalchemy import Enum as SAEnum

from app.db import Base


class TaskStatus(StrEnum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status"), nullable=False, default=TaskStatus.created)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
