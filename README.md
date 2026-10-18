# TinyOps - A Minimal Status API with DevOps Automation

TinyOps is a small Python HTTP API built with FastAPI. The baseline version was intentionally minimal, and the DevOps implementation adds only the operational pieces needed to build, test, containerize, and run it on Kubernetes.

## What It Does

- `GET /` returns basic application information.
- `GET /health` returns `{"status": "ok"}` with HTTP 200.
- `GET /version` returns the running application version.
- `GET /metrics` returns lightweight Prometheus-style text metrics.

## Prerequisites

- Python 3.13 or compatible Python 3 version
- Git
- Docker, for container builds
- kubectl and Minikube or another local Kubernetes cluster, for Kubernetes testing

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements-dev.txt
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

## Docker

Build the container image:

```powershell
docker build -t tinyops:local .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 -e APP_VERSION=local-docker tinyops:local
```

Verify it:

```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
```

## Kubernetes

For Minikube, build the image inside Minikube's Docker environment or load the image into the cluster, then apply the manifest:

```powershell
minikube start
minikube image build -t tinyops:local .
kubectl apply -f k8s/tinyops.yaml
kubectl rollout status deployment/tinyops-api
kubectl port-forward service/tinyops-api 8000:80
```

Verify it:

```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/metrics
```

Clean up:

```powershell
kubectl delete -f k8s/tinyops.yaml
```

## CI

GitHub Actions runs on pushes and pull requests. The workflow installs dependencies, runs pytest, and builds the Docker image.

## Architecture And Operations

Request path in Kubernetes:

1. A user sends an HTTP request to the Kubernetes Service.
2. The Service forwards traffic to a Pod selected by `app.kubernetes.io/name: tinyops-api`.
3. The Pod runs the `tinyops:local` container.
4. Uvicorn serves the FastAPI application on port `8000`.

The Kubernetes manifest uses a Deployment because the API is stateless. It uses a ClusterIP Service because local access can be done with `kubectl port-forward` and the app does not need public exposure.

## Release And Recovery

The original baseline is preserved at commit `6f1101c079bdaa9a7b3cf4cb1927c833cd39b90d`. All DevOps improvements are kept in one pull request.

The running version can be checked with:

```powershell
curl http://127.0.0.1:8000/version
```

If a Kubernetes rollout fails, recover with:

```powershell
kubectl rollout undo deployment/tinyops-api
kubectl rollout status deployment/tinyops-api
curl http://127.0.0.1:8000/health
```

## Observability And Security

- `/health` is used for Kubernetes readiness and liveness probes.
- `/metrics` exposes simple Prometheus-style text for version, request count, and uptime.
- Uvicorn logs go to standard output and can be viewed with `kubectl logs deployment/tinyops-api`.
- The app needs no secrets.
- The container runs as a non-root user.
- The Kubernetes manifest disables privilege escalation, drops Linux capabilities, and uses a read-only root filesystem.

## Verified Evidence And Limitations

Verified locally:

- `python -m pytest` passed with `3 passed, 1 warning`.
- `/health` returned `{"status":"ok"}` from local Uvicorn.
- `/version` returned `{"version":"local"}` from local Uvicorn.
- `/metrics` returned HTTP 200 and Prometheus-style text.
- `k8s/tinyops.yaml` parsed as one Deployment and one Service.
- `docker build -t tinyops:local .` completed successfully after Docker Desktop was started.
- `docker run --rm -p 8002:8000 -e APP_VERSION=local-docker tinyops:local` served `/health` and `/version` successfully.
- Minikube was recreated successfully with the Docker driver.
- `kubectl apply -f k8s/tinyops.yaml` created the Deployment and Service.
- `kubectl rollout status deployment/tinyops-api` completed successfully.
- The Kubernetes Pod reached `1/1 Running`.
- `kubectl port-forward service/tinyops-api 8003:80` exposed the Service locally.
- Kubernetes `/health` returned `{"status":"ok"}`.
- Kubernetes `/version` returned `{"version":"devops-local"}`.
- Kubernetes `/metrics` returned HTTP 200 and Prometheus-style text.
- Kubernetes logs showed successful startup and request logs.

Verified in GitHub Actions:

- The `test-and-build` workflow passed.
- The workflow ran pytest and built the Docker image.

Local limitation:

- The first Minikube attempt was interrupted by a stale/broken cluster state. Recreating the Minikube cluster fixed it, and Kubernetes verification then passed.

## Viva Short Answers

- Deployment instead of StatefulSet: the API is stateless and does not need persistent identity or storage.
- ClusterIP instead of LoadBalancer: local `kubectl port-forward` is enough for this project.
- Health means `/health` returns HTTP 200, the Pod is ready, and logs do not show repeated crashes.
- Recovery means rolling back the Deployment and verifying `/health`, `/version`, and logs.
- Terraform and cloud are not used because the guide allows local Kubernetes and excludes Terraform from required scope.
