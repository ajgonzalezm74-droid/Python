# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
import requests

auth = Blueprint('auth', __name__)

def validar_email(email):
    """Validar formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_email_real(email):
    """Verificar si el email existe (dominio válido)"""
    try:
        dominio = email.split('@')[1]
        # Verificar si el dominio tiene registro MX
        import socket
        socket.getaddrinfo(dominio, 25)
        return True
    except:
        return False

def validar_telefono(telefono):
    """Validar formato de teléfono venezolano"""
    # Formato: 0412-1234567, 04121234567, +584121234567
    patron = r'^(\+?58|0)?(4\d{2})-?\d{7}$'
    return re.match(patron, telefono) is not None

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        telefono = request.form.get('telefono')
        
        # Validaciones
        errores = []
        
        if not username or len(username) < 3:
            errores.append("El nombre de usuario debe tener al menos 3 caracteres")
        
        if not validar_email(email):
            errores.append("Formato de correo electrónico inválido")
        elif not validar_email_real(email):
            errores.append("El dominio del correo no parece válido")
        
        if not password or len(password) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres")
        
        if password != confirm_password:
            errores.append("Las contraseñas no coinciden")
        
        if telefono and not validar_telefono(telefono):
            errores.append("Formato de teléfono inválido (ej: 04121234567)")
        
        # Verificar si usuario o email ya existen
        if User.query.filter_by(username=username).first():
            errores.append("El nombre de usuario ya está en uso")
        
        if User.query.filter_by(email=email).first():
            errores.append("El correo electrónico ya está registrado")
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('auth.registro'))
        
        # Crear usuario
        nuevo_usuario = User(
            username=username,
            email=email,
            telefono=telefono
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('registro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Buscar por email o username
        user = User.query.filter(
            (User.email == email) | (User.username == email)
        ).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'¡Bienvenido {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.inicio'))
        else:
            flash('Email/Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))

# API para verificar email en tiempo real (AJAX)
@auth.route('/api/verificar-email', methods=['POST'])
def verificar_email():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'valido': False, 'mensaje': 'Email requerido'})
    
    if not validar_email(email):
        return jsonify({'valido': False, 'mensaje': 'Formato de email inválido'})
    
    # Verificar si ya existe
    existe = User.query.filter_by(email=email).first()
    if existe:
        return jsonify({'valido': False, 'mensaje': 'Email ya registrado'})
    
    return jsonify({'valido': True, 'mensaje': 'Email válido'})

@auth.route('/api/verificar-usuario', methods=['POST'])
def verificar_usuario():
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({'valido': False, 'mensaje': 'Usuario requerido'})
    
    if len(username) < 3:
        return jsonify({'valido': False, 'mensaje': 'Mínimo 3 caracteres'})
    
    existe = User.query.filter_by(username=username).first()
    if existe:
        return jsonify({'valido': False, 'mensaje': 'Usuario ya existe'})
    
    return jsonify({'valido': True, 'mensaje': 'Usuario disponible'})
