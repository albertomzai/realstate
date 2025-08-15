"""Blueprint for inmueble CRUD operations."""

from flask import Blueprint, request, jsonify, abort
from .. import db
from ..models import Inmueble, Propietario

inmuebles_bp = Blueprint('inmuebles', __name__)

@inmuebles_bp.route('', methods=['GET'])
def get_inmuebles():
    """Return a list of all inmuebles with embedded propietario."""
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles])

@inmuebles_bp.route('', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'propietario_id']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    propietario = Propietario.query.get(data['propietario_id'])
    if not propietario:
        abort(404, description='Propietario not found')

    inmueble = Inmueble(**data)
    db.session.add(inmueble)
    db.session.commit()
    return jsonify(inmueble.to_dict()), 201

@inmuebles_bp.route('/<int:id>', methods=['PUT'])
def update_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    data = request.get_json() or {}
    for key, value in data.items():
        if hasattr(inmueble, key) and key != 'id':
            setattr(inmueble, key, value)

    db.session.commit()
    return jsonify(inmueble.to_dict())

@inmuebles_bp.route('/<int:id>', methods=['DELETE'])
def delete_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    db.session.delete(inmueble)
    db.session.commit()
    return jsonify({"message": "Inmueble deleted"})