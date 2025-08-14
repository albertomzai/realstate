from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Global database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la extensión SQLAlchemy con la app
    db.init_app(app)

    # Registrar blueprints de rutas
    from .routes import inmuebles_bp, propietarios_bp
    app.register_blueprint(inmuebles_bp, url_prefix='/api')
    app.register_blueprint(propietarios_bp, url_prefix='/api')

    # Exponer la instancia db como atributo de la app
    app.db = db

    return app

__all__ = ['create_app', 'db']