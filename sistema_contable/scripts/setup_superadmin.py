# scripts/setup_superadmin.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.permiso import Permiso
from models.rol import Rol

def setup():
    app = create_app()
    with app.app_context():
        # Crear permisos de superadmin
        super_perms = [
            'superadmin_ver_usuarios', 'superadmin_crear_usuarios',
            'superadmin_editar_usuarios', 'superadmin_eliminar_usuarios',
            'superadmin_ver_roles', 'superadmin_ver_permisos'
        ]
        
        for perm in super_perms:
            if not Permiso.query.filter_by(nombre=perm).first():
                p = Permiso(nombre=perm, modulo='superadmin', descripcion=f'Permiso {perm}')
                db.session.add(p)
        
        # Asignar al rol admin
        admin = Rol.query.filter_by(nombre='admin').first()
        if admin:
            todos = Permiso.query.all()
            admin.permisos = todos
            
        db.session.commit()
        print("✅ Permisos superadmin creados")

if __name__ == '__main__':
    setup()