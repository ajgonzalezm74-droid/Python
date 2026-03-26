# scripts/asignar_todos_permisos.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.usuario import Usuario
from models.rol import Rol
from models.permiso import Permiso

def asignar():
    app = create_app()
    with app.app_context():
        # Tomar el primer usuario (cambia si es necesario)
        usuario = Usuario.query.first()
        
        if usuario:
            print(f"👤 Usuario: {usuario.username}")
            
            # Buscar o crear rol superadmin
            rol = Rol.query.filter_by(nombre='superadmin').first()
            if not rol:
                rol = Rol(nombre='superadmin', descripcion='Super Admin - Todos los permisos')
                db.session.add(rol)
                print("✅ Rol superadmin creado")
            
            # Asignar todos los permisos al rol
            todos_permisos = Permiso.query.all()
            rol.permisos = todos_permisos
            print(f"✅ Asignados {len(todos_permisos)} permisos al rol")
            
            # Asignar rol al usuario
            if rol not in usuario.roles:
                usuario.roles.append(rol)
                db.session.commit()
                print(f"✅ Rol superadmin asignado a {usuario.username}")
            else:
                print("ℹ️ El usuario ya tiene el rol superadmin")
            
            # Mostrar resultado
            print(f"\n🔐 Permisos actuales: {len(usuario.get_permisos())}")
        else:
            print("❌ No hay usuarios")

if __name__ == '__main__':
    asignar()