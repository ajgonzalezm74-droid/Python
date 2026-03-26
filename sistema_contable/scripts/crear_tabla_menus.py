# scripts/crear_tabla_menus.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.menu import Menu

def crear_tabla_menus():
    app = create_app()
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        print("✅ Tablas de menús creadas")
        
        # Verificar si ya hay menús
        if Menu.query.count() > 0:
            print("ℹ️ Ya existen menús configurados")
            return
        
        # Menús predefinidos
        menus = [
            # Nivel 1: Dashboard
            {'nombre': 'Dashboard', 'icono': 'fas fa-home', 'url': 'dashboard.dashboard', 'orden': 1},
            
            # Nivel 1: Gestión
            {'nombre': 'Gestión', 'icono': 'fas fa-chart-line', 'url': None, 'orden': 2},
            #   Nivel 2: Clientes
            {'nombre': 'Clientes', 'icono': 'fas fa-users', 'url': 'clientes.listar', 'orden': 1, 'padre': 'Gestión'},
            #   Nivel 2: Cobranzas
            {'nombre': 'Cobranzas', 'icono': 'fas fa-hand-holding-usd', 'url': 'cobranzas.listar', 'orden': 2, 'padre': 'Gestión'},
            #   Nivel 2: Pagos
            {'nombre': 'Pagos', 'icono': 'fas fa-credit-card', 'url': 'pagos.listar', 'orden': 3, 'padre': 'Gestión'},
            #   Nivel 2: Citas
            {'nombre': 'Citas', 'icono': 'fas fa-calendar-alt', 'url': 'citas.listar', 'orden': 4, 'padre': 'Gestión'},
            #   Nivel 2: Reportes
            {'nombre': 'Reportes', 'icono': 'fas fa-chart-bar', 'url': 'reportes.dashboard', 'orden': 5, 'padre': 'Gestión'},
            
            # Nivel 1: Administración
            {'nombre': 'Administración', 'icono': 'fas fa-cog', 'url': None, 'orden': 3},
            #   Nivel 2: Usuarios
            {'nombre': 'Usuarios', 'icono': 'fas fa-users-cog', 'url': 'admin.usuarios', 'orden': 1, 'padre': 'Administración'},
            #   Nivel 2: Roles
            {'nombre': 'Roles', 'icono': 'fas fa-shield-alt', 'url': 'admin.listar_roles', 'orden': 2, 'padre': 'Administración'},
            #   Nivel 2: Matriz de Permisos
            {'nombre': 'Matriz de Permisos', 'icono': 'fas fa-table', 'url': 'admin.matriz_permisos', 'orden': 3, 'padre': 'Administración'},
            #   Nivel 2: Gestión de Menús
            {'nombre': 'Gestión de Menús', 'icono': 'fas fa-bars', 'url': 'admin.gestionar_menus', 'orden': 4, 'padre': 'Administración'},
        ]
        
        # Crear diccionario para referenciar por nombre
        menu_dict = {}
        
        # Primero crear todos los menús
        for menu_data in menus:
            menu = Menu(
                nombre=menu_data['nombre'],
                icono=menu_data['icono'],
                url=menu_data['url'],
                orden=menu_data['orden']
            )
            db.session.add(menu)
            db.session.flush()
            menu_dict[menu_data['nombre']] = menu
        
        # Luego establecer relaciones padre-hijo
        for menu_data in menus:
            if 'padre' in menu_data:
                hijo = menu_dict[menu_data['nombre']]
                padre = menu_dict[menu_data['padre']]
                hijo.padre_id = padre.id
        
        db.session.commit()
        print(f"✅ {len(menus)} menús creados")
        
        # Mostrar estructura
        print("\n📋 Estructura de menús:")
        menus_raiz = Menu.query.filter_by(padre_id=None).order_by(Menu.orden).all()
        for menu in menus_raiz:
            print(f"  📁 {menu.nombre}")
            for hijo in menu.hijos.order_by(Menu.orden).all():
                print(f"     📄 {hijo.nombre} -> {hijo.url}")

if __name__ == '__main__':
    crear_tabla_menus()
    