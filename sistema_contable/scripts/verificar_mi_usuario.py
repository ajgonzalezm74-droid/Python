# scripts/verificar_mi_usuario.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.usuario import Usuario

def verificar():
    app = create_app()
    with app.app_context():
        # Cambia 'admin' por tu nombre de usuario
        usuario = Usuario.query.filter_by(username='admin').first()
        
        if not usuario:
            usuario = Usuario.query.first()  # Toma el primer usuario
        
        if usuario:
            print(f"\n👤 Usuario: {usuario.username}")
            print(f"📧 Email: {usuario.email}")
            print(f"🔑 ID: {usuario.id}")
            print(f"\n📋 Roles:")
            for rol in usuario.roles:
                print(f"  - {rol.nombre}")
                print(f"    Permisos: {[p.nombre for p in rol.permisos]}")
            
            print(f"\n🔐 Permisos totales en sesión: {usuario.get_permisos()}")
            
            # Verificar permisos específicos
            permisos_necesarios = [
                'superadmin_crear_usuarios',
                'admin_total',
                'crear_usuarios'
            ]
            
            print(f"\n🎯 Verificando permisos para 'Crear Usuario':")
            for permiso in permisos_necesarios:
                if usuario.tiene_permiso(permiso):
                    print(f"  ✅ TIENE: {permiso}")
                else:
                    print(f"  ❌ NO TIENE: {permiso}")

if __name__ == '__main__':
    verificar()