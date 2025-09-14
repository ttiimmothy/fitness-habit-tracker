FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY . .
RUN uv pip install --system -e .
ENTRYPOINT ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:${PORT} app.main:app"]