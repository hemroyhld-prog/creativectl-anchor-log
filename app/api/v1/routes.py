from fastapi import APIRouter
from app.db import get_total_requests
from time import time

router = APIRouter()

start_time = time()


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.get("/readiness")
def readiness():
    try:
        total = get_total_requests()
        return {
            "status": "ready",
            "total_requests": total
        }
    except Exception:
        return {
            "status": "not_ready"
        }


@router.get("/metrics")
def metrics():
    uptime = time() - start_time
    return {
        "engine": "running",
        "version": "0.1",
        "total_requests": get_total_requests(),
        "uptime_seconds": round(uptime, 2)
    }

