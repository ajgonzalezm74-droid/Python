# models.py
from datetime import datetime
from extensions import db   
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class HistorialTasa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))  # Campo opcional para teléfono
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    email_verificado = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

#  Actualizar CalculoUsuario
class CalculoUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre_item = db.Column(db.String(100), nullable=False)
    precio_bs = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tasa_usd = db.Column(db.Float, nullable=True)
    tasa_tipo = db.Column(db.String(20), nullable=True)
    
    user = db.relationship('User', backref='calculos')