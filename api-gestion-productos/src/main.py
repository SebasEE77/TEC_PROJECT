"""Main FastAPI application for Food Inventory API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from models.db import create_tables
from routes.products import router as products_router
from routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Creates database tables on startup.
    """
    # Create tables on startup
    create_tables()
    yield


# Create FastAPI application
app = FastAPI(
    title="Food Inventory API",
    description="API REST para la gestión de productos comestibles en un inventario",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los endpoints para usuarios y productos
app.include_router(users_router)
app.include_router(products_router)

if __name__ == "__main__":
    print("🚀 Starting Food Inventory API...")
    print("📚 API: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

