"""
Solar Predictive Maintenance System - FastAPI Backend
Entry point for the API server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.routers import sensor, analytics, health, alert
from backend.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Solar Predictive Maintenance System",
    description="AI-driven predictive maintenance for solar panels",
    version="1.0.0"
)

# CORS configuration for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(sensor.router, prefix="/api/sensor", tags=["Sensor Data"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(alert.router, prefix="/api/alerts", tags=["Alerts"])

@app.get("/")
async def root():
    return {
        "message": "Solar Predictive Maintenance System API",
        "version": "1.0.0",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
