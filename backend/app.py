from . import create_app, _db

__name__ = '__main__'

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        _db.create_all()  # Crea las tablas si no existen
    app.run(host='0.0.0.0', port=5000, debug=True)