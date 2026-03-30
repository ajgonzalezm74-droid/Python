# init_db.py
import os
import sys

# Configurar entorno
os.environ['FLASK_APP'] = 'app.py'

# Importar la app
from app import app
from extensions import db

# Importar modelos (importante: deben importarse ANTES de create_all)
from models import CalculoUsuario
from models import User  # Si User está definido en models.py

def init_database():
    with app.app_context():
        print("=" * 50)
        print("Inicializando Base de Datos")
        print("=" * 50)
        
        # Mostrar configuración
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')
        print(f"Database URI: {db_uri}")
        
        # Verificar si el archivo de base de datos ya existe
        if db_uri and db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            if os.path.exists(db_path):
                print(f"Archivo DB existe: {db_path}")
            else:
                print(f"Archivo DB no existe, se creará: {db_path}")
        
        print("\nCreando tablas...")
        try:
            db.create_all()
            print("✓ Tablas creadas exitosamente")
        except Exception as e:
            print(f"✗ Error al crear tablas: {e}")
            return
        
        # Verificar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tablas = inspector.get_table_names()
        
        print(f"\nTablas encontradas ({len(tablas)}):")
        for tabla in sorted(tablas):
            print(f"  📋 {tabla}")
        
        # Verificar específicamente nuestra tabla
        if 'calculo_usuario' in tablas:
            print("\n✅ TABLA 'calculo_usuario' VERIFICADA")
            
            # Mostrar estructura
            print("\nEstructura de la tabla:")
            print("-" * 40)
            columnas = inspector.get_columns('calculo_usuario')
            for col in columnas:
                print(f"  • {col['name']:15} {str(col['type']):15} nullable: {col['nullable']}")
            
            # Verificar si tiene registros
            try:
                count = CalculoUsuario.query.count()
                print(f"\nRegistros existentes: {count}")
            except Exception as e:
                print(f"Error al contar registros: {e}")
        else:
            print("\n❌ ERROR: Tabla 'calculo_usuario' NO fue creada")
            print("\nPosibles causas:")
            print("  1. El modelo CalculoUsuario no está definido correctamente")
            print("  2. El modelo no fue importado antes de db.create_all()")
            print("  3. Hay errores de sintaxis en el modelo")
            
            # Verificar si el modelo está registrado
            print("\nModelos registrados en SQLAlchemy:")
            for mapper in db.Model.registry.mappers:
                print(f"  • {mapper.class_.__name__}")

if __name__ == "__main__":
    init_database()
