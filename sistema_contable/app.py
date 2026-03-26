# app.py
from flask import Flask, redirect, url_for
from models import db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.clientes import clientes_bp
from routes.cobranzas import cobranzas_bp
from routes.pagos import pagos_bp
from routes.citas import citas_bp
from routes.reportes import reportes_bp
import os

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'instance', 
        'dbsgc.sqlite'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'tu_clave_secreta_aqui'
    
    # CONFIGURACIÓN CSRF
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)
    
    # Excluir login de CSRF
    csrf.exempt('auth.login')
    
    # ============================================
    # CONTEXT PROCESSOR PARA MENÚ DINÁMICO
    # ============================================
    @app.context_processor
    def inject_menu():
        from models.menu import Menu
        from models.usuario import Usuario
        from flask import session
        
        def get_user_menus():
            if 'user_id' not in session:
                print("⚠️ No hay usuario en sesión")
                return []
            
            usuario = Usuario.query.get(session['user_id'])
            if not usuario:
                print("⚠️ Usuario no encontrado")
                return []
            
            permisos_usuario = set(usuario.get_permisos())
            print(f"🔐 Permisos para menú: {len(permisos_usuario)} permisos")
            
            # Verificar si tiene permisos de administración
            tiene_admin = 'admin_usuarios' in permisos_usuario or 'admin_total' in permisos_usuario
            print(f"📌 Tiene permisos de admin: {tiene_admin}")
            
            # Obtener menús raíz
            menus = Menu.query.filter_by(padre_id=None, activo=True).order_by(Menu.orden).all()
            
            result = []
            for menu in menus:
                # Obtener hijos
                hijos = list(menu.hijos.filter_by(activo=True).order_by(Menu.orden).all())
                print(f"📁 Procesando: {menu.nombre} - {len(hijos)} hijos")
                
                # Dashboard siempre visible
                if menu.nombre == 'Dashboard':
                    result.append(menu)
                    print(f"  ✅ Dashboard agregado")
                
                # Gestión
                elif menu.nombre == 'Gestión':
                    hijos_visibles = []
                    for hijo in hijos:
                        if hijo.url:
                            modulo = hijo.url.split('.')[0]
                            permiso_necesario = f"ver_{modulo}"
                            if permiso_necesario in permisos_usuario or 'admin_total' in permisos_usuario:
                                hijos_visibles.append(hijo)
                                print(f"  ✅ {hijo.nombre} visible")
                            else:
                                print(f"  ❌ {hijo.nombre} oculto (falta {permiso_necesario})")
                    if hijos_visibles:
                        menu.hijos = hijos_visibles
                        result.append(menu)
                        print(f"  📁 Gestión agregada con {len(hijos_visibles)} submenús")
                
                # Administración
                elif menu.nombre == 'Administración':
                    if tiene_admin:
                        menu.hijos = hijos
                        result.append(menu)
                        print(f"  ✅ Administración agregada con {len(hijos)} submenús")
                    else:
                        print(f"  ❌ Administración oculta (sin permisos de admin)")
                
                # Otros menús
                else:
                    result.append(menu)
                    print(f"  ✅ {menu.nombre} agregado")
            
            print(f"📋 Menús finales: {[m.nombre for m in result]}")
            return result
        
        return {'menu_principal': get_user_menus()}
    
    # ============================================
    # CONTEXT PROCESSOR PARA CSRF
    # ============================================
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)
    
    # Inicializar db
    db.init_app(app)
    
    # Verificar conexión
    with app.app_context():
        try:
            db.engine.connect()
            print(f"✅ Conectado a BD: dbsgc.sqlite")
            
            from models.usuario import Usuario
            from models.rol import Rol
            from models.permiso import Permiso
            print("✅ Modelos cargados correctamente")
            
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            if 'menus' not in inspector.get_table_names():
                print("⚠️ Tabla 'menus' no encontrada. Ejecuta scripts/crear_tabla_menus.py")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(cobranzas_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(citas_bp)
    app.register_blueprint(reportes_bp)
    
    # Ruta raíz
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)