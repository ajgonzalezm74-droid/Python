from models import db

# Tabla pivote para usuarios y roles
usuario_roles = db.Table('usuario_roles',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True)
)

# Tabla pivote para roles y permisos
roles_permisos = db.Table('roles_permisos',
    db.Column('id_rol', db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True),
    db.Column('id_permiso', db.Integer, db.ForeignKey('permisos.id_permiso'), primary_key=True)
)