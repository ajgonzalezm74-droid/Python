# models/menu.py
from models import db
from datetime import datetime

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    icono = db.Column(db.String(50), default='fas fa-circle')  # Icono de FontAwesome
    url = db.Column(db.String(200))  # URL o endpoint name
    orden = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación jerárquica
    padre_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    hijos = db.relationship('Menu', backref=db.backref('padre', remote_side=[id]), lazy='dynamic')
    
    # Relación con roles
    roles = db.relationship('Rol', secondary='menu_roles', backref='menus')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Menu {self.nombre}>'

class MenuRoles(db.Model):
    __tablename__ = 'menu_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)