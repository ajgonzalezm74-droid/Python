# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from functools import wraps
from models import db
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

# Decorador para verificar si el usuario está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar permisos de usuario
def permiso_requerido(*permisos_necesarios):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Por favor, inicia sesión', 'error')
                return redirect(url_for('auth.login'))
            
            user_permisos = session.get('permisos', [])
            
            for permiso in permisos_necesarios:
                if permiso in user_permisos:
                    return f(*args, **kwargs)
            
            flash('No tienes permisos suficientes', 'error')
            return abort(403)
        return decorated_function
    return decorator


# Vista para login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        print(f"🔍 Intentando login: {username}")
        
        # Buscar usuario en BD Permitir login por username o email
        
        usuario = Usuario.query.filter(
            (Usuario.username == username) | (Usuario.email == username)
        ).first()
        
        if usuario:
            print(f"✅ Usuario encontrado: {usuario.username}")
            
            if usuario.activo and usuario.verify_password(password):
                print("✅ Contraseña válida")
                
                # Guardar datos en sesión
                session['user_id'] = usuario.id
                session['username'] = usuario.username
                session['nombre'] = usuario.nombre
                session['email'] = usuario.email
                
                # Cargar permisos
                permisos = usuario.get_permisos()
                session['permisos'] = permisos
                print(f"🔐 Permisos: {permisos}")
                
                if remember:
                    session.permanent = True
                
                flash(f'¡Bienvenido {usuario.nombre}!', 'success')
                
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('dashboard.dashboard'))
            else:
                print("❌ Contraseña inválida")
                flash('Contraseña incorrecta', 'error')
        else:
            print(f"❌ Usuario no encontrado")
            flash('Usuario no encontrado', 'error')
        
        return render_template('login.html')
    
    return render_template('login.html')


# Vista para cerrar sesión 

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))

# Vista para recuperar contraseña

@auth_bp.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    """Vista para recuperar contraseña"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Buscar si el email existe en la BD
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario:
            # Aquí iría la lógica para enviar email con instrucciones
            flash('Se ha enviado un enlace de recuperación a tu correo electrónico', 'info')
            print(f"🔐 Solicitud de recuperación para: {email}")  # Debug
        else:
            flash('No existe una cuenta con ese correo electrónico', 'error')
        
        return redirect(url_for('auth.login'))
    
    # Si es GET, mostrar el formulario de recuperación
    return render_template('recuperar_password.html')