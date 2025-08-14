import pytest

from backend import create_app, db, Propietario, Inmueble

@pytest.fixture(scope='module')
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Seed a propietario for tests
            prop = Propietario(nombre='Juan', email='juan@example.com')
            db.session.add(prop)
            db.session.commit()

        yield client

def test_get_inmuebles_empty(client):
    response = client.get('/api/inmuebles')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_and_get_inmueble(client):
    # Create inmueble
    data = {
        'direccion': 'Calle Falsa 123',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 1200.0,
        'propietario_id': 1
    }
    post_resp = client.post('/api/inmuebles', json=data)
    assert post_resp.status_code == 201

    # Get list
    get_resp = client.get('/api/inmuebles')
    inmuebles = get_resp.get_json()
    assert len(inmuebles) == 1
    inmueble = inmuebles[0]
    assert inmueble['direccion'] == data['direccion']
    assert inmueble['propietario']['nombre'] == 'Juan'

def test_update_inmueble(client):
    # Assume inmueble id 1 exists from previous test
    update_data = {'precio_alquiler': 1300.0, 'disponible': False}
    put_resp = client.put('/api/inmuebles/1', json=update_data)
    assert put_resp.status_code == 200

    get_resp = client.get('/api/inmuebles')
    inmueble = get_resp.get_json()[0]
    assert inmueble['precio_alquiler'] == 1300.0
    assert inmueble['disponible'] is False

def test_delete_inmueble(client):
    del_resp = client.delete('/api/inmuebles/1')
    assert del_resp.status_code == 200

    get_resp = client.get('/api/inmuebles')
    assert get_resp.get_json() == []