import json

import pytest
from backend import create_app, db
from backend.models import Propietario, Inmueble

@pytest.fixture
def app():
    """Create a fresh Flask application for each test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        # Seed a propietario for tests
        propietario = Propietario(nombre='Juan', email='juan@example.com')
        db.session.add(propietario)
        db.session.commit()

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
        'precio_alquiler': 1200.0,
        'disponible': True,
        'propietario_id': 1
    }
    response = client.post('/api/inmuebles', json=payload)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['direccion'] == payload['direccion']
    assert 'propietario' in data and data['propietario']['id'] == 1

def test_update_inmueble(client):
    # First create an inmueble
    client.post('/api/inmuebles', json={
        'direccion': 'Calle X',
        'ciudad': 'Barcelona',
        'tipo': 'Casa',
        'precio_alquiler': 1500,
        'disponible': True,
        'propietario_id': 1
    })

    update_payload = {"ciudad": "Valencia", "precio_alquiler": 1600}
    response = client.put('/api/inmuebles/1', json=update_payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['ciudad'] == 'Valencia'
    assert data['precio_alquiler'] == 1600

def test_delete_inmueble(client):
    client.post('/api/inmuebles', json={
        'direccion': 'Calle Y',
        'ciudad': 'Sevilla',
        'tipo': 'Local',
        'precio_alquiler': 800,
        'disponible': True,
        'propietario_id': 1
    })

    response = client.delete('/api/inmuebles/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Inmueble deleted'

def test_get_propietarios(client):
    response = client.get('/api/propietarios')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 1