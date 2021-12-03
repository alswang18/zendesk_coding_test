# pull official base image
FROM python:3.9.5-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.11

RUN pip install poetry==$POETRY_VERSION

# add and install requirements
COPY ./poetry.lock .
COPY ./pyproject.toml .

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc make \
  && apt-get clean

# set that venv won't be created in development
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .