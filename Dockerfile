# Основной этап
FROM python:3.12.7-slim-bookworm AS base

ENV TZ=Europe/Moscow
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

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

# Проверка, где установлен Poetry
RUN echo $PATH && ls /root/.local/bin

ENV PATH=/root/.local/bin:$PATH

EXPOSE 7000

# Запуск приложения
CMD ["/root/.local/bin/poetry", "run", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
