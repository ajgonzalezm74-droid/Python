from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(150))
    rif = db.Column(db.String(20))

    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))

    direccion = db.Column(db.String(200))

    fecha_registro = db.Column(db.DateTime)