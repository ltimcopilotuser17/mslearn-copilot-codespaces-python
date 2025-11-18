import pytest
from fastapi.testclient import TestClient
from webapp.main import app

client = TestClient(app)


def test_get_cities_france():
    """Test getting cities for France"""
    response = client.post("/cities", json={"country": "France"})
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "France"
    assert "cities" in data
    assert len(data["cities"]) == 5
    assert "Paris" in data["cities"]
    assert "Lyon" in data["cities"]


def test_get_cities_usa():
    """Test getting cities for USA"""
    response = client.post("/cities", json={"country": "USA"})
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "USA"
    assert "cities" in data
    assert len(data["cities"]) == 5
    assert "New York" in data["cities"]


def test_get_cities_germany():
    """Test getting cities for Germany"""
    response = client.post("/cities", json={"country": "Germany"})
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "Germany"
    assert "cities" in data
    assert "Berlin" in data["cities"]


def test_get_cities_unknown_country():
    """Test getting cities for an unknown country"""
    response = client.post("/cities", json={"country": "Atlantis"})
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "Atlantis"
    assert data["cities"] == []
    assert "message" in data
    assert data["message"] == "No cities found for Atlantis"


def test_get_cities_empty_string():
    """Test getting cities for an empty country name"""
    response = client.post("/cities", json={"country": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == ""
    assert data["cities"] == []
    assert "message" in data


def test_get_cities_all_known_countries():
    """Test that all hardcoded countries return non-empty city lists"""
    known_countries = [
        "France", "Germany", "Spain", "Italy", "USA", "Japan", "UK"
    ]

    for country in known_countries:
        response = client.post("/cities", json={"country": country})
        assert response.status_code == 200
        data = response.json()
        assert data["country"] == country
        assert len(data["cities"]) > 0
        assert "message" not in data
