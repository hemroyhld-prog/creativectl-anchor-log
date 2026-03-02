import time
from collections import defaultdict

# Start time for uptime
START_TIME = time.time()

# Counters
REQUEST_COUNT = 0
STATUS_COUNT = defaultdict(int)

# Histogram buckets (milliseconds)
HISTOGRAM_BUCKETS = [50, 100, 300, 1000]

LATENCY_BUCKET_COUNTS = {le: 0 for le in HISTOGRAM_BUCKETS}
LATENCY_BUCKET_COUNTS["+Inf"] = 0

LATENCY_SUM = 0.0
LATENCY_COUNT = 0


def increment_metrics(status_code: int, duration_ms: float):
    global REQUEST_COUNT, LATENCY_SUM, LATENCY_COUNT

    REQUEST_COUNT += 1
    STATUS_COUNT[status_code] += 1

    LATENCY_SUM += duration_ms
    LATENCY_COUNT += 1

    # Cumulative histogram buckets
    for le in HISTOGRAM_BUCKETS:
        if duration_ms <= le:
            LATENCY_BUCKET_COUNTS[le] += 1

    LATENCY_BUCKET_COUNTS["+Inf"] += 1


def prometheus_metrics():
    lines = []

    # -----------------------------
    # Total Requests
    # -----------------------------
    lines.append("# HELP app_requests_total Total HTTP requests")
    lines.append("# TYPE app_requests_total counter")
    lines.append(f"app_requests_total {REQUEST_COUNT}")

    # -----------------------------
    # Status Codes
    # -----------------------------
    lines.append("# HELP app_status_count HTTP status codes")
    lines.append("# TYPE app_status_count counter")
    for status, count in STATUS_COUNT.items():
        lines.append(
            f'app_status_count{{status="{status}"}} {count}'
        )

    # -----------------------------
    # Histogram
    # -----------------------------
    lines.append("# HELP app_request_duration_ms Request duration in milliseconds")
    lines.append("# TYPE app_request_duration_ms histogram")

    for le in HISTOGRAM_BUCKETS:
        lines.append(
            f'app_request_duration_ms_bucket{{le="{le}"}} {LATENCY_BUCKET_COUNTS[le]}'
        )

    lines.append(
        f'app_request_duration_ms_bucket{{le="+Inf"}} {LATENCY_BUCKET_COUNTS["+Inf"]}'
    )

    lines.append(f"app_request_duration_ms_count {LATENCY_COUNT}")
    lines.append(f"app_request_duration_ms_sum {round(LATENCY_SUM, 2)}")

    # -----------------------------
    # Uptime
    # -----------------------------
    uptime = round(time.time() - START_TIME, 2)
    lines.append("# HELP app_uptime_seconds Application uptime in seconds")
    lines.append("# TYPE app_uptime_seconds gauge")
    lines.append(f"app_uptime_seconds {uptime}")

    return "\n".join(lines)
