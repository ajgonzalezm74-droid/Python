# scripts/crear_roles_predefinidos.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.rol import Rol
from models.permiso import Permiso

def crear_roles_predefinidos():
    app = create_app()
    with app.app_context():
        print("🔧 Creando roles predefinidos...")
        
        # Obtener todos los permisos
        todos_permisos = {p.nombre: p for p in Permiso.query.all()}
        
        # Definición de roles con sus permisos
        roles_config = [
            {
                'nombre': 'consultant',
                'descripcion': 'Consultor - Acceso de lectura a todos los módulos',
                'permisos': ['view_clientes', 'read_clientes', 'view_cobranzas', 'read_cobranzas',
                            'view_pagos', 'read_pagos', 'view_citas', 'read_citas', 
                            'view_reportes', 'read_reportes']
            },
            {
                'nombre': 'administrador',
                'descripcion': 'Administrador - Acceso completo a clientes, citas, pagos',
                'permisos': ['view_clientes', 'read_clientes', 'write_clientes', 'delete_clientes',
                            'view_citas', 'read_citas', 'write_citas', 'delete_citas',
                            'view_pagos', 'read_pagos', 'write_pagos']
            },
            {
                'nombre': 'cobrador',
                'descripcion': 'Cobrador - Gestión de cobranzas',
                'permisos': ['view_cobranzas', 'read_cobranzas', 'write_cobranzas',
                            'view_clientes', 'read_clientes']
            },
            {
                'nombre': 'cajero',
                'descripcion': 'Cajero - Gestión de pagos',
                'permisos': ['view_pagos', 'read_pagos', 'write_pagos',
                            'view_clientes', 'read_clientes']
            }
        ]
        
        for config in roles_config:
            rol = Rol.query.filter_by(nombre=config['nombre']).first()
            if not rol:
                rol = Rol(nombre=config['nombre'], descripcion=config['descripcion'])
                db.session.add(rol)
                print(f"✅ Rol '{config['nombre']}' creado")
            
            # Asignar permisos
            rol.permisos = []
            for permiso_nombre in config['permisos']:
                if permiso_nombre in todos_permisos:
                    rol.permisos.append(todos_permisos[permiso_nombre])
            
            print(f"   Asignados {len(rol.permisos)} permisos")
        
        db.session.commit()
        print("\n🎉 Roles predefinidos creados")

if __name__ == '__main__':
    crear_roles_predefinidos()