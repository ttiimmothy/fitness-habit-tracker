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
- GET /habits, POST /habits
- POST /habits/:id/log, GET /habits/:id/logs
- GET /stats/overview