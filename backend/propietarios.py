from flask import Blueprint, jsonify
from . import db, Propietario

propietarios_bp = Blueprint('propietarios', __name__)

@propietarios_bp.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    result = []
    for p in propietarios:
        result.append({
            'id': p.id,
            'nombre': p.nombre,
            'email': p.email,
            'telefono': p.telefono
        })
    return jsonify(result), 200