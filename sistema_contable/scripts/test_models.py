# scripts/test_models.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.usuario import Usuario
from models.rol import Rol
from models.permiso import Permiso

def test_models():
    app = create_app()
    with app.app_context():
        print("🔍 Probando modelos...")
        
        # Probar consulta a roles
        roles = Rol.query.all()
        print(f"✅ Roles encontrados: {len(roles)}")
        for rol in roles:
            print(f"  - {rol.nombre} (id_rol: {rol.id_rol})")
        
        # Probar consulta a permisos
        permisos = Permiso.query.all()
        print(f"✅ Permisos encontrados: {len(permisos)}")
        
        # Probar consulta a usuarios
        usuarios = Usuario.query.all()
        print(f"✅ Usuarios encontrados: {len(usuarios)}")
        for usuario in usuarios:
            print(f"  - {usuario.username} (id: {usuario.id})")
            print(f"    Roles: {[r.nombre for r in usuario.roles]}")
        
        # Probar verificación de contraseña
        if usuarios:
            usuario = usuarios[0]
            test_pass = 'User2024'
            if usuario.verify_password(test_pass):
                print(f"✅ Contraseña correcta para {usuario.username}")
                print(f"🔐 Permisos: {usuario.get_permisos()}")
            else:
                print(f"❌ Contraseña incorrecta para {usuario.username}")

if __name__ == '__main__':
    test_models()