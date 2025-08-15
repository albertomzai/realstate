"""Blueprint for propietario operations."""

from flask import Blueprint, jsonify
from ..models import Propietario

propietarios_bp = Blueprint('propietarios', __name__)

@propietarios_bp.route('', methods=['GET'])
def get_propietarios():
    """Return a list of all propietarios."""
    propietarios = Propietario.query.all()
    return jsonify([p.to_dict() for p in propietarios])