from . import create_app

# Se importa la instancia de db desde el factory
_app = create_app()
db = _app.db

class Propietario(db.Model):
    __tablename__ = 'propietarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    telefono = db.Column(db.String)

    inmuebles = db.relationship('Inmueble', backref='propietario', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono
        }

class Inmueble(db.Model):
    __tablename__ = 'inmuebles'

    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String, nullable=False)
    ciudad = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    precio_alquiler = db.Column(db.Float)
    disponible = db.Column(db.Boolean, default=True)
    propietario_id = db.Column(db.Integer, db.ForeignKey('propietarios.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'tipo': self.tipo,
            'precio_alquiler': self.precio_alquiler,
            'disponible': self.disponible,
            'propietario_id': self.propietario_id,
            'propietario': self.propietario.to_dict() if self.propietario else None
        }

class Inquilino(db.Model):
    __tablename__ = 'inquilinos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    inmueble_alquilado_id = db.Column(db.Integer, db.ForeignKey('inmuebles.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'inmueble_alquilado_id': self.inmueble_alquilado_id
        }