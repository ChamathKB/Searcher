# Dockerfile is based on the following tutorial:
# https://www.erraticbits.ca/post/2021/fastapi/

# Build step #1: build the React front end
FROM node:20-bookworm-slim as build-step

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY frontend/package.json  ./

RUN npm install

COPY ./frontend/ ./

RUN npm run build


FROM python:3.11-slim-bookworm

RUN apt-get update -y && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry for packages management
RUN python -m pip install -U pip poetry
RUN poetry config virtualenvs.create false

# Use /app as the working directory
WORKDIR /app

# Copy poetry files & install the dependencies
COPY ./backend/pyproject.toml /app
COPY ./backend/poetry.lock /app
COPY --from=build-step /app/dist /app/static

RUN poetry lock --no-update
RUN poetry install --no-interaction --no-ansi --no-root --without dev
RUN python -c 'from fastembed.embedding import DefaultEmbedding; DefaultEmbedding("sentence-transformers/all-MiniLM-L6-v2")'

# Finally copy the application source code and install root
COPY ./backend/searcher /app/searcher

EXPOSE 8000

CMD uvicorn searcher.service:app --host 0.0.0.0 --port 8000 --workers ${WORKERS:-1}
