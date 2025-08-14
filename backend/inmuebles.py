from flask import Blueprint, jsonify, request, current_app
from . import db, Propietario, Inmueble

inmuebles_bp = Blueprint('inmuebles', __name__)

@inmuebles_bp.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    inmuebles = Inmueble.query.all()
    result = []
    for inmueble in inmuebles:
        propietario = Propietario.query.get(inmueble.propietario_id)
        result.append({
            'id': inmueble.id,
            'direccion': inmueble.direccion,
            'ciudad': inmueble.ciudad,
            'tipo': inmueble.tipo,
            'precio_alquiler': inmueble.precio_alquiler,
            'disponible': inmueble.disponible,
            'propietario': {
                'id': propietario.id if propietario else None,
                'nombre': propietario.nombre if propietario else None
            }
        })
    return jsonify(result), 200

@inmuebles_bp.route('/inmuebles', methods=['POST'])
def create_inmueble():
    data = request.get_json() or {}
    required_fields = ['direccion', 'ciudad', 'tipo']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    inmueble = Inmueble(
        direccion=data['direccion'],
        ciudad=data['ciudad'],
        tipo=data['tipo'],
        precio_alquiler=data.get('precio_alquiler'),
        disponible=data.get('disponible', True),
        propietario_id=data.get('propietario_id')
    )
    db.session.add(inmueble)
    db.session.commit()

    return jsonify({'id': inmueble.id}), 201

@inmuebles_bp.route('/inmuebles/<int:id>', methods=['PUT'])
def update_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    data = request.get_json() or {}

    for field in ['direccion', 'ciudad', 'tipo', 'precio_alquiler', 'disponible', 'propietario_id']:
        if field in data:
            setattr(inmueble, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Inmueble updated'}), 200

@inmuebles_bp.route('/inmuebles/<int:id>', methods=['DELETE'])
def delete_inmueble(id):
    inmueble = Inmueble.query.get_or_404(id)
    db.session.delete(inmueble)
    db.session.commit()
    return jsonify({'message': 'Inmueble deleted'}), 200