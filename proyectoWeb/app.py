from flask import Flask
from extensions import db
from routes.api import api
from routes.views import views
import os

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
    return app.send_static_file('sw.js')


if __name__ == "__main__":
    app.run(debug=True)