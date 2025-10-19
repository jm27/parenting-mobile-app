from fastapi import APIRouter
from datetime import datetime
import psutil
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "0.1.0",
            "system": {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "disk_usage_percent": disk.percent,
                "available_memory_gb": round(memory.available / (1024**3), 2)
            },
            "database": "connected",  # TODO: Add actual DB health check
            "openai": "configured"    # TODO: Add OpenAI API check
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }
