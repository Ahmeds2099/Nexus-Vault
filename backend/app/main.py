"""
main.py — FastAPI application entry point.

This file:
1. Creates the FastAPI app instance
2. Configures middleware (CORS)
3. Registers all routers
4. Creates database tables on startup
5. Provides health check and root endpoints
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings
from app.database import Base, engine
from app.routes.items import router as items_router

settings = get_settings()


# ── Lifespan (startup/shutdown events) ────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs on startup and shutdown.
    Creates DB tables if they don't exist yet.
    """
    # STARTUP
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print("📦 Creating database tables if not exists...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready")

    yield  # App runs here

    # SHUTDOWN
    print("👋 Shutting down Nexus Vault API...")


# ── App Instance ───────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Local-first content saving system — save anything, find it instantly.",
    docs_url="/docs",       # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc at http://localhost:8000/redoc
    lifespan=lifespan,
)


# ── CORS Middleware ────────────────────────────────────────────────────────────
# Allows the Next.js frontend (running on port 3000) to talk to this API

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# ── Custom Exception Handlers ─────────────────────────────────────────────────

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """Return HTTP errors in our standard { success, data, error } format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": str(exc.detail),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Return Pydantic validation errors in a human-readable format."""
    errors = []
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"])
        errors.append(f"{field}: {error['msg']}")

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "error": "Validation failed: " + "; ".join(errors),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all for unexpected server errors — never expose internals."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": "Internal server error. Please try again.",
        },
    )


# ── Root Routes ────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """API root — confirms server is running."""
    return {
        "success": True,
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs",
        },
        "error": None,
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"success": True, "data": {"status": "healthy"}, "error": None}


# ── Register Routers ───────────────────────────────────────────────────────────

app.include_router(items_router)
