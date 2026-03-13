from flask import Flask
from models import db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbssc.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def inicio():
    return "Sistema contable funcionando"

if __name__ == "__main__":
    app.run(debug=True)