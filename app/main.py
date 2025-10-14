"""
FastAPI application for AI Tutor Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db

# FastAPI app will be created below with lifespan


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    yield

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "environment": settings.environment,
        "database_url": settings.database_url.split("@")[-1] if "@" in settings.database_url else "configured"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug
    }


# Include API routes (will be added later)
# from app.api.v1 import students, programs, materials, messages, schedule, assignments
# app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
# app.include_router(programs.router, prefix="/api/v1/programs", tags=["programs"])
# app.include_router(materials.router, prefix="/api/v1/materials", tags=["materials"])
# app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
# app.include_router(schedule.router, prefix="/api/v1/schedule", tags=["schedule"])
# app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["assignments"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
