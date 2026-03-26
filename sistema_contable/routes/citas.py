# routes/citas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required

citas_bp = Blueprint('citas', __name__)

@citas_bp.route('/citas')
@login_required
def listar():
    """Lista de citas"""
    citas = []  # Temporal
    return render_template('citas/lista.html', citas=citas)

@citas_bp.route('/citas/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Agendar nueva cita"""
    if request.method == 'POST':
        flash('Cita agendada exitosamente', 'success')
        return redirect(url_for('citas.listar'))
    return render_template('citas/nuevo.html')