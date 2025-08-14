from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

_db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    _db.init_app(app)

    # Registrar blueprints
    from .routes.inmuebles import inmuebles_bp
    from .routes.proprietarios import proprietarios_bp

    app.register_blueprint(inmuebles_bp, url_prefix='/api/inmuebles')
    app.register_blueprint(proprietarios_bp, url_prefix='/api/propietarios')

    # Rutas raíz para servir el frontend
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Manejo de errores globales
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error'}), 500

    return app