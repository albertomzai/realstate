from flask_sqlalchemy import SQLAlchemy

_db = SQLAlchemy()

class Propietario(_db.Model):
    __tablename__ = 'propietarios'

    id = _db.Column(_db.Integer, primary_key=True)
    nombre = _db.Column(_db.String, nullable=False)
    email = _db.Column(_db.String, unique=True)
    telefono = _db.Column(_db.String)

    inmuebles = _db.relationship('Inmueble', backref='propietario', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono
        }