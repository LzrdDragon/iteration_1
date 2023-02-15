# syntax = docker/dockerfile:1
# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.10-slim-bullseye

# `MY_ENV` arg is used to make prod / dev builds:
ARG MY_ENV \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000

ENV MY_ENV=${MY_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.3.2 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code

RUN groupadd -g "${GID}" -r web \
  && useradd -d '/code' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/code'

COPY --chown=web:web ./poetry.lock ./pyproject.toml /code/

# Creating folders, and files for a project:
COPY . /code

# Project initialization:
# hadolint ignore=SC2046
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$MY_ENV" \
  && poetry --version \
  # Install deps:
  && poetry run pip install -U pip \
  && poetry install \
    $(if [ "$MY_ENV" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi

EXPOSE 8000

# Running as non-root user:
USER web
