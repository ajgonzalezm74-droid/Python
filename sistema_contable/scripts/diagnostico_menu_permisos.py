# scripts/diagnostico_menu_permisos.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models.usuario import Usuario
from models.menu import Menu

def diagnosticar():
    app = create_app()
    with app.app_context():
        # Buscar usuario admin
        usuario = Usuario.query.filter_by(username='admin').first()
        if not usuario:
            print("❌ Usuario 'admin' no encontrado")
            return
        
        print(f"👤 Usuario: {usuario.username}")
        print(f"🔐 Permisos: {usuario.get_permisos()}")
        
        # Verificar si tiene permiso para ver clientes
        print(f"\n✅ Tiene ver_clientes: {'ver_clientes' in usuario.get_permisos()}")
        print(f"✅ Tiene ver_cobranzas: {'ver_cobranzas' in usuario.get_permisos()}")
        print(f"✅ Tiene ver_pagos: {'ver_pagos' in usuario.get_permisos()}")
        print(f"✅ Tiene ver_citas: {'ver_citas' in usuario.get_permisos()}")
        
        # Obtener todos los menús
        print("\n📋 MENÚS EN BASE DE DATOS:")
        menus = Menu.query.order_by(Menu.orden).all()
        for m in menus:
            print(f"  ID:{m.id} | Nombre:{m.nombre} | Padre:{m.padre_id} | URL:{m.url} | Activo:{m.activo}")
        
        # Simular el filtrado de menús
        print("\n🔍 FILTRADO DE MENÚS:")
        permisos_usuario = set(usuario.get_permisos())
        
        raices = Menu.query.filter_by(padre_id=None, activo=True).order_by(Menu.orden).all()
        
        for raiz in raices:
            hijos = list(raiz.hijos.filter_by(activo=True).order_by(Menu.orden).all())
            
            if raiz.nombre == 'Dashboard':
                # Dashboard siempre visible
                print(f"✅ {raiz.nombre} - Visible")
            elif raiz.nombre == 'Gestión':
                # Filtrar hijos según permisos
                hijos_visibles = []
                for hijo in hijos:
                    modulo = hijo.url.split('.')[0] if hijo.url else ''
                    permiso_necesario = f"ver_{modulo}"
                    if permiso_necesario in permisos_usuario or 'admin_total' in permisos_usuario:
                        hijos_visibles.append(hijo)
                        print(f"  ✅ {hijo.nombre} - Visible (permiso: {permiso_necesario})")
                    else:
                        print(f"  ❌ {hijo.nombre} - Oculto (falta: {permiso_necesario})")
                
                if hijos_visibles:
                    print(f"📁 {raiz.nombre} - Visible ({len(hijos_visibles)} submenús)")
                else:
                    print(f"📁 {raiz.nombre} - OCULTO (sin submenús visibles)")
            else:
                # Otros menús
                if raiz.url:
                    modulo = raiz.url.split('.')[0]
                    permiso_necesario = f"ver_{modulo}"
                    if permiso_necesario in permisos_usuario or 'admin_total' in permisos_usuario:
                        print(f"✅ {raiz.nombre} - Visible")
                    else:
                        print(f"❌ {raiz.nombre} - Oculto")
                else:
                    print(f"📁 {raiz.nombre} - Revisar")

if __name__ == '__main__':
    diagnosticar()
    