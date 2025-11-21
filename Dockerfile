FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

COPY pyproject.toml uv.lock .python-version ./

RUN uv venv

RUN uv sync --frozen --no-dev

COPY . .

CMD [ ".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ]
