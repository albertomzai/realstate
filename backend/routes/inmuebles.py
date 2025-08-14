from flask import Blueprint, request, jsonify, abort
from ..models.propietario import Propietario
from ..models.inmueble import Inmueble
from .. import _db

inmuebles_bp = Blueprint('inmuebles', __name__)

@inmuebles_bp.route('/', methods=['GET'])
def get_inmuebles():
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles]), 200

@inmuebles_bp.route('/', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'propietario_id']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    propietario = Propietario.query.get(data['propietario_id'])
    if not propietario:
        abort(400, description='Propietario no encontrado')

    inmueble = Inmueble(**data)
    _db.session.add(inmueble)
    _db.session.commit()
    return jsonify(inmueble.to_dict()), 201

@inmuebles_bp.route('/<int:id>', methods=['PUT'])
def update_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    data = request.get_json() or {}

    if 'propietario_id' in data:
        propietario = Propietario.query.get(data['propietario_id'])
        if not propietario:
            abort(400, description='Propietario no encontrado')
        inmueble.propietario_id = data['propietario_id']

    for field in ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'disponible']:
        if field in data:
            setattr(inmueble, field, data[field])

    _db.session.commit()
    return jsonify(inmueble.to_dict()), 200

@inmuebles_bp.route('/<int:id>', methods=['DELETE'])
def delete_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    _db.session.delete(inmueble)
    _db.session.commit()
    return jsonify({'message': 'Inmueble eliminado'}), 200