from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cita(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)

    servicio = db.Column(db.String(100))
    descripcion = db.Column(db.Text)

    estado = db.Column(db.String(20))