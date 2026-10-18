from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_returns_local_default():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "local"}


def test_metrics_returns_prometheus_text():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "tinyops_app_info" in response.text
    assert "tinyops_requests_total" in response.text
