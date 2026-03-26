# models/permiso.py
from models import db
from models.asociaciones import roles_permisos

class Permiso(db.Model):
    __tablename__ = 'permisos'
    
    id_permiso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    modulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(200))
    
    # Relación muchos a muchos con Rol
    roles = db.relationship('Rol', secondary=roles_permisos, back_populates='permisos')
    
    def __repr__(self):
        return f'<Permiso {self.nombre}>'