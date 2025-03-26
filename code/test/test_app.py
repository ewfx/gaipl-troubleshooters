import pytest
from flask import Flask
import code.src.backend.app as app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_handle_query(client):
    response = client.post('/query', json={'query': 'check memory'})
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert "runbook_status" in data

def test_handle_heal(client):
    response = client.post('/heal', json={'issue_description': 'Memory leak detected'})
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert data["status"] in ["success", "error"]

def test_generate_runbook(client):
    response = client.post('/generate_runbook', json={'issue_description': 'CPU spike detected'})
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert data["status"] in ["success", "error"]

def test_generate_heal_script(client):
    response = client.post('/generate_heal_script', json={'issue_description': 'Network issue detected'})
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert data["status"] in ["success", "error"]

def test_get_incidents(client):
    response = client.get('/incidents')
    assert response.status_code == 200

def test_get_change_requests(client):
    response = client.get('/change_requests')
    assert response.status_code == 200

def test_cr_tracker(client):
    response = client.post('/cr_tracker', json={
        'incident': {'id': '123', 'description': 'Test incident'},
        'change_requests': [{'id': 'cr1', 'description': 'Test change request'}]
    })
    assert response.status_code == 200 or response.status_code == 400
    data = response.get_json()
    if response.status_code == 200:
        assert "impact_analysis" in data
    else:
        assert "error" in data

def test_apps_affected(client):
    response = client.post('/apps_affected', json={'incident_id': '123'})
    assert response.status_code == 200 or response.status_code == 400
    data = response.get_json()
    if response.status_code == 200:
        assert "apps_affected_analysis" in data
    else:
        assert "error" in data