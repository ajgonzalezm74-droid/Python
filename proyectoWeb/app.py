# app.py
from flask import Flask, send_from_directory
from flask_login import LoginManager
from extensions import db
import os

app = Flask(__name__)

# Configuración - Usar la base de datos existente
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'tasas.db')

app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiala-por-una-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"📁 Base de datos en: {DB_PATH}")

# Inicializar extensiones
db.init_app(app)

# Configurar Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

# Importar modelos
from models import User, HistorialTasa, CalculoUsuario

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importar blueprints
from routes.views import views
from routes.auth import auth

# Registrar blueprints
app.register_blueprint(views)
app.register_blueprint(auth)

# Service worker

@app.route('/sw.js')
def serve_sw():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'js'),
        'sw.js',
        mimetype='application/javascript'
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)