# scripts/check_imports.py
import sys
import os

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("=== VERIFICANDO IMPORTS ===")
print(f"Directorio actual: {os.getcwd()}")
print(f"Directorio raíz añadido: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))}")
print(f"Python path: {sys.path}")

try:
    print("\n1. Intentando importar models...")
    from models import db
    print("✅ models importado correctamente")
    
    print("\n2. Intentando importar Usuario...")
    from models.usuario import Usuario
    print("✅ Usuario importado correctamente")
    
    print("\n3. Verificando tabla usuario_roles...")
    from models.asociaciones import usuario_roles
    print("✅ usuario_roles importado correctamente")
    
    print("\n🎉 Todos los imports funcionan!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()