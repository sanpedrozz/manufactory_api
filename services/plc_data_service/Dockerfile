# Этап сборки зависимостей
FROM python:3.13.0-slim-bookworm AS builder

# Настройки окружения
ENV TZ=Europe/Moscow \
    POETRY_VERSION=1.8.2 \
    PYTHONUNBUFFERED=on \
    PYTHONPATH=/app

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY poetry.lock pyproject.toml /app/

# Установка зависимостей через Poetry
RUN poetry install --no-interaction --no-ansi

# Копирование кода проекта
COPY src /app/src

# Команда для запуска сервиса
CMD ["python", "/app/src/plc_data_history/main.py"]
