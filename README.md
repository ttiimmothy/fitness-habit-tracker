# Fitness & Habit Tracker

Monorepo with FastAPI backend and Astro client.

## Quickstart

1. Copy envs
   - backend: create `.env` from `.env.example`
   - client: create `.env` with `PUBLIC_VITE_API_URL=http://localhost:8000`
2. Start dev stack
```bash
docker compose up --build
poetry run alembic revision --autogenerate -m "init schema"
poetry run alembic upgrade head
```
3. Seed demo data
```bash
docker compose exec backend poetry run python seed.py
```
4. Open client at http://localhost:4321

## API

- POST /auth/login { email, password } → { accessToken, user }
- GET /auth/me → { user }
- GET /habits, POST /habits, PUT /habits, DELETE /habits
- POST /habits/logs/:id/log, GET /habits/logs/today
- GET /stats/{habit_id}/stats/streak, /stats/{habit_id}/daily-progress