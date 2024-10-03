# Этап сборки зависимостей
FROM python:3.12.7-slim-bookworm AS builder

ENV TZ=Europe/Moscow \
    POETRY_VERSION=1.7.0 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHONDONTWRITEBYTECODE=on \
    PYTHONFAULTHANDLER=on \
    PYTHONUNBUFFERED=on

# Установка зависимостей для сборки и Poetry в одном слое
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    curl \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    apt-get purge --auto-remove -y curl tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /scr

# Копирование файлов и установка зависимостей
COPY pyproject.toml poetry.lock /scr/
RUN poetry install --no-interaction --no-ansi -vvv

# Копирование оставшихся файлов
COPY . /scr/

EXPOSE 7000

# Запуск uvicorn напрямую без poetry run
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
