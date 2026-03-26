# scripts/verificar_sesion.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.usuario import Usuario

def verificar_sesion():
    app = create_app()
    with app.app_context():
        # Buscar usuario admin
        usuario = Usuario.query.filter_by(username='admin').first()
        
        if usuario:
            print(f"\n👤 Usuario en BD: {usuario.username}")
            print(f"🔐 Permisos en BD: {usuario.get_permisos()}")
            
            print(f"\n📋 Permisos que deberías tener en sesión:")
            permisos_importantes = [
                'superadmin_crear_usuarios',
                'crear_usuarios',
                'admin_usuarios'
            ]
            for p in permisos_importantes:
                if p in usuario.get_permisos():
                    print(f"  ✅ {p}")
                else:
                    print(f"  ❌ {p}")
        else:
            print("❌ Usuario 'admin' no encontrado")

if __name__ == '__main__':
    verificar_sesion()