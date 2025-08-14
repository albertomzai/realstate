from flask_sqlalchemy import SQLAlchemy

_db = SQLAlchemy()

class Inquilino(_db.Model):
    __tablename__ = 'inquilinos'

    id = _db.Column(_db.Integer, primary_key=True)
    nombre = _db.Column(_db.String, nullable=False)
    email = _db.Column(_db.String, unique=True)
    inmueble_alquilado_id = _db.Column(_db.Integer, _db.ForeignKey('inmuebles.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'inmueble_alquilado_id': self.inmueble_alquilado_id
        }