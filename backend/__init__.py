from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

_db = None

def create_app(test_config=None):
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    global _db
    _db = SQLAlchemy(app)

    # Importar y registrar blueprints
    from . import routes as routes_module
    app.register_blueprint(routes_module.inmuebles_bp, url_prefix='/api')
    app.register_blueprint(routes_module.propietarios_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Manejo de errores 404 y 400
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    # Exponer la instancia de db para los modelos y tests
    app.db = _db

    return app