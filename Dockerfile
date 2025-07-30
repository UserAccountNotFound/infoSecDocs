# Используем официальный образ Python
FROM python:3.11-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости для Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Playwright и его зависимости
RUN pip install playwright && \
    playwright install chrome && \
    playwright install-deps

# Настраиваем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f poetry.lock ]; then \
      pip install poetry && \
      poetry install --no-root --no-interaction --no-ansi; \
    else \
      pip install --no-cache-dir ".[all]"; \
    fi

# Копируем исходный код
WORKDIR /docs
COPY . .

# Устанавливаем переменную окружения для asyncio
ENV PYTHONASYNCIODEBUG=1

# Точка входа с явным указанием нового event loop
ENTRYPOINT ["python", "-c", "import asyncio; from mkdocs.__main__ import cli; asyncio.set_event_loop(asyncio.new_event_loop()); cli()"]
CMD ["build", "--site-dir", "/public"]