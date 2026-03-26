# scripts/update_password.py
from app import create_app
from models import db
from sistema_contable.models.usuario import Usuario

def update_passwords():
    app = create_app()
    with app.app_context():
        usuario = Usuario.query.filter_by(username='antonio').first()
        if usuario:
            print(f"Usuario encontrado: {usuario.username}")
            print(f"Hash actual: {usuario.password_hash}")
            
            # Actualizar a hash real
            usuario.set_password('User2024')  # Cambia esto por la contraseña real
            db.session.commit()
            
            print(f"Nuevo hash: {usuario.password_hash}")
            print("✅ Contraseña actualizada")
        else:
            print("❌ Usuario no encontrado")

if __name__ == '__main__':
    update_passwords()