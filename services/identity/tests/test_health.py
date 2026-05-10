from fastapi.testclient import TestClient

from identity.main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status() -> None:
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_is_json() -> None:
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]
