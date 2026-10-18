import os
import time

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI(title="TinyOps Status API")
APP_VERSION = os.getenv("APP_VERSION", "local")
START_TIME = time.time()
REQUEST_COUNT = 0


@app.middleware("http")
async def count_requests(request: Request, call_next):
    global REQUEST_COUNT
    response = await call_next(request)
    REQUEST_COUNT += 1
    return response


@app.get("/")
def read_root():
    return {
        "message": "TinyOps Status API",
        "health": "/health",
        "version": "/version",
        "metrics": "/metrics",
    }


@app.get("/health")
def read_health():
    return {"status": "ok"}


@app.get("/version")
def read_version():
    return {"version": APP_VERSION}


@app.get("/metrics", response_class=PlainTextResponse)
def read_metrics():
    uptime_seconds = int(time.time() - START_TIME)
    return "\n".join(
        [
            "# HELP tinyops_app_info Application version information.",
            "# TYPE tinyops_app_info gauge",
            f'tinyops_app_info{{version="{APP_VERSION}"}} 1',
            "# HELP tinyops_requests_total Total HTTP requests served.",
            "# TYPE tinyops_requests_total counter",
            f"tinyops_requests_total {REQUEST_COUNT}",
            "# HELP tinyops_uptime_seconds Application uptime in seconds.",
            "# TYPE tinyops_uptime_seconds gauge",
            f"tinyops_uptime_seconds {uptime_seconds}",
            "",
        ]
    )
