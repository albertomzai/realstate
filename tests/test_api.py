"""Test suite for the backend API."""

import json
import pytest

from backend import create_app, _db as db

@pytest.fixture(scope='module')
def app():
    """Create a test Flask application with an in-memory SQLite database."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_inmuebles_empty(client):
    response = client.get('/api/inmuebles')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_inmueble(client):
    payload = {
        'direccion': 'Calle Falsa 123',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 1200.5,
        'disponible': True
    }
    response = client.post('/api/inmuebles', json=payload)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['direccion'] == payload['direccion']

def test_update_inmueble(client):
    # First create an inmueble to update
    payload = {
        'direccion': 'Calle 1',
        'ciudad': 'Barcelona',
        'tipo': 'Casa'
    }
    post_resp = client.post('/api/inmuebles', json=payload)
    inmueble_id = json.loads(post_resp.data)['id']

    update_payload = {"precio_alquiler": 2000}
    put_resp = client.put(f'/api/inmuebles/{inmueble_id}', json=update_payload)
    assert put_resp.status_code == 200
    updated_data = json.loads(put_resp.data)
    assert updated_data['precio_alquiler'] == 2000

def test_delete_inmueble(client):
    # Create an inmueble to delete
    payload = {"direccion": "Calle X", "ciudad": "Valencia", "tipo": "Local"}
    post_resp = client.post('/api/inmuebles', json=payload)
    inmueble_id = json.loads(post_resp.data)['id']

    del_resp = client.delete(f'/api/inmuebles/{inmueble_id}')
    assert del_resp.status_code == 200

    # Verify deletion
    get_resp = client.get('/api/inmuebles')
    data = json.loads(get_resp.data)
    ids = [i['id'] for i in data]
    assert inmueble_id not in ids

def test_get_propietarios(client):
    response = client.get('/api/propietarios')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)