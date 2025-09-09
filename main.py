import time
import traceback
from contextlib import asynccontextmanager
from typing import Any, Dict

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from api.answers import router as answers_router
from api.questions import router as questions_router
from config import settings
from database.connection import close_db, init_db


async def _run_migrations() -> None:
    """Run Alembic migrations."""
    try:
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")
        raise


async def _startup_db() -> None:
    try:
        await _run_migrations()
        await init_db()
        logger.info("Database connections initialized")
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        raise


async def _shutdown_db() -> None:
    """Close database connections."""
    await close_db()
    logger.info("Database connections closed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""

    logger.info("Starting application...")
    await _startup_db()

    yield

    logger.info("Shutting down application...")

    await _shutdown_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    app = FastAPI(
        lifespan=lifespan,
        title="Q/A app",
        description="Question and Answer application",
        version="1.0.0",
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        logger.error(f"Request: {request.method} {request.url}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )

    @app.middleware("http")
    async def monitoring_middleware(request: Request, call_next):
        start_time = time.time()

        logger.debug(f"Request started: {request.method} {request.url.path}")

        try:
            response = await call_next(request)

            process_time = time.time() - start_time
            if process_time > 5:
                logger.warning(
                    f"Slow request: {request.method} {request.url.path} "
                    f"took {process_time:.2f}s"
                )
            elif process_time > 30:
                logger.error(
                    f"Very slow request: {request.method} {request.url.path} "
                    f"took {process_time:.2f}s - consider optimizing"
                )

            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"after {process_time:.2f}s - Error: {e}"
            )
            raise

    _configure_middleware(app)
    _register_routes(app)

    return app


def _configure_middleware(app: FastAPI) -> None:
    """Configure application middleware."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Requested-With", "Accept", "Origin"],
    )


def _register_routes(app: FastAPI) -> None:
    """Register application routes."""
    app.add_api_route("/health", health_check, methods=["GET"])
    app.include_router(questions_router)
    app.include_router(answers_router)


async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
    }


app = create_app()
