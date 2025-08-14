import pytest

from backend import create_app, db as _db

@pytest.fixture(scope='module')

def test_client():
    app = create_app()
    # Usar base de datos en memoria para tests
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        _db.create_all()

        # Crear un propietario de prueba
        from backend.models import Propietario, Inmueble
        propietario = Propietario(nombre='Juan', email='juan@example.com')
        _db.session.add(propietario)
        _db.session.commit()

    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')

def propietario_id():
    return 1

def test_get_inmuebles(test_client):
    response = test_client.get('/api/inmuebles')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_inmueble(test_client, propietario_id):
    payload = {
        'direccion': 'Calle Falsa 123',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 800.0,
        'disponible': True,
        'propietario_id': propietario_id
    }
    response = test_client.post('/api/inmuebles', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['direccion'] == payload['direccion']

def test_update_inmueble(test_client, propietario_id):
    # Crear inmueble a actualizar
    from backend.models import Inmueble
    with _db.session.begin():
        inmueble = Inmueble(direccion='Calle 1', ciudad='Barcelona', tipo='Casa', precio_alquiler=1200, disponible=True, propietario_id=propietario_id)
        _db.session.add(inmueble)
        _db.session.flush()
        inmueble_id = inmueble.id

    update_payload = {'precio_alquiler': 1300}
    response = test_client.put(f'/api/inmuebles/{inmueble_id}', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['precio_alquiler'] == 1300

def test_delete_inmueble(test_client, propietario_id):
    # Crear inmueble a eliminar
    from backend.models import Inmueble
    with _db.session.begin():
        inmueble = Inmueble(direccion='Calle 2', ciudad='Sevilla', tipo='Local', precio_alquiler=500, disponible=True, propietario_id=propietario_id)
        _db.session.add(inmueble)
        _db.session.flush()
        inmueble_id = inmueble.id

    response = test_client.delete(f'/api/inmuebles/{inmueble_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_get_propietarios(test_client):
    response = test_client.get('/api/propietarios')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1