# crear_tabla.py
from app import app
from extensions import db
from models import CalculoUsuario, User, HistorialTasa

def crear_tablas():
    with app.app_context():
        print("=== Creando tablas en la base de datos ===\n")
        
        # Mostrar configuración
        db_path = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"Base de datos: {db_path}\n")
        
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        print("✓ Proceso completado\n")
        
        # Verificar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tablas = inspector.get_table_names()
        
        print(f"Tablas encontradas ({len(tablas)}):")
        for tabla in sorted(tablas):
            print(f"  - {tabla}")
        
        # Verificar específicamente calculo_usuario
        print("\n=== Verificando tabla 'calculo_usuario' ===")
        if 'calculo_usuario' in tablas:
            print("✅ TABLA EXISTE\n")
            
            print("Estructura:")
            columnas = inspector.get_columns('calculo_usuario')
            for col in columnas:
                print(f"  • {col['name']:15} {str(col['type']):20} {'NULL' if col['nullable'] else 'NOT NULL'}")
            
            # Contar registros
            try:
                count = CalculoUsuario.query.count()
                print(f"\nRegistros actuales: {count}")
            except Exception as e:
                print(f"Error al contar: {e}")
        else:
            print("❌ ERROR: La tabla 'calculo_usuario' NO existe")
            print("\nPosibles soluciones:")
            print("1. Verifica que el modelo esté correctamente definido")
            print("2. Ejecuta: flask --app app shell")
            print("3. Dentro del shell: from extensions import db; db.create_all()")

if __name__ == "__main__":
    crear_tablas()
