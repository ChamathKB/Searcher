FROM python:3.11-slim-bookworm

RUN apt-get update -y && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install -U pip poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml /app
COPY ./poetry.lock /app

RUN poetry install --no-interaction --no-ansi --no-root --without dev
RUN python -c 'from fastembed.embedding import DefaultEmbedding; DefaultEmbedding("sentence-transformers/all-MiniLM-L6-v2")'

# Finally copy the application source code and install root
COPY searcher /app/searcher

EXPOSE 8000

CMD uvicorn searcher.service:app --host 0.0.0.0 --port 8000 --workers ${WORKERS:-1}
