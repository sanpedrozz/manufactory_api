FROM ubuntu:latest

ENV TZ=Europe/Moscow
ENV POETRY_VERSION=1.7.0
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    ffmpeg \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    poetry --version

WORKDIR /scr
COPY pyproject.toml poetry.lock /scr/

RUN poetry install --no-root

COPY . /scr/

EXPOSE 7000

CMD ["poetry", "run", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
