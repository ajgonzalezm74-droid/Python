# scripts/test_cliente.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models.cliente import Cliente

def test_cliente():
    app = create_app()
    with app.app_context():
        # Contar clientes activos
        total = Cliente.query.filter_by(activo=True).count()
        print(f"📊 Total clientes activos: {total}")
        
        # Listar clientes
        clientes = Cliente.query.filter_by(activo=True).all()
        print(f"👥 Clientes encontrados: {len(clientes)}")
        for c in clientes:
            print(f"   ID: {c.id_cliente}, Nombre: {c.nombre} {c.apellidos}, Email: {c.email}")

if __name__ == '__main__':
    test_cliente()