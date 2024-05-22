import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_task(client):
    response = client.post('/tasks', json={'name': 'Test Task'})
    assert response.status_code == 201
    assert response.json['name'] == 'Test Task'

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)

