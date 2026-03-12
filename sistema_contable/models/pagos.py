from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Pago(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    proveedor = db.Column(db.String(150))

    fecha = db.Column(db.Date)

    concepto = db.Column(db.String(200))

    monto = db.Column(db.Float)

    tipo_gasto = db.Column(db.String(100))