import pytest

from backend import create_app, _db

@pytest.fixture(scope='module')
def app():
    app = create_app()
    # Configurar la base de datos en memoria para pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        _db.init_app(app)
        _db.create_all()
    yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_get_propietarios(client, app):
    # Crear un propietario de prueba
    with app.app_context():
        from backend.models.propietario import Propietario
        prop = Propietario(nombre='Test', email='test@example.com')
        _db.session.add(prop)
        _db.session.commit()

    resp = client.get('/api/propietarios/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(p['nombre'] == 'Test' for p in data)

def test_crud_inmueble(client, app):
    # Crear propietario primero
    with app.app_context():
        from backend.models.propietario import Propietario
        prop = Propietario(nombre='Owner', email='owner@example.com')
        _db.session.add(prop)
        _db.session.commit()

    # POST crear inmueble
    payload = {
        'direccion': 'Calle 1',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 800.0,
        'propietario_id': prop.id
    }
    resp = client.post('/api/inmuebles/', json=payload)
    assert resp.status_code == 201
    inmueble_data = resp.get_json()
    assert inmueble_data['direccion'] == 'Calle 1'

    # GET lista de inmuebles
    resp = client.get('/api/inmuebles/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1

    # PUT actualizar inmueble
    update_payload = {'precio_alquiler': 850.0}
    resp = client.put(f'/api/inmuebles/{inmueble_data['id']}', json=update_payload)
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated['precio_alquiler'] == 850.0

    # DELETE eliminar inmueble
    resp = client.delete(f'/api/inmuebles/{inmueble_data['id']}')
    assert resp.status_code == 200
    # Verificar que ya no existe
    resp = client.get('/api/inmuebles/')
    data = resp.get_json()
    assert all(i['id'] != inmueble_data['id'] for i in data)