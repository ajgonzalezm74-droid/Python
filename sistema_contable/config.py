import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/dbssc.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False