# syntax=docker/dockerfile:1.0.0-experimental

FROM python:3.9

WORKDIR /app

# install poetry
RUN pip3 install poetry

COPY poetry.toml /app/
COPY pyproject.toml /app/

# install tests deps
RUN poetry install

COPY baseline_image /app/baseline_image

ENTRYPOINT ["poetry", "run", "baseline_test"]
