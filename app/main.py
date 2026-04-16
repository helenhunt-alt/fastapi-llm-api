from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "environment": settings.env,
        }

    return app


app = create_app()
