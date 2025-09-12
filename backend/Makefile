run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port $${PORT:-8000}

lint:
	ruff check . && black --check .

fmt:
	ruff check --fix . && black .

test:
	pytest -q --cov

seed:
	poetry run python seed.py

db-upgrade:
	alembic upgrade head
