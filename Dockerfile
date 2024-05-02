FROM python:3.12

ENV TZ=Europe/Moscow
ENV POETRY_VERSION=1.7.0
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

WORKDIR /scr
COPY pyproject.toml poetry.lock /scr/

RUN pip install poetry
RUN poetry install --no-root

COPY . /scr/

EXPOSE 7000

CMD ["poetry", "run", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
