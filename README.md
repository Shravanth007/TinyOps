# TinyOps - A Minimal Status API with DevOps Automation

TinyOps is a small Python HTTP API built with FastAPI. The baseline version is intentionally minimal so the original application is easy to compare with later DevOps improvements.

## What It Does

- `GET /` returns basic application information.
- `GET /health` returns `{"status": "ok"}` with HTTP 200.

## Prerequisites

- Python 3.13 or compatible Python 3 version
- Git

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open the health endpoint:

```powershell
curl http://127.0.0.1:8000/health
```

Run tests:

```powershell
python -m pytest
```

## Baseline Scope

This baseline contains only the original minimal application and a basic automated test. Docker, Kubernetes, CI/CD, monitoring, and release automation are intentionally not included in the baseline phase.
