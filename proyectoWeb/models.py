from datetime import datetime
from extensions import db   

class HistorialTasa(db.Model):
    #__tablename__ = "historial_tasas"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    