# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos después de crear db
from .usuario import Usuario
from .rol import Rol
from .permiso import Permiso
from .asociaciones import usuario_roles, roles_permisos
from .menu import Menu, MenuRoles
# Importar otros modelos según sea necesario
from .cliente import Cliente