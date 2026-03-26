# routes/clientes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.auth import login_required, permiso_requerido
from models import db
from models.cliente import Cliente
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes')
@login_required
@permiso_requerido('ver_clientes')
def listar():
    """Lista de clientes"""
    clientes = Cliente.query.filter_by(activo=True).all()
    return render_template('clientes/lista.html', clientes=clientes)

@clientes_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_clientes')
def nuevo():
    """Crear nuevo cliente"""
    if request.method == 'POST':
        # Crear cliente con el usuario actual
        cliente = Cliente(
            id_documento=request.form.get('id_documento'),
            tipo_documento=request.form.get('tipo_documento', 'V'),
            nombre=request.form.get('nombre'),
            apellidos=request.form.get('apellidos'),
            direccion=request.form.get('direccion'),
            ciudad=request.form.get('ciudad'),
            codigo_postal=request.form.get('codigo_postal'),
            rif=request.form.get('rif'),
            nombre_compania=request.form.get('nombre_compania'),
            cargo=request.form.get('cargo'),
            departamento=request.form.get('departamento'),
            notas=request.form.get('notas'),
            telefono=request.form.get('telefono'),
            telefono_alternativo=request.form.get('telefono_alternativo'),
            email=request.form.get('email'),
            pais=request.form.get('pais'),
            estado=request.form.get('estado'),
            id_usuario=session.get('user_id'),  # Usuario que crea
            activo=True
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        flash(f'Cliente {cliente.nombre_completo} creado exitosamente', 'success')
        return redirect(url_for('clientes.listar'))
    
    return render_template('clientes/nuevo.html')

@clientes_bp.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_clientes')
def editar(id):
    """Editar cliente"""
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.id_documento = request.form.get('id_documento')
        cliente.tipo_documento = request.form.get('tipo_documento')
        cliente.nombre = request.form.get('nombre')
        cliente.apellidos = request.form.get('apellidos')
        cliente.direccion = request.form.get('direccion')
        cliente.ciudad = request.form.get('ciudad')
        cliente.codigo_postal = request.form.get('codigo_postal')
        cliente.rif = request.form.get('rif')
        cliente.nombre_compania = request.form.get('nombre_compania')
        cliente.cargo = request.form.get('cargo')
        cliente.departamento = request.form.get('departamento')
        cliente.notas = request.form.get('notas')
        cliente.telefono = request.form.get('telefono')
        cliente.telefono_alternativo = request.form.get('telefono_alternativo')
        cliente.email = request.form.get('email')
        cliente.pais = request.form.get('pais')
        cliente.estado = request.form.get('estado')
        cliente.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes.listar'))
    
    return render_template('clientes/editar.html', cliente=cliente)

@clientes_bp.route('/clientes/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_clientes')
def eliminar(id):
    """Eliminar cliente (soft delete)"""
    cliente = Cliente.query.get_or_404(id)
    cliente.activo = False
    db.session.commit()
    
    return {'message': 'Cliente eliminado correctamente'}, 200