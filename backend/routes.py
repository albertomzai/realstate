"""API routes for the real estate backend."""

from flask import Blueprint, request, jsonify
from .models import Inmueble, Propietario, _db as db

api_bp = Blueprint('api', __name__)

# Helper functions

def get_inmueble_or_404(inmueble_id):
    inmueble = Inmueble.query.get(inmueble_id)
    if not inmueble:
        return None, jsonify({'error': 'Inmueble no encontrado'}), 404
    return inmueble, None, None

# Routes for inmuebles

@api_bp.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    """Return a list of all inmuebles with owner data."""
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles]), 200

@api_bp.route('/inmuebles', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos requeridos faltantes'}), 400

    inmueble = Inmueble(**data)
    db.session.add(inmueble)
    db.session.commit()
    return jsonify(inmueble.to_dict()), 201

@api_bp.route('/inmuebles/<int:inmueble_id>', methods=['PUT'])
def update_inmueble(inmueble_id):
    inmueble, err_resp, status = get_inmueble_or_404(inmueble_id)
    if err_resp:
        return err_resp, status

    data = request.get_json() or {}
    for key in ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'disponible', 'propietario_id']:
        if key in data:
            setattr(inmueble, key, data[key])

    db.session.commit()
    return jsonify(inmueble.to_dict()), 200

@api_bp.route('/inmuebles/<int:inmueble_id>', methods=['DELETE'])
def delete_inmueble(inmueble_id):
    inmueble, err_resp, status = get_inmueble_or_404(inmueble_id)
    if err_resp:
        return err_resp, status

    db.session.delete(inmueble)
    db.session.commit()
    return jsonify({'message': 'Inmueble eliminado'}), 200

# Routes for propietarios

@api_bp.route('/propietarios', methods=['GET'])
def get_propietarios():
    """Return a list of all propietarios."""
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios]), 200