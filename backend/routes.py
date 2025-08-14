from flask import Blueprint, request, jsonify, abort
from .models import Propietario, Inmueble, Inquilino

# Blueprint para inmuebles
inmuebles_bp = Blueprint('inmuebles', __name__)

@inmuebles_bp.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles]), 200

@inmuebles_bp.route('/inmuebles', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo', 'propietario_id']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    inmueble = Inmueble(**data)
    try:
        Inmueble.query.session.add(inmueble)
        Inmueble.query.session.commit()
    except Exception as e:
        Inmueble.query.session.rollback()
        abort(400, description=str(e))

    return jsonify(inmueble.to_dict()), 201

@inmuebles_bp.route('/inmuebles/<int:inmueble_id>', methods=['PUT'])
def update_inmueble(inmueble_id):
    inmueble = Inmueble.query.get_or_404(inmueble_id)
    data = request.get_json() or {}

    for field in ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'disponible', 'propietario_id']:
        if field in data:
            setattr(inmueble, field, data[field])

    try:
        Inmueble.query.session.commit()
    except Exception as e:
        Inmueble.query.session.rollback()
        abort(400, description=str(e))

    return jsonify(inmueble.to_dict()), 200

@inmuebles_bp.route('/inmuebles/<int:inmueble_id>', methods=['DELETE'])
def delete_inmueble(inmueble_id):
    inmueble = Inmueble.query.get_or_404(inmueble_id)
    try:
        Inmueble.query.session.delete(inmueble)
        Inmueble.query.session.commit()
    except Exception as e:
        Inmueble.query.session.rollback()
        abort(400, description=str(e))

    return jsonify({'message': 'Inmueble deleted successfully'}), 200

# Blueprint para propietarios
propietarios_bp = Blueprint('propietarios', __name__)

@propietarios_bp.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios]), 200

# Manejo de errores comunes
@inmuebles_bp.errorhandler(404)
@propietarios_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@inmuebles_bp.errorhandler(400)
@propietarios_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400