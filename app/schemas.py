from typing import Literal
from pydantic import BaseModel, Field, ConfigDict  # <-- добавили ConfigDict

StatusLiteral = Literal["created", "in_progress", "completed"]

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: StatusLiteral | None = None

class TaskOut(BaseModel):
    id: str
    title: str
    description: str | None
    status: StatusLiteral

    # было:
    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)  # <-- так корректно для v2
