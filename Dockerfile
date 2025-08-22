# лёгкий и быстрый образ с uv + Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# только манифесты для кеша
COPY pyproject.toml ./
# (если есть uv.lock — добавьте) COPY uv.lock ./

# ставим зависимости (без dev) в слой
RUN uv sync --frozen --no-dev

# копируем исходники
COPY app ./app

# создаём БД (если нет) при старте — делается в app/main.py через SQLAlchemy
EXPOSE 8000

# prod-команда
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
