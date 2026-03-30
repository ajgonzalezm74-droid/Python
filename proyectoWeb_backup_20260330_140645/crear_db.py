from app import app
from extensions import db
import models

print("Tablas registradas antes de create_all():")
print(db.metadata.tables.keys())

with app.app_context():
    db.create_all()
    print("Tablas después de create_all():")
    print(db.metadata.tables.keys())