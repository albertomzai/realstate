from flask_sqlalchemy import SQLAlchemy

_db = SQLAlchemy()

class Inmueble(_db.Model):
    __tablename__ = 'inmuebles'

    id = _db.Column(_db.Integer, primary_key=True)
    direccion = _db.Column(_db.String, nullable=False)
    ciudad = _db.Column(_db.String, nullable=False)
    tipo = _db.Column(_db.String),  # 'Piso', 'Casa', 'Local'
    precio_alquiler = _db.Column(_db.Float)
    disponible = _db.Column(_db.Boolean, default=True)
    propietario_id = _db.Column(_db.Integer, _db.ForeignKey('propietarios.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'tipo': self.tipo,
            'precio_alquiler': self.precio_alquiler,
            'disponible': self.disponible,
            'propietario_id': self.propietario_id,
            'propietario_nombre': self.propietario.nombre if self.propietario else None
        }