# scripts/crear_permisos_matriz.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.permiso import Permiso

def crear_permisos_matriz():
    app = create_app()
    with app.app_context():
        print("🔧 Creando permisos con estructura de matriz...")
        
        # Módulos del sistema
        modulos = ['clientes', 'cobranzas', 'pagos', 'citas', 'reportes', 'usuarios']
        
        # Acciones por módulo
        acciones = [
            {'nombre': 'view', 'descripcion': 'Ver listado y detalles'},
            {'nombre': 'read', 'descripcion': 'Leer información detallada'},
            {'nombre': 'write', 'descripcion': 'Crear y editar registros'},
            {'nombre': 'delete', 'descripcion': 'Eliminar registros'}
        ]
        
        permisos_creados = []
        
        for modulo in modulos:
            for accion in acciones:
                nombre_permiso = f"{accion['nombre']}_{modulo}"
                descripcion = f"{accion['descripcion']} de {modulo}"
                
                permiso = Permiso.query.filter_by(nombre=nombre_permiso).first()
                if not permiso:
                    permiso = Permiso(
                        nombre=nombre_permiso,
                        modulo=modulo,
                        descripcion=descripcion
                    )
                    db.session.add(permiso)
                    permisos_creados.append(nombre_permiso)
                    print(f"  ✅ Creado: {nombre_permiso}")
                else:
                    print(f"  ⏩ Ya existe: {nombre_permiso}")
        
        db.session.commit()
        print(f"\n📊 {len(permisos_creados)} permisos creados")
        print("\n📋 Estructura de permisos:")
        print("   Módulos: clientes, cobranzas, pagos, citas, reportes, usuarios")
        print("   Acciones: view, read, write, delete")

if __name__ == '__main__':
    crear_permisos_matriz()