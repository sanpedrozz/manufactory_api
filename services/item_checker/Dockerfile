# Этап сборки зависимостей
FROM python:3.13.0-slim-bookworm AS builder

# Настройки окружения
ENV TZ=Europe/Moscow \
    POETRY_VERSION=1.8.4 \
    PYTHONUNBUFFERED=on \
    PYTHONPATH=/app/src

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install jinja2
RUN pip install python-multipart

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY poetry.lock pyproject.toml /app/

# Установка зависимостей через Poetry
RUN poetry install --no-root --no-interaction --no-ansi -vvv

# Копирование кода проекта
COPY services/item_checker/src /app/services/item_checker/src
COPY shared /app/shared
COPY ../../.env /app/.env

# Запуск сервиса
CMD ["uvicorn", "services.item_checker.src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
