# scripts/crear_permisos_crud.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.permiso import Permiso

def crear_permisos_crud():
    app = create_app()
    with app.app_context():
        print("🔧 Creando permisos CRUD por módulo...")
        
        modulos = ['clientes', 'cobranzas', 'pagos', 'citas', 'reportes']
        acciones = ['ver', 'crear', 'editar', 'eliminar']
        
        creados = 0
        for modulo in modulos:
            for accion in acciones:
                # Para reportes, no tiene eliminar
                if modulo == 'reportes' and accion == 'eliminar':
                    continue
                    
                nombre = f"{accion}_{modulo}"
                descripcion = f"{accion.capitalize()} {modulo}"
                
                permiso = Permiso.query.filter_by(nombre=nombre).first()
                if not permiso:
                    permiso = Permiso(nombre=nombre, modulo=modulo, descripcion=descripcion)
                    db.session.add(permiso)
                    creados += 1
                    print(f"  ✅ Creado: {nombre}")
        
        db.session.commit()
        print(f"\n📊 {creados} permisos CRUD creados")

if __name__ == '__main__':
    crear_permisos_crud()