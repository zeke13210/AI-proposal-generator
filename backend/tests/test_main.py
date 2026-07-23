import os
os.environ["TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Unit Tests ---

def test_validate_input_empty():
    response = client.post("/api/generate", json={"notes": "   "})
    assert response.status_code == 400
    assert "Notes cannot be empty" in response.json()["detail"]

def test_validate_input_too_long():
    long_notes = "a" * 10001
    response = client.post("/api/generate", json={"notes": long_notes})
    assert response.status_code == 422
    assert any("at most 10000 characters" in str(e["msg"]) for e in response.json()["detail"])

# --- Integration Tests ---

def test_generate_proposal_flow_happy_path():
    sample_notes = "Client wants a simple website, but maybe some SEO, and possibly full social media management."
    response = client.post("/api/generate", json={"notes": sample_notes})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "title" in data
    assert "summary" in data
    assert "deliverables" in data
    assert "timeline" in data
    assert "estimatedHours" in data
    assert "totalPrice" in data
    
    # Calculate pricing verification (estimatedHours * 100)
    assert data["totalPrice"] == data["estimatedHours"] * 100
