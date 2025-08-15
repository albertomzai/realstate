import json

import pytest
from backend import create_app, db
from backend.models import Inmueble, Propietario

@pytest.fixture(scope='module')
def app():
    # Use an in-memory SQLite database for tests
    test_config = {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    app = create_app(test_config)
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_get_inmuebles_empty(client):
    response = client.get('/api/inmuebles')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_update_delete_inmueble(client, app):
    # Create propietario first
    with app.app_context():
        prop = Propietario(nombre='Juan', email='juan@example.com')
        db.session.add(prop)
        db.session.commit()

    payload = {
        'direccion': 'Calle Falsa 123',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 800.0,
        'disponible': True,
        'propietario_id': prop.id
    }

    # POST create
    resp = client.post('/api/inmuebles', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 201
    inmueble_data = resp.get_json()
    inmueble_id = inmueble_data['id']

    # GET should return the created inmueble
    get_resp = client.get('/api/inmuebles')
    assert get_resp.status_code == 200
    inmuebles_list = get_resp.get_json()
    assert any(i['id'] == inmueble_id for i in inmuebles_list)

    # PUT update
    update_payload = {'precio_alquiler': 850.0}
    put_resp = client.put(f'/api/inmuebles/{inmueble_id}', data=json.dumps(update_payload), content_type='application/json')
    assert put_resp.status_code == 200
    updated_data = put_resp.get_json()
    assert updated_data['precio_alquiler'] == 850.0

    # DELETE
    del_resp = client.delete(f'/api/inmuebles/{inmueble_id}')
    assert del_resp.status_code == 200
    assert del_resp.get_json()['message'] == 'Inmueble deleted successfully'

def test_get_propietarios(client, app):
    with app.app_context():
        # Ensure there is at least one propietario
        prop = Propietario(nombre='Ana', email='ana@example.com')
        db.session.add(prop)
        db.session.commit()

    resp = client.get('/api/propietarios')
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(p['nombre'] == 'Ana' for p in data)