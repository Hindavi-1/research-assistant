"""Aggregates all v1 routers under a single APIRouter, mounted in app.main."""
from fastapi import APIRouter

from app.api.v1 import research, sessions

api_router = APIRouter()
api_router.include_router(sessions.router)
api_router.include_router(research.router)
