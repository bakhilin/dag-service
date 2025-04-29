# Stage 1
FROM python:3.11-slim@sha256:82c07f2f6e35255b92eb16f38dbd22679d5e8fb523064138d7c6468e7bf0c15b AS builder

WORKDIR /dag-service/
COPY pyproject.toml poetry.lock* /dag-service/
ARG POETRY_VERSION=1.5.0

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /dag-service/
ENV DATABASE_URL=sqlite+aiosqlite:///:memory:
RUN poetry run pytest --cov=src --cov-report=term-missing


FROM python:3.11-slim@sha256:82c07f2f6e35255b92eb16f38dbd22679d5e8fb523064138d7c6468e7bf0c15b AS production

WORKDIR /dag-service/
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /dag-service /dag-service

RUN rm -rf tests/ 

# RUN poetry install --no-dev --no-root

ENV DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER:-daguser}:${POSTGRES_PASSWORD:-dagpassword}@db:5432/${POSTGRES_DB:-dagdb}


CMD ["poetry", "run", \
    "uvicorn", "main:app", \
    "--host", "0.0.0.0", "--port", "8080"]