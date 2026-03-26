# scripts/ver_rutas_admin.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()
with app.app_context():
    print("\n=== RUTAS DE ADMIN ===\n")
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('admin.'):
            print(f"{rule.endpoint}: {rule.rule}")