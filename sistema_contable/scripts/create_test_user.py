# scripts/create_test_user.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from app import create_app
from models import db
from sistema_contable.models.usuario import Usuario
from sistema_contable.models.permiso import Rol, Permiso

def create_test_user():
    app = create_app()
    with app.app_context():
        # Crear usuario de prueba
        test_user = Usuario.query.filter_by(username='antonio').first()
        
        if not test_user:
            test_user = Usuario(
                username='antonio',
                email='antonio@mail.com',
                nombre='Antonio Gonzalez',
                activo=True
            )
            test_user.set_password('User2024')
            db.session.add(test_user)
            db.session.commit()
            print("✅ Usuario de prueba creado")
        else:
            print("✅ Usuario ya existe")
            # Actualizar contraseña
            test_user.set_password('User2024')
            db.session.commit()
            print("✅ Contraseña actualizada")

if __name__ == '__main__':
    create_test_user()