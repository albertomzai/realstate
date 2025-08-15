from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

# Initialise the database object
db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure a new Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is not None:
        app.config.update(test_config)

    # Initialise extensions
    db.init_app(app)

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    # Serve the index page for root URL
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app