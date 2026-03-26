# routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify
from functools import wraps
from models import db
from models.usuario import Usuario
from models.rol import Rol
from models.permiso import Permiso
from flask_wtf.csrf import generate_csrf

admin_bp = Blueprint('admin', __name__)

# Decorador para verificar permisos de administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión', 'error')
            return redirect(url_for('auth.login'))
        
        permisos = session.get('permisos', [])
        if 'admin_usuarios' not in permisos and 'admin_total' not in permisos:
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# GESTIÓN DE USUARIOS
# ============================================

@admin_bp.route('/admin/usuarios')
@admin_required
def usuarios():
    """Listar todos los usuarios"""
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', 
                         usuarios=usuarios,
                         csrf_token=generate_csrf())

@admin_bp.route('/admin/usuarios/nuevo', methods=['GET', 'POST'])
@admin_required
def usuario_nuevo():
    """Crear nuevo usuario"""
    if request.method == 'POST':
        username = request.form.get('username')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        roles_ids = request.form.getlist('roles')
        activo = 'activo' in request.form
        
        # Validaciones
        errores = []
        
        if Usuario.query.filter_by(username=username).first():
            errores.append(f"El nombre de usuario '{username}' ya está en uso")
        
        if Usuario.query.filter_by(email=email).first():
            errores.append(f"El email '{email}' ya está registrado")
        
        if errores:
            for error in errores:
                flash(error, 'error')
            roles = Rol.query.all()
            return render_template('admin/usuario_nuevo.html', 
                                 roles=roles, 
                                 datos=request.form)
        
        # Crear usuario
        usuario = Usuario(
            username=username,
            nombre=nombre,
            email=email,
            activo=activo
        )
        usuario.set_password(password)
        
        # Asignar roles
        for rol_id in roles_ids:
            rol = Rol.query.get(rol_id)
            if rol:
                usuario.roles.append(rol)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash(f'Usuario {username} creado exitosamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    # GET - mostrar formulario
    roles = Rol.query.all()
    return render_template('admin/usuario_nuevo.html', roles=roles, datos={})

# Context processor para cargar menú dinámico según permisos
@admin_bp.route('/admin/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def usuario_editar(id):
    """Editar usuario existente"""
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.username = request.form.get('username')
        usuario.nombre = request.form.get('nombre')
        usuario.email = request.form.get('email')
        usuario.activo = 'activo' in request.form
        
        # Actualizar roles
        roles_ids = request.form.getlist('roles')
        usuario.roles = []
        for rol_id in roles_ids:
            rol = Rol.query.get(rol_id)
            if rol:
                usuario.roles.append(rol)
        
        db.session.commit()
        flash('Usuario actualizado', 'success')
        return redirect(url_for('admin.usuarios'))
    
    roles = Rol.query.all()
    return render_template('admin/usuario_editar.html', 
                         usuario=usuario, 
                         roles=roles,
                         csrf_token=generate_csrf())

@admin_bp.route('/admin/usuarios/<int:id>/eliminar', methods=['POST'])
@admin_required
def usuario_eliminar(id):
    """Eliminar usuario (solo superadmin)"""
    if id == session.get('user_id'):
        return jsonify({'error': 'No puedes eliminar tu propio usuario'}), 400
    
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuario eliminado correctamente'})

@admin_bp.route('/admin/usuarios/cambiar-password', methods=['POST'])
@admin_required
def cambiar_password():
    """Cambiar contraseña de un usuario"""
    usuario_id = request.form.get('usuario_id')
    password = request.form.get('password')
    
    if not password:
        flash('La contraseña no puede estar vacía', 'error')
        return redirect(request.referrer or url_for('admin.usuarios'))
    
    if len(password) < 6:
        flash('La contraseña debe tener al menos 6 caracteres', 'error')
        return redirect(request.referrer or url_for('admin.usuarios'))
    
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.set_password(password)
        db.session.commit()
        flash(f'Contraseña actualizada correctamente', 'success')
    else:
        flash('Usuario no encontrado', 'error')
    
    return redirect(url_for('admin.usuario_editar', id=usuario_id))

# ============================================
# GESTIÓN DE ROLES (CRUD completo)
# ============================================

@admin_bp.route('/admin/roles')
@admin_required
def listar_roles():
    """Listar todos los roles"""
    roles = Rol.query.all()
    return render_template('admin/roles.html', roles=roles, csrf_token=generate_csrf())

@admin_bp.route('/admin/roles/nuevo', methods=['GET', 'POST'])
@admin_required
def crear_rol():
    """Crear nuevo rol con permisos"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        permisos_ids = request.form.getlist('permisos')
        
        if Rol.query.filter_by(nombre=nombre).first():
            flash('El nombre del rol ya existe', 'error')
            return redirect(url_for('admin.crear_rol'))
        
        rol = Rol(nombre=nombre, descripcion=descripcion)
        
        for permiso_id in permisos_ids:
            permiso = Permiso.query.get(permiso_id)
            if permiso:
                rol.permisos.append(permiso)
        
        db.session.add(rol)
        db.session.commit()
        
        flash(f'Rol "{nombre}" creado exitosamente', 'success')
        return redirect(url_for('admin.listar_roles'))
    
    # GET - mostrar formulario
    permisos = Permiso.query.order_by(Permiso.modulo, Permiso.nombre).all()
    permisos_por_modulo = {}
    for p in permisos:
        if p.modulo not in permisos_por_modulo:
            permisos_por_modulo[p.modulo] = []
        permisos_por_modulo[p.modulo].append(p)
    
    return render_template('admin/rol_form.html', 
                         rol=None, 
                         permisos_por_modulo=permisos_por_modulo,
                         csrf_token=generate_csrf())

@admin_bp.route('/admin/roles/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_rol(id):
    """Editar rol existente"""
    rol = Rol.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        permisos_ids = request.form.getlist('permisos')
        
        otro_rol = Rol.query.filter(Rol.nombre == nombre, Rol.id_rol != id).first()
        if otro_rol:
            flash('El nombre del rol ya existe', 'error')
            return redirect(url_for('admin.editar_rol', id=id))
        
        rol.nombre = nombre
        rol.descripcion = descripcion
        rol.permisos = []
        
        for permiso_id in permisos_ids:
            permiso = Permiso.query.get(permiso_id)
            if permiso:
                rol.permisos.append(permiso)
        
        db.session.commit()
        
        flash(f'Rol "{nombre}" actualizado correctamente', 'success')
        return redirect(url_for('admin.listar_roles'))
    
    # GET - mostrar formulario
    permisos = Permiso.query.order_by(Permiso.modulo, Permiso.nombre).all()
    permisos_por_modulo = {}
    for p in permisos:
        if p.modulo not in permisos_por_modulo:
            permisos_por_modulo[p.modulo] = []
        permisos_por_modulo[p.modulo].append(p)
    
    return render_template('admin/rol_form.html', 
                         rol=rol, 
                         permisos_por_modulo=permisos_por_modulo,
                         csrf_token=generate_csrf())

@admin_bp.route('/admin/roles/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_rol(id):
    """Eliminar rol (solo si no tiene usuarios asignados)"""
    rol = Rol.query.get_or_404(id)
    
    if rol.usuarios:
        return jsonify({'error': 'No se puede eliminar un rol con usuarios asignados'}), 400
    
    db.session.delete(rol)
    db.session.commit()
    
    return jsonify({'message': 'Rol eliminado correctamente'})

@admin_bp.route('/admin/roles/<int:id>/permisos')
@admin_required
def obtener_permisos_rol(id):
    """Obtener permisos de un rol en formato JSON"""
    rol = Rol.query.get_or_404(id)
    permisos = [{'nombre': p.nombre, 'modulo': p.modulo, 'descripcion': p.descripcion} 
                for p in rol.permisos]
    return jsonify(permisos)

@admin_bp.route('/admin/roles/<int:id>/usuarios')
@admin_required
def rol_usuarios(id):
    """Ver usuarios que tienen este rol"""
    rol = Rol.query.get_or_404(id)
    usuarios = rol.usuarios
    return render_template('admin/rol_usuarios.html', rol=rol, usuarios=usuarios)

# ============================================
# RUTAS PARA SUPERADMIN
# ============================================

@admin_bp.route('/admin/super/dashboard')
@admin_required
def super_dashboard():
    """Dashboard para superadmin"""
    stats = {
        'total_usuarios': Usuario.query.count(),
        'usuarios_activos': Usuario.query.filter_by(activo=True).count(),
        'total_roles': Rol.query.count(),
        'total_permisos': Permiso.query.count(),
    }
    ultimos_usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).limit(5).all()
    return render_template('admin/super_dashboard.html', 
                         stats=stats, 
                         ultimos_usuarios=ultimos_usuarios)

@admin_bp.route('/admin/super/roles')
@admin_required
def super_roles():
    """Gestión de roles para superadmin"""
    roles = Rol.query.all()
    permisos = Permiso.query.all()
    return render_template('admin/super_roles.html', 
                         roles=roles, 
                         permisos=permisos)

@admin_bp.route('/admin/super/permisos')
@admin_required
def super_permisos():
    """Ver todos los permisos"""
    permisos = Permiso.query.order_by(Permiso.modulo, Permiso.nombre).all()
    return render_template('admin/super_permisos.html', permisos=permisos)
#---------------------------------------------------------------------------------
# Ruta para guardar la matriz de permisos por rol (usada en superadmin)
#---------------------------------------------------------------------------------
@admin_bp.route('/admin/roles/matriz/guardar', methods=['POST'])
@admin_required
def guardar_permisos_matriz():
    """Guardar la matriz de permisos por rol"""
    try:
        data = request.get_json()
        
        for rol_id, permisos_data in data.items():
            rol = Rol.query.get(int(rol_id))
            if not rol or rol.nombre == 'superadmin':
                continue
            
            # Obtener todos los permisos actuales del rol
            permisos_actuales = {p.nombre for p in rol.permisos}
            
            # Nuevos permisos a asignar
            nuevos_permisos = set()
            
            for permiso_nombre, activado in permisos_data.items():
                if activado:
                    # Buscar el permiso en la BD
                    permiso = Permiso.query.filter_by(nombre=permiso_nombre).first()
                    if permiso:
                        nuevos_permisos.add(permiso)
            
            # Actualizar permisos del rol
            rol.permisos = list(nuevos_permisos)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Permisos actualizados correctamente'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    @admin_bp.route('/admin/roles/matriz')
    
    # Vista para mostrar la matriz de permisos por rol
    @admin_required
    def matriz_permisos():
        """Vista matriz de permisos por rol"""
        roles = Rol.query.all()
        
        # Módulos del sistema
        modulos = ['clientes', 'cobranzas', 'pagos', 'citas', 'reportes', 'usuarios']
        
        # Acciones
        acciones = ['view', 'read', 'write', 'delete']
        
        # Obtener permisos actuales por rol
        permisos_por_rol = {}
        for rol in roles:
            permisos_por_rol[rol.id_rol] = {p.nombre for p in rol.permisos}
        
        return render_template('admin/roles_matriz.html',
                            roles=roles,
                            modulos=modulos,
                            acciones=acciones,
                            permisos_por_rol=permisos_por_rol,
                            csrf_token=generate_csrf())
        
# ---------------------------------------------------------------------------
# routes/admin.py - Agregar estas rutas
# Context processor para cargar menú dinámico según permisos
# ---------------------------------------------------------------------------------
@admin_bp.route('/admin/permisos/todos')
@admin_required
def obtener_todos_permisos():
    """Obtener todos los permisos del sistema"""
    permisos = Permiso.query.order_by(Permiso.modulo, Permiso.nombre).all()
    return jsonify([{
        'id_permiso': p.id_permiso,
        'nombre': p.nombre,
        'modulo': p.modulo,
        'descripcion': p.descripcion
    } for p in permisos])

@admin_bp.route('/admin/roles/<int:id>')
@admin_required
def obtener_rol(id):
    """Obtener un rol específico"""
    rol = Rol.query.get_or_404(id)
    return jsonify({
        'id_rol': rol.id_rol,
        'nombre': rol.nombre,
        'descripcion': rol.descripcion,
        'permisos': [p.id_permiso for p in rol.permisos]
    })

@admin_bp.route('/admin/roles/<int:id>/usuarios')
@admin_required
def obtener_usuarios_rol(id):
    """Obtener usuarios de un rol"""
    rol = Rol.query.get_or_404(id)
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'nombre': u.nombre,
        'email': u.email
    } for u in rol.usuarios])

@admin_bp.route('/admin/roles/nuevo', methods=['POST'])
@admin_required
def crear_rol_api():
    """Crear nuevo rol vía API"""
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    permisos_ids = data.get('permisos', [])
    
    if Rol.query.filter_by(nombre=nombre).first():
        return jsonify({'success': False, 'message': 'El nombre del rol ya existe'}), 400
    
    rol = Rol(nombre=nombre, descripcion=descripcion)
    
    for permiso_id in permisos_ids:
        permiso = Permiso.query.get(permiso_id)
        if permiso:
            rol.permisos.append(permiso)
    
    db.session.add(rol)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Rol "{nombre}" creado'})

@admin_bp.route('/admin/roles/<int:id>/editar', methods=['PUT'])
@admin_required
def editar_rol_api(id):
    """Editar rol vía API"""
    rol = Rol.query.get_or_404(id)
    data = request.get_json()
    
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    permisos_ids = data.get('permisos', [])
    
    # Verificar nombre duplicado
    otro = Rol.query.filter(Rol.nombre == nombre, Rol.id_rol != id).first()
    if otro:
        return jsonify({'success': False, 'message': 'El nombre del rol ya existe'}), 400
    
    rol.nombre = nombre
    rol.descripcion = descripcion
    rol.permisos = []
    
    for permiso_id in permisos_ids:
        permiso = Permiso.query.get(permiso_id)
        if permiso:
            rol.permisos.append(permiso)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Rol "{nombre}" actualizado'})

@admin_bp.route('/admin/roles/<int:id>/eliminar', methods=['DELETE'])
@admin_required
def eliminar_rol_api(id):
    """Eliminar rol vía API"""
    rol = Rol.query.get_or_404(id)
    
    if rol.usuarios:
        return jsonify({'success': False, 'message': 'No se puede eliminar un rol con usuarios asignados'}), 400
    
    db.session.delete(rol)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Rol eliminado'})
        
# routes/admin.py - Agregar al final del archivo
# Context processor para cargar menú dinámico según permisos
#---------------------------------------------------------------------------------
from models.menu import Menu, MenuRoles

@admin_bp.route('/admin/menus')
@admin_required
def gestionar_menus():
    """Gestión de menús dinámicos"""
    from models.menu import Menu
    from models.rol import Rol
    
    # Obtener todos los menús (sin filtrar por padre para mostrar jerarquía)
    menus = Menu.query.filter_by(padre_id=None).order_by(Menu.orden).all()
    roles = Rol.query.all()
    
    return render_template('admin/menus.html', 
                         menus=menus, 
                         roles=roles, 
                         csrf_token=generate_csrf())