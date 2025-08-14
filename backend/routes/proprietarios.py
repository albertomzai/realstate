from flask import Blueprint, jsonify
from ..models.propietario import Propietario

proprietarios_bp = Blueprint('proprietarios', __name__)

@proprietarios_bp.route('/', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios]), 200