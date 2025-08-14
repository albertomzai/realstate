from flask import Blueprint, request, jsonify, abort
from .models import Inmueble, Propietario
from . import db

# Blueprint para inmuebles
inmuebles_bp = Blueprint('inmuebles', __name__)

@inmuebles_bp.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles])

@inmuebles_bp.route('/inmuebles', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    propietario_id = data.get('propietario_id')
    if propietario_id and not Propietario.query.get(propietario_id):
        abort(400, description='Invalid propietario_id')

    inmueble = Inmueble(**data)
    db.session.add(inmueble)
    db.session.commit()
    return jsonify(inmueble.to_dict()), 201

@inmuebles_bp.route('/inmuebles/<int:id>', methods=['PUT'])
def update_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    data = request.get_json() or {}

    if 'propietario_id' in data:
        propietario_id = data['propietario_id']
        if not Propietario.query.get(propietario_id):
            abort(400, description='Invalid propietario_id')

    for key, value in data.items():
        if hasattr(inmueble, key) and key != 'id':
            setattr(inmueble, key, value)

    db.session.commit()
    return jsonify(inmueble.to_dict())

@inmuebles_bp.route('/inmuebles/<int:id>', methods=['DELETE'])
def delete_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    db.session.delete(inmueble)
    db.session.commit()
    return jsonify({'message': 'Inmueble deleted'}), 200

# Blueprint para propietarios
propietarios_bp = Blueprint('propietarios', __name__)

@propietarios_bp.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios])