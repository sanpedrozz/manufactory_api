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

WORKDIR /app

# Копирование файлов для установки зависимостей
COPY ../../pyproject.toml ../../poetry.lock ./
RUN poetry install --no-interaction --no-ansi --only mqtt_stat_service

# Копирование остального кода
COPY . /app/

# Запуск скрипта
CMD ["python", "src/services/mqtt_statistic/statistic.py"]
