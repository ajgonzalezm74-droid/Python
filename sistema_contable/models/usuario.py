from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100))
    usuario = db.Column(db.String(50), unique=True)

    email = db.Column(db.String(120))
    password = db.Column(db.String(200))

    rol = db.Column(db.String(20))
    estado = db.Column(db.Boolean, default=True)