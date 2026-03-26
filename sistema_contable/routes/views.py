from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'tu_template.html')@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if username in USERS and USERS[username]['password'] == password:
            session['user'] = username
            session['nombre'] = USERS[username]['nombre']
            
            # 🔐 CARGAR PERMISOS DEL USUARIO (desde BD o desde configuración)
            # Ejemplo con tu USERS actual (cuando migres a BD, esto vendrá de la consulta)
            if username == 'admin@gmail.com':
                session['permisos'] = [
                    'ver_clientes', 'crear_clientes', 'editar_clientes', 'eliminar_clientes',
                    'ver_cobranzas', 'crear_cobranzas', 'editar_cobranzas',
                    'ver_citas', 'crear_citas', 'editar_citas', 'eliminar_citas',
                    'ver_reportes', 'exportar_reportes',
                    'admin_total'
                ]
            else:
                session['permisos'] = ['ver_clientes', 'ver_cobranzas']  # permisos básicos
            
            if remember:
                session.permanent = True
            
            flash('¡Bienvenido!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

def dashboard(request):
    return render(request, 'dashboard.html')