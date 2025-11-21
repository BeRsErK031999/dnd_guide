docker compose down
docker volume rm postgres_data
docker compose up -d
docker compose exec backend .venv/bin/alembic upgrade head
docker compose down
