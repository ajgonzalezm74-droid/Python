from flask import Flask, send_from_directory
from extensions import db
from routes.api import api
from routes.views import views
import os
from dotenv import load_dotenv


# Carga las variables ANTES de configurar la app
load_dotenv() 
#chatgpt
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

db_path = os.path.join(basedir, "instance", "tasas.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(api)
app.register_blueprint(views)

@app.route('/sw.js')
def serve_sw():
    # return app.send_static_file('sw.js')
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'js'),
        'sw.js'
    )


if __name__ == "__main__":
    # Render asigna un puerto automáticamente en la variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
    