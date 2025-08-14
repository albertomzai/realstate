from flask import Blueprint, request, jsonify

from .models import db, Inmueble, Propietario

# Blueprint para inmuebles
inmuebles_bp = Blueprint('inmuebles', __name__)

@inmuebles_bp.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    inmuebles = Inmueble.query.all()
    return jsonify([i.to_dict() for i in inmuebles])

@inmuebles_bp.route('/inmuebles', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo', 'propietario_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    inmueble = Inmueble(**data)
    db.session.add(inmueble)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(inmueble.to_dict()), 201

@inmuebles_bp.route('/inmuebles/<int:id>', methods=['PUT'])
def update_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    data = request.get_json() or {}
    for field in ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'disponible', 'propietario_id']:
        if field in data:
            setattr(inmueble, field, data[field])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(inmueble.to_dict())

@inmuebles_bp.route('/inmuebles/<int:id>', methods=['DELETE'])
def delete_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    db.session.delete(inmueble)
    db.session.commit()
    return jsonify({'message': 'Inmueble deleted successfully'})

# Blueprint para propietarios
propietarios_bp = Blueprint('propietarios', __name__)

@propietarios_bp.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios])