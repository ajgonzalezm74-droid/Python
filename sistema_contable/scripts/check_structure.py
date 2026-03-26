# scripts/check_structure.py
import sqlite3
import os

db_path = 'instance/dbsgc.sqlite'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== VERIFICANDO ESTRUCTURA DE TABLAS ===\n")

tables = ['roles', 'permisos', 'usuarios', 'roles_permisos', 'usuario_roles']

for table in tables:
    print(f"\n📋 Tabla: {table}")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]}: {col[2]}")

conn.close()