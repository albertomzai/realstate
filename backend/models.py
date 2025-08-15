"""SQLAlchemy models for the real estate application."""

from . import db

class Propietario(db.Model):
    """Representa a un propietario de inmuebles."""

    __tablename__ = 'propietarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.String(20))

    inmuebles = db.relationship('Inmueble', backref='propietario', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono
        }

class Inmueble(db.Model):
    """Representa un inmueble disponible para alquiler."""

    __tablename__ = 'inmuebles'

    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(256), nullable=False)
    ciudad = db.Column(db.String(64), nullable=False)
    tipo = db.Column(db.String(20))
    precio_alquiler = db.Column(db.Float)
    disponible = db.Column(db.Boolean, default=True)
    propietario_id = db.Column(db.Integer, db.ForeignKey('propietarios.id'), nullable=False)

    inquilino = db.relationship('Inquilino', backref='inmueble_alquilado', uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "tipo": self.tipo,
            "precio_alquiler": self.precio_alquiler,
            "disponible": self.disponible,
            "propietario_id": self.propietario_id,
            "propietario": self.propietario.to_dict() if self.propietario else None
        }

class Inquilino(db.Model):
    """Representa un inquilino que alquila un inmueble."""

    __tablename__ = 'inquilinos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True)
    inmueble_alquilado_id = db.Column(db.Integer, db.ForeignKey('inmuebles.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "inmueble_alquilado_id": self.inmueble_alquilado_id
        }