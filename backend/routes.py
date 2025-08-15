from flask import Blueprint, request, jsonify, abort
from .models import Inmueble, Propietario
from . import db

api_bp = Blueprint('api', __name__)

# --- Inmuebles endpoints ---

@api_bp.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles])

@api_bp.route('/inmuebles', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    inmueble = Inmueble(**{
        'direccion': data['direccion'],
        'ciudad': data['ciudad'],
        'tipo': data['tipo'],
        'precio_alquiler': data.get('precio_alquiler'),
        'disponible': data.get('disponible', True),
        'propietario_id': data.get('propietario_id')
    })

    db.session.add(inmueble)
    db.session.commit()

    return jsonify(inmueble.to_dict()), 201

@api_bp.route('/inmuebles/<int:id>', methods=['PUT'])
def update_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    data = request.get_json() or {}

    for field in ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'disponible', 'propietario_id']:
        if field in data:
            setattr(inmueble, field, data[field])

    db.session.commit()
    return jsonify(inmueble.to_dict())

@api_bp.route('/inmuebles/<int:id>', methods=['DELETE'])
def delete_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    db.session.delete(inmueble)
    db.session.commit()
    return jsonify({'message': 'Inmueble deleted successfully'})

# --- Propietarios endpoints ---

@api_bp.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios])