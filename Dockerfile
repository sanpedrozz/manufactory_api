# Этап сборки зависимостей
FROM python:3.12.7-slim-bookworm AS builder

ENV TZ=Europe/Moscow
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

# Установка зависимостей для сборки
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    curl \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install "poetry==1.7.0" && poetry config virtualenvs.create false

WORKDIR /scr
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry install --no-interaction --no-ansi -vvv

# Основной этап
FROM python:3.12.7-slim-bookworm AS base

ENV TZ=Europe/Moscow
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

# Установка необходимых инструментов для выполнения
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    curl \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /scr

# Копирование приложения и установленных зависимостей из предыдущего этапа
COPY --from=builder /root/.local /root/.local
COPY . /scr/

ENV PATH="/root/.local/bin:$PATH"

EXPOSE 7000

# Запуск приложения
CMD ["poetry", "run", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
