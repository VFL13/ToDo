from starlette.testclient import TestClient

from .routes import core_router

client = TestClient(core_router)


def test_healthcheck():
    resp = client.get("/")
    assert resp.status_code == 200, "DANGGER: App is unhealthy"