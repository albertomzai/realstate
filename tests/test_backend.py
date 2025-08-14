import os
import json
import pytest

from backend import create_app, db
from backend.models import Propietario, Inmueble

@pytest.fixture(scope='module')
def client():
    # Usamos una base de datos en memoria para los tests
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

        # Creamos un propietario de prueba
        propietario = Propietario(nombre='Juan', email='juan@example.com')
        db.session.add(propietario)
        db.session.commit()

    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def propietario_id(client):
    # Obtener el id del propietario creado en la fixture anterior
    r = client.get('/api/propietarios')
    data = json.loads(r.data)
    return data[0]['id'] if data else None

def test_create_inmueble(client, propietario_id):
    payload = {
        'direccion': 'Calle Falsa 123',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 800.0,
        'propietario_id': propietario_id
    }

    r = client.post('/api/inmuebles', json=payload)
    assert r.status_code == 201
    data = json.loads(r.data)
    assert data['direccion'] == payload['direccion']
    assert data['propietario']['id'] == propietario_id

def test_get_inmuebles(client):
    r = client.get('/api/inmuebles')
    assert r.status_code == 200
    data = json.loads(r.data)
    assert isinstance(data, list)

def test_update_inmueble(client, propietario_id):
    # Creamos un inmueble para actualizar
    payload_create = {
        'direccion': 'Calle 1',
        'ciudad': 'Barcelona',
        'propietario_id': propietario_id
    }
    r = client.post('/api/inmuebles', json=payload_create)
    inmueble_id = json.loads(r.data)['id']

    # Actualizamos el campo direccion
    payload_update = {'direccion': 'Calle 2'}
    r = client.put(f'/api/inmuebles/{inmueble_id}', json=payload_update)
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data['direccion'] == 'Calle 2'

def test_delete_inmueble(client, propietario_id):
    # Creamos un inmueble para borrar
    payload_create = {
        'direccion': 'Calle X',
        'ciudad': 'Sevilla',
        'propietario_id': propietario_id
    }
    r = client.post('/api/inmuebles', json=payload_create)
    inmueble_id = json.loads(r.data)['id']

    # Eliminamos el inmueble
    r = client.delete(f'/api/inmuebles/{inmueble_id}')
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data['message'] == 'Inmueble deleted'

def test_get_propietarios(client):
    r = client.get('/api/propietarios')
    assert r.status_code == 200
    data = json.loads(r.data)
    assert isinstance(data, list)
    assert len(data) >= 1