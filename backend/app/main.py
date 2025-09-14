from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from app.core.config import settings
from app.core.rate_limit import init_rate_limiter
from app.problem_details import install_problem_handlers
from app.routers import auth
from app.routers import habits
from app.routers import logs
from app.routers import stats


@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup logic
  if settings.rate_limit_enabled:  # toggle via env
    try:
      await init_rate_limiter()
    except Exception as e:
      # Log but don't crash in dev
      print(f"⚠️ Rate limiter init failed: {e}")

  yield

  # Shutdown logic
  if FastAPILimiter.redis:
    await FastAPILimiter.redis.aclose()


def create_app() -> FastAPI:
  app = FastAPI(title="Fitness & Habit Tracker",
                version="0.1.0", lifespan=lifespan)

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:4321", "https://fitness-habit-tracker.vercel.app"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
      expose_headers=[],
  )

  install_problem_handlers(app)

  api_router = APIRouter(prefix="/api")

  api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
  api_router.include_router(habits.router, prefix="/habits", tags=["habits"])
  api_router.include_router(logs.router, prefix="/logs/habits", tags=["logs"])
  api_router.include_router(stats.router, prefix="/stats", tags=["stats"])

  app.include_router(api_router)

  # @app.middleware("http")
  # async def _log_origin(request, call_next):
  #   if "origin" in request.headers:
  #     print("Origin seen by server ->", request.headers["origin"])
  #   return await call_next(request)

  @app.get("/health")
  async def health():
    return {"status": "ok"}

  return app


app = create_app()
