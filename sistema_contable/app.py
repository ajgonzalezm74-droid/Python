from flask import Flask
from config import Config
from models import sqlite as db
from routes.auth import auth_bp
from routes.clientes import clientes_bp
from routes.dashboard import dashboard_bp

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(dashboard_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)