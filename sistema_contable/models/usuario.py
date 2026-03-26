# models/usuario.py
from models import db
from models.asociaciones import usuario_roles
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=True)
    
    roles = db.relationship('Rol', secondary=usuario_roles, 
                           back_populates='usuarios',
                           primaryjoin="Usuario.id == usuario_roles.c.usuario_id",
                           secondaryjoin="Rol.id_rol == usuario_roles.c.rol_id")
    
    # Método para establecer contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Método para verificar contraseña
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Métodos para verificar permisos
    def tiene_permiso(self, permiso_nombre):
        """Verifica si el usuario tiene un permiso específico"""
        for rol in self.roles:
            for permiso in rol.permisos:
                if permiso.nombre == permiso_nombre:
                    return True
        return False
    
    # Método para obtener todos los permisos del usuario
    def get_permisos(self):
        """Retorna lista de todos los permisos del usuario"""
        permisos = set()
        for rol in self.roles:
            for permiso in rol.permisos:
                permisos.add(permiso.nombre)
        return list(permisos)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'