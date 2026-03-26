# models/rol.py
from models import db
from models.asociaciones import usuario_roles, roles_permisos

class Rol(db.Model):
    __tablename__ = 'roles'
    
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))
    
    # Relación muchos a muchos con Usuario
    usuarios = db.relationship('Usuario', secondary=usuario_roles, back_populates='roles')
    
    # Relación muchos a muchos con Permiso
    permisos = db.relationship('Permiso', secondary=roles_permisos, back_populates='roles')
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'