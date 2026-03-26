# scripts/create_admin_permissions.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.permiso import Permiso
from models.rol import Rol

def create_admin_permissions():
    app = create_app()
    with app.app_context():
        # Crear permisos de administración
        admin_permissions = [
            {'nombre': 'admin_usuarios', 'modulo': 'admin', 'descripcion': 'Gestionar usuarios del sistema'},
            {'nombre': 'crear_usuarios', 'modulo': 'admin', 'descripcion': 'Crear nuevos usuarios'},
            {'nombre': 'editar_usuarios', 'modulo': 'admin', 'descripcion': 'Editar usuarios existentes'},
            {'nombre': 'eliminar_usuarios', 'modulo': 'admin', 'descripcion': 'Eliminar usuarios'},
            {'nombre': 'cambiar_password', 'modulo': 'admin', 'descripcion': 'Cambiar contraseñas de usuarios'},
            {'nombre': 'admin_roles', 'modulo': 'admin', 'descripcion': 'Gestionar roles y permisos'},
        ]
        
        for perm_data in admin_permissions:
            permiso = Permiso.query.filter_by(nombre=perm_data['nombre']).first()
            if not permiso:
                permiso = Permiso(**perm_data)
                db.session.add(permiso)
                print(f"✅ Permiso creado: {perm_data['nombre']}")
        
        # Asignar permisos al rol admin
        admin_rol = Rol.query.filter_by(nombre='admin').first()
        if admin_rol:
            todos_permisos = Permiso.query.all()
            admin_rol.permisos = todos_permisos
            print("✅ Permisos asignados al rol admin")
        
        db.session.commit()
        print("🎉 Configuración de permisos completada")

if __name__ == '__main__':
    create_admin_permissions()