# routes/pagos.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/pagos')
@login_required
def listar():
    """Lista de pagos"""
    pagos = []  # Temporal
    return render_template('pagos/lista.html', pagos=pagos)

@pagos_bp.route('/pagos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Registrar nuevo pago"""
    if request.method == 'POST':
        flash('Pago registrado exitosamente', 'success')
        return redirect(url_for('pagos.listar'))
    return render_template('pagos/nuevo.html')