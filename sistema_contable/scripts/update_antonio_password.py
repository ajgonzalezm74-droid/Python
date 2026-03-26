# scripts/update_antonio_password.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.usuario import Usuario

def update_password():
    app = create_app()
    with app.app_context():
        usuario = Usuario.query.filter_by(username='antonio').first()
        
        if usuario:
            print(f"✅ Usuario encontrado: {usuario.username}")
            print(f"📧 Email: {usuario.email}")
            print(f"🔑 Hash actual: {usuario.password_hash}")
            
            # Actualizar contraseña
            usuario.set_password('User2024')
            db.session.commit()
            
            print(f"✅ Nueva contraseña: User2024")
            print(f"🔐 Nuevo hash: {usuario.password_hash}")
            
            # Verificar
            if usuario.verify_password('User2024'):
                print("✅ Verificación exitosa")
            else:
                print("❌ Error en verificación")
        else:
            print("❌ Usuario 'antonio' no encontrado")
            
            # Crear usuario si no existe
            nuevo_usuario = Usuario(
                username='antonio',
                email='antonio@mail.com',
                nombre='Antonio Gonzalez',
                activo=True
            )
            nuevo_usuario.set_password('User2024')
            db.session.add(nuevo_usuario)
            db.session.commit()
            print("✅ Usuario creado correctamente")

if __name__ == '__main__':
    update_password()