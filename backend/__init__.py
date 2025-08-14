from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models
class Propietario(db.Model):
    __tablename__ = 'propietarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    telefono = db.Column(db.String(32))

    inmuebles = db.relationship('Inmueble', backref='propietario', lazy=True)

class Inmueble(db.Model):
    __tablename__ = 'inmuebles'
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(256), nullable=False)
    ciudad = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.Enum('Piso', 'Casa', 'Local'), nullable=False)
    precio_alquiler = db.Column(db.Float)
    disponible = db.Column(db.Boolean, default=True)
    propietario_id = db.Column(db.Integer, db.ForeignKey('propietarios.id'))

class Inquilino(db.Model):
    __tablename__ = 'inquilinos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    inmueble_alquilado_id = db.Column(db.Integer, db.ForeignKey('inmuebles.id'))

# Blueprints import
from .inmuebles import inmuebles_bp
from .propietarios import propietarios_bp

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inmobiliaria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(inmuebles_bp, url_prefix='/api')
    app.register_blueprint(propietarios_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app