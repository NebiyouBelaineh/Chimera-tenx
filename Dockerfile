FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --dev

RUN useradd -m appuser
USER appuser

COPY . .

CMD ["uv", "run", "pytest", "tests/", "-v"]
