from flask import Flask, send_from_directory
from extensions import db
from routes.api import api
from routes.views import views
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Base de datos SQLite
db_path = os.path.join(basedir, "instance", "tasas.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Blueprints
app.register_blueprint(api)
app.register_blueprint(views)

# Service worker
@app.route('/sw.js')
def serve_sw():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'js'),
        'sw.js'
    )

# Ejecutar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)