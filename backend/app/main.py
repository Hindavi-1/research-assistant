"""FastAPI application entrypoint."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.config import get_settings
from app.core.exceptions import ResearchAssistantError
from app.core.logging import logger, setup_logging

settings = get_settings()
setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Agentic research assistant — automates literature discovery, gap analysis, "
        "and evidence-backed research idea/title generation."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ResearchAssistantError)
async def research_assistant_exception_handler(request: Request, exc: ResearchAssistantError):
    logger.error(f"{request.method} {request.url.path} -> {exc.message}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}
