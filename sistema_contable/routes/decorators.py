from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

# Decorador para verificar permisos de usuario
def permiso_requerido(*permisos_necesarios):
    """
    Decorador para verificar que el usuario actual tiene al menos UNO de los permisos requeridos.
    Uso: @permiso_requerido('ver_clientes', 'ser_admin')
    """
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # Verifica si el usuario está autenticado (asumiendo que usas Flask-Login)
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder.', 'warning')
                return redirect(url_for('auth.login'))

            # Itera sobre los permisos requeridos
            for permiso in permisos_necesarios:
                if current_user.tiene_permiso(permiso):
                    # Si tiene AL MENOS UNO, se le permite el acceso
                    return func(*args, **kwargs)

            # Si el usuario está autenticado pero no tiene NINGUNO de los permisos, se deniega el acceso.
            flash('No tienes permisos suficientes para acceder a esta página.', 'danger')
            return abort(403)  # O redirigir a una página de "acceso denegado"
        return decorated_view
    return decorator