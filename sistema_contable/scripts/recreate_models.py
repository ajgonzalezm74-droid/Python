# scripts/recreate_models.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db

def recreate_models():
    app = create_app()
    with app.app_context():
        # Eliminar todas las tablas (CUIDADO: borra datos)
        db.drop_all()
        print("✅ Tablas eliminadas")
        
        # Crear tablas nuevamente
        db.create_all()
        print("✅ Tablas creadas correctamente")
        
        # Verificar tablas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Tablas en BD: {tables}")

if __name__ == '__main__':
    respuesta = input("⚠️  Esto ELIMINARÁ TODOS LOS DATOS. ¿Continuar? (s/N): ")
    if respuesta.lower() == 's':
        recreate_models()
    else:
        print("Operación cancelada")