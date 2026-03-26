# scripts/fix_database.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.usuario import Usuario
from models.rol import Rol
from models.permiso import Permiso

def fix_database():
    app = create_app()
    with app.app_context():
        print("🔧 Reparando base de datos...")
        
        # 1. Crear tablas faltantes
        db.create_all()
        print("✅ Tablas creadas/verificadas")
        
        # 2. Crear roles básicos si no existen
        roles_data = [
            {'nombre': 'admin', 'descripcion': 'Administrador del sistema'},
            {'nombre': 'usuario', 'descripcion': 'Usuario básico'},
            {'nombre': 'consultor', 'descripcion': 'Solo consulta'}
        ]
        
        for rol_data in roles_data:
            rol = Rol.query.filter_by(nombre=rol_data['nombre']).first()
            if not rol:
                rol = Rol(**rol_data)
                db.session.add(rol)
                print(f"✅ Rol creado: {rol_data['nombre']}")
        
        # 3. Crear permisos básicos
        permisos_data = [
            {'nombre': 'ver_clientes', 'modulo': 'clientes'},
            {'nombre': 'crear_clientes', 'modulo': 'clientes'},
            {'nombre': 'editar_clientes', 'modulo': 'clientes'},
            {'nombre': 'ver_cobranzas', 'modulo': 'cobranzas'},
            {'nombre': 'ver_citas', 'modulo': 'citas'},
            {'nombre': 'ver_reportes', 'modulo': 'reportes'},
        ]
        
        for permiso_data in permisos_data:
            permiso = Permiso.query.filter_by(nombre=permiso_data['nombre']).first()
            if not permiso:
                permiso = Permiso(**permiso_data)
                db.session.add(permiso)
                print(f"✅ Permiso creado: {permiso_data['nombre']}")
        
        db.session.commit()
        
        # 4. Buscar o crear usuario antonio
        usuario = Usuario.query.filter_by(username='antonio').first()
        
        if not usuario:
            usuario = Usuario(
                username='antonio',
                email='antonio@mail.com',
                nombre='Antonio Gonzalez',
                activo=True
            )
            db.session.add(usuario)
            print("✅ Usuario creado")
        
        # 5. Actualizar contraseña (USANDO EL MÉTODO CORRECTO)
        usuario.set_password('User2024')  # Esto genera el hash correcto
        db.session.commit()
        print("✅ Contraseña actualizada")
        
        # 6. Asignar rol admin al usuario
        rol_admin = Rol.query.filter_by(nombre='admin').first()
        if rol_admin and rol_admin not in usuario.roles:
            usuario.roles.append(rol_admin)
            db.session.commit()
            print("✅ Rol admin asignado")
        
        # 7. Verificar
        print(f"\n📊 Usuario: {usuario.username}")
        print(f"🔑 Hash: {usuario.password_hash}")
        print(f"👥 Roles: {[r.nombre for r in usuario.roles]}")
        
        # 8. Probar verificación
        test_password = 'User2024'
        if usuario.verify_password(test_password):
            print("✅ VERIFICACIÓN EXITOSA - Contraseña correcta")
        else:
            print("❌ Error en verificación")
        
        # 9. Listar tablas para confirmar
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n📋 Tablas en BD: {tables}")

if __name__ == '__main__':
    fix_database()