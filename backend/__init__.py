from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializamos la extensión de base de datos
db = SQLAlchemy()

def create_app():
    """Factory que crea y configura la aplicación Flask."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializamos las extensiones
    db.init_app(app)

    # Registramos los blueprints de la API
    from .routes import inmuebles_bp, propietarios_bp
    app.register_blueprint(inmuebles_bp, url_prefix='/api')
    app.register_blueprint(propietarios_bp, url_prefix='/api')

    # Ruta raíz que sirve el index.html del frontend
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    # Manejo de errores genéricos
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad Request'}, 400

    return app