import json

from backend import create_app, db as _db

@pytest.fixture(scope='module')
def app():
    app = create_app()
    # Configurar la base de datos en memoria para pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_and_get_inmueble(client, app):
    # Crear propietario primero
    from backend.models import Propietario
    with app.app_context():
        prop = Propietario(nombre='Juan', email='juan@example.com')
        _db.session.add(prop)
        _db.session.commit()

    # Crear inmueble
    payload = {
        'direccion': 'Calle Falsa 123',
        'ciudad': 'Madrid',
        'tipo': 'Piso',
        'precio_alquiler': 800.0,
        'propietario_id': prop.id
    }

    resp = client.post('/api/inmuebles', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['direccion'] == payload['direccion']

    # Obtener lista de inmuebles
    resp = client.get('/api/inmuebles')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]['propietario']['nombre'] == 'Juan'

def test_update_inmueble(client, app):
    with app.app_context():
        from backend.models import Inmueble, Propietario
        prop = Propietario(nombre='Ana', email='ana@example.com')
        _db.session.add(prop)
        _db.session.commit()

        inmueble = Inmueble(direccion='Calle 1', ciudad='Barcelona', tipo='Casa', propietario_id=prop.id)
        _db.session.add(inmueble)
        _db.session.commit()

    update_payload = {'precio_alquiler': 1200.0, 'disponible': False}
    resp = client.put(f'/api/inmuebles/{inmueble.id}', data=json.dumps(update_payload), content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['precio_alquiler'] == 1200.0
    assert data['disponible'] is False

def test_delete_inmueble(client, app):
    with app.app_context():
        from backend.models import Inmueble, Propietario
        prop = Propietario(nombre='Luis', email='luis@example.com')
        _db.session.add(prop)
        _db.session.commit()

        inmueble = Inmueble(direccion='Calle 2', ciudad='Sevilla', tipo='Local', propietario_id=prop.id)
        _db.session.add(inmueble)
        _db.session.commit()

    resp = client.delete(f'/api/inmuebles/{inmueble.id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'Inmueble deleted successfully'

def test_get_propietarios(client, app):
    with app.app_context():
        from backend.models import Propietario
        _db.session.add(Propietario(nombre='Maria', email='maria@example.com'))
        _db.session.commit()

    resp = client.get('/api/propietarios')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1