from fastapi import FastAPI

from app.db import Base, engine
from app.api import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager", version="0.1.0")
    app.include_router(tasks_router)
    return app


app = create_app()

# auto-create schema on startup (для тестового задания достаточно)
Base.metadata.create_all(bind=engine)
