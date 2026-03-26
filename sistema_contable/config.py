import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-desarrollo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'instance', 
        'dbsgc.sqlite'  # CORREGIDO
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False