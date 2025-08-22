FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# копируем манифесты, чтобы кэшировались зависимости
COPY pyproject.toml uv.lock ./

# ставим только прод-зависимости, строго по lock-файлу
RUN uv sync --frozen --no-dev

# теперь исходники
COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
