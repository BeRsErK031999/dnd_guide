docker compose up -d
docker compose exec backend .venv/bin/alembic upgrade head
