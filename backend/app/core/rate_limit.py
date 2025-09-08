from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

from app.core.config import settings


async def init_rate_limiter() -> None:
  redis = await aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
  await FastAPILimiter.init(redis)
