from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def problem_response(status: int, title: str, detail: str | None = None, type_: str | None = None):
  body = {
    "type": type_ or "about:blank",
    "title": title,
    "status": status,
  }
  if detail:
    body["detail"] = detail
  return JSONResponse(status_code=status, content=body)


def install_problem_handlers(app: FastAPI) -> None:
  @app.exception_handler(StarletteHTTPException)
  async def http_exc_handler(request: Request, exc: StarletteHTTPException):
    return problem_response(exc.status_code, exc.detail or "HTTP Error")

  @app.exception_handler(RequestValidationError)
  async def validation_exc_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
      status_code=422,
      content={
        "type": "https://example.com/validation-error",
        "title": "Validation Error",
        "status": 422,
        "errors": exc.errors(),
      },
    )
