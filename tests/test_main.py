"""Tests for the lighting control application."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel import SQLModel
from app.main import app
from app.database import get_session


# Create a test database
@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_add_light_switch(client: TestClient):
    """Test adding a new light switch."""
    response = client.post(
        "/api/switches",
        json={"name": "Kitchen Light"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Kitchen Light"
    assert data["is_on"] is False
    assert "id" in data


def test_list_light_switches(client: TestClient):
    """Test listing all light switches."""
    # Add some switches
    client.post("/api/switches", json={"name": "Light 1"})
    client.post("/api/switches", json={"name": "Light 2"})

    response = client.get("/api/switches")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_toggle_light_switch(client: TestClient):
    """Test toggling a light switch."""
    # Add a switch
    add_response = client.post(
        "/api/switches",
        json={"name": "Test Light"}
    )
    switch_id = add_response.json()["id"]

    # Toggle on
    toggle_response = client.put(
        f"/api/switches/{switch_id}",
        json={"is_on": True}
    )
    assert toggle_response.status_code == 200
    data = toggle_response.json()
    assert data["is_on"] is True

    # Toggle off
    toggle_response = client.put(
        f"/api/switches/{switch_id}",
        json={"is_on": False}
    )
    assert toggle_response.status_code == 200
    data = toggle_response.json()
    assert data["is_on"] is False


def test_delete_light_switch(client: TestClient):
    """Test deleting a light switch."""
    # Add a switch
    add_response = client.post(
        "/api/switches",
        json={"name": "Test Light"}
    )
    switch_id = add_response.json()["id"]

    # Delete switch
    delete_response = client.delete(f"/api/switches/{switch_id}")
    assert delete_response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/api/switches/{switch_id}")
    assert get_response.status_code == 404
