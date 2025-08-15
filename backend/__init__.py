"""Backend package initialization.

This module creates the Flask application factory and configures the database.
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

_db = None

def create_app():
    """Create and configure a new Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    global _db
    _db = SQLAlchemy(app)
    Migrate(app, _db)

    # Import models to register them with SQLAlchemy
    from . import models  # noqa: F401

    # Register API blueprint
    from .routes import api_bp  # noqa: E402
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400

    # Ensure tables are created
    with app.app_context():
        _db.create_all()

    return app