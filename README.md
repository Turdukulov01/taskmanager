# Task Manager (FastAPI + uv)

Коротко: CRUD-сервис управления задачами. Статусы: `created`, `in_progress`, `completed`.  
Документация: **Swagger** по адресу `http://localhost:8000/docs`.

---

## 1) Описание
- **FastAPI** + **SQLAlchemy 2.0** + **Pydantic v2**
- БД по умолчанию: **SQLite** (`tasks.db` создаётся автоматически)
- Менеджер пакетов/запуска: **uv**
- Тесты: **pytest**
- Контейнеризация: **Docker**

---

## 2) Требования
- Python ≥ 3.12  
- Установленный **uv** (https://docs.astral.sh/uv/)  
- (опционально) Docker ≥ 24

---

## 3) Установка и запуск (Linux/macOS)
bash
#1) Установить зависимости (включая dev)
uv sync --all-extras --group dev

---

# 2) Запустить API (порт 8000)
-uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
-Открой в браузере: http://localhost:8000/docs (Swagger) или http://localhost:8000/redoc

---

## 4) Установка и запуск (Windows, PowerShell)

# 1) Установить зависимости (включая dev)
uv sync --all-extras --group dev
# 2) Запустить API (порт 8000)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- Открой: http://localhost:8000/docs

---

## 5) Быстрая проверка функционала

Через Swagger
    - 1) Перейди в /docs.
    - 2) POST /tasks → тело:
        { "title": "Write tests", "description": "cover all cases" }
    - 3) Cкопируй id → GET /tasks/{id}.
    - 4) PATCH /tasks/{id} → обнови статус на in_progress/completed.
    - 5) DELETE /tasks/{id} → удаление.

Через curl
-    # создать
        curl -s http://localhost:8000/tasks -H "Content-Type: application/json" \
         -d '{"title":"Task A","description":"desc"}'
    
-    # список (фильтр + пагинация)
        curl -s "http://localhost:8000/tasks?status=created&limit=10&offset=0"
    
-    # обновить (подставь id)
        curl -s -X PATCH http://localhost:8000/tasks/<id> -H "Content-Type: application/json" \
         -d '{"status":"completed"}'
    
-    # удалить
        curl -i -X DELETE http://localhost:8000/tasks/<id>  

---

## 6) Тесты
- uv run pytest -q --cov=app --cov-report=term-missing

---

## 7) Конфигурация (ENV)

# Linux/macOS
export APP_DATABASE_URL="sqlite:///./dev.db"
uv run uvicorn app.main:app --reload

# Windows PowerShell
$env:APP_DATABASE_URL="sqlite:///./dev.db"
uv run uvicorn app.main:app --reload
                PostgreSQL: добавь драйвер psycopg[binary] и используй строку вида
                postgresql+psycopg://user:pass@host:5432/dbname.

---

## 8) Docker
# собрать образ
docker build -t task-manager .

# запустить контейнер (порт 8000 на хосте)
docker run --name taskmgr -p 8000:8000 task-manager
    Открой: http://localhost:8000/docs
        Рекомендовано хранить uv.lock в репозитории. Если lock отсутствует, в Dockerfile используйте RUN uv sync --no-dev

---

## 9) Структура проекта

    app/
 ├─ api.py        # HTTP-эндпоинты
 ├─ crud.py       # бизнес-логика поверх ORM
 ├─ db.py         # engine, session, Base
 ├─ main.py       # FastAPI app и инициализация схемы
 ├─ models.py     # SQLAlchemy-модели (Task, TaskStatus)
 ├─ schemas.py    # Pydantic-схемы (TaskCreate/Update/Out)
 └─ core/config.py# настройки (ENV)
tests/
 ├─ conftest.py
 └─ test_tasks.py
    test_get_db.py
pyproject.toml
Dockerfile
README.md

---

## 10) Полезные команды
# только prod-зависимости
uv sync

# запуск без перезагрузки
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
    Готово. API слушает порт 8000. Документация: http://localhost:8000/docs.










