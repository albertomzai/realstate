"""Backend package initialization.

This module creates the Flask application factory, configures SQLAlchemy,
registers blueprints and serves static files from the frontend directory.
"""

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Initialise the database object. It will be bound to the app in create_app.
db = SQLAlchemy()

def create_app():
    """Create and configure a Flask application instance.

    Returns:
        flask.Flask: The configured Flask application.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Basic configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise extensions
    db.init_app(app)

    # Register blueprints
    from .routes.inmuebles import inmuebles_bp
    from .routes.propietarios import propietarios_bp

    app.register_blueprint(inmuebles_bp, url_prefix='/api/inmuebles')
    app.register_blueprint(propietarios_bp, url_prefix='/api/propietarios')

    # Serve the root page
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": str(error)}, 400

    return app