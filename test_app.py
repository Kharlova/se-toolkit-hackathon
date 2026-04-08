"""
Tests for Plant Watering Tracker API
Run with: python -m pytest test_app.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_create_plant():
    """Test creating a new plant"""
    response = client.post("/api/plants", json={
        "name": "Test Plant",
        "watering_frequency_days": 7
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Plant added successfully"

def test_get_plants_empty():
    """Test getting plants when none exist"""
    response = client.get("/api/plants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_plant():
    """Test creating a plant and retrieving it"""
    # Create a plant
    create_response = client.post("/api/plants", json={
        "name": "Monstera",
        "watering_frequency_days": 7
    })
    assert create_response.status_code == 200
    plant_id = create_response.json()["id"]
    
    # Get plants
    get_response = client.get("/api/plants")
    assert get_response.status_code == 200
    plants = get_response.json()
    assert len(plants) > 0
    
    # Find our plant
    plant = next((p for p in plants if p["id"] == plant_id), None)
    assert plant is not None
    assert plant["name"] == "Monstera"
    assert plant["watering_frequency_days"] == 7

def test_water_plant():
    """Test marking a plant as watered"""
    # Create a plant
    create_response = client.post("/api/plants", json={
        "name": "Cactus",
        "watering_frequency_days": 14
    })
    assert create_response.status_code == 200
    plant_id = create_response.json()["id"]
    
    # Water the plant
    water_response = client.post(f"/api/plants/{plant_id}/water")
    assert water_response.status_code == 200
    assert "watered successfully" in water_response.json()["message"]
    
    # Check that last_watered is updated
    get_response = client.get("/api/plants")
    plants = get_response.json()
    plant = next((p for p in plants if p["id"] == plant_id), None)
    assert plant["last_watered"] is not None

def test_delete_plant():
    """Test deleting a plant"""
    # Create a plant
    create_response = client.post("/api/plants", json={
        "name": "Fern",
        "watering_frequency_days": 3
    })
    assert create_response.status_code == 200
    plant_id = create_response.json()["id"]
    
    # Delete the plant
    delete_response = client.delete(f"/api/plants/{plant_id}")
    assert delete_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get("/api/plants")
    plants = get_response.json()
    plant_ids = [p["id"] for p in plants]
    assert plant_id not in plant_ids

def test_water_nonexistent_plant():
    """Test watering a plant that doesn't exist"""
    response = client.post("/api/plants/99999/water")
    assert response.status_code == 404

def test_delete_nonexistent_plant():
    """Test deleting a plant that doesn't exist"""
    response = client.delete("/api/plants/99999")
    assert response.status_code == 404
