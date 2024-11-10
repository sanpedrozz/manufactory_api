# Этап сборки зависимостей
FROM python:3.13.0-slim-bookworm


# Настройки окружения
ENV TZ=Europe/Moscow \
    POETRY_VERSION=1.8.4 \
    PYTHONUNBUFFERED=on

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY poetry.lock pyproject.toml /app/

# Установка зависимостей через Poetry
RUN poetry install --no-root --no-interaction --no-ansi -vvv && \
    poetry show  # Проверка установленных пакетов



# Копирование кода проекта
COPY services/hmi_statistic/src /app/services/hmi_statistic/src
COPY shared /app/shared
COPY ../../.env /app/.env

# Set the command to run the script
CMD ["poetry", "run", "python", "services/hmi_statistic/src/main.py"]
