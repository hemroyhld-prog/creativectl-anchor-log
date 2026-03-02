from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.api.v1.routes import router as v1_router
from app.db import init_db, increment_requests
from app.config import get_settings
from app.middleware.request_id import request_id_middleware
from app.middleware.rate_limit import rate_limit_middleware
from app.metrics import increment_metrics, prometheus_metrics

import time
import json
import logging
from datetime import datetime

settings = get_settings()

# ------------------------
# Logger Setup
# ------------------------
logger = logging.getLogger("engine")
logger.setLevel(settings.log_level)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.propagate = False

# ------------------------
# App Init
# ------------------------
app = FastAPI(title=f"{settings.app_name} v{settings.version}")

# ------------------------
# Middleware Order (IMPORTANT)
# ------------------------

# 1️⃣ Request ID
app.middleware("http")(request_id_middleware)

# 2️⃣ Rate Limit
app.middleware("http")(rate_limit_middleware)

# 3️⃣ Logging + Metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    increment_requests()

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    duration_ms = round(duration * 1000, 2)
    increment_metrics(response.status_code, duration_ms)

    client_ip = request.client.host if request.client else "unknown"
    request_id = getattr(request.state, "request_id", "unknown")

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "client_ip": client_ip,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": duration_ms,
    }

    logger.info(json.dumps(log_data))
    return response

# ------------------------
# Lifecycle
# ------------------------

@app.on_event("startup")
def startup():
    logger.info("Application startup initiated")
    init_db()
    logger.info("Application startup complete")

@app.on_event("shutdown")
def shutdown():
    logger.info("Application shutdown complete")

# ------------------------
# Routes
# ------------------------

app.include_router(v1_router, prefix="/api/v1")

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return prometheus_metrics()
