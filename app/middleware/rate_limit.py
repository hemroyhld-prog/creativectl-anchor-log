import time
from fastapi import Request
from starlette.responses import JSONResponse

# Sliding window stores
ip_buckets = {}
api_key_buckets = {}

IP_LIMIT = 20
API_KEY_LIMIT = 50
WINDOW_SIZE = 60  # seconds


def is_rate_limited(bucket: dict, key: str, limit: int):
    now = time.time()

    if key not in bucket:
        bucket[key] = []

    # Remove expired timestamps
    bucket[key] = [t for t in bucket[key] if now - t < WINDOW_SIZE]

    if len(bucket[key]) >= limit:
        return True

    bucket[key].append(now)
    return False


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    api_key = request.headers.get("x-api-key")

    # IP check
    if is_rate_limited(ip_buckets, client_ip, IP_LIMIT):
        return JSONResponse(
            status_code=429,
            content={"detail": "IP rate limit exceeded"}
        )

    # API key check (if present)
    if api_key:
        if is_rate_limited(api_key_buckets, api_key, API_KEY_LIMIT):
            return JSONResponse(
                status_code=429,
                content={"detail": "API key rate limit exceeded"}
            )

    response = await call_next(request)
    return response
