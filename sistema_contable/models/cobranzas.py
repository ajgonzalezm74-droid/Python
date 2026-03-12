from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cobranza(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    fecha = db.Column(db.Date)

    concepto = db.Column(db.String(200))

    monto = db.Column(db.Float)

    metodo_pago = db.Column(db.String(50))