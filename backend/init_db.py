# Script to initialise the database and create tables if they do not exist.

from backend import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print('Database tables created successfully.')