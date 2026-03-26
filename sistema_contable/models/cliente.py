# models/cliente.py
from models import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    id_documento = db.Column(db.Integer, unique=True)
    tipo_documento = db.Column(db.String(5), default='V')
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))
    rif = db.Column(db.String(20))
    nombre_compania = db.Column(db.String(150))
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    notas = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    telefono_alternativo = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    pais = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    
    # Relación con usuario que creó el cliente
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=False)
    usuario = db.relationship('Usuario', backref='clientes')
    
    # Fechas
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Propiedad para nombre completo
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"
    
    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellidos}>'