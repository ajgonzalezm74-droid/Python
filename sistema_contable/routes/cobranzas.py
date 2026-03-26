# routes/cobranzas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required

cobranzas_bp = Blueprint('cobranzas', __name__)

@cobranzas_bp.route('/cobranzas')
@login_required
def listar():
    """Lista de cobranzas"""
    cobranzas = []  # Temporal
    return render_template('cobranzas/lista.html', cobranzas=cobranzas)

@cobranzas_bp.route('/cobranzas/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Crear nueva cobranza"""
    if request.method == 'POST':
        flash('Cobranza registrada exitosamente', 'success')
        return redirect(url_for('cobranzas.listar'))
    return render_template('cobranzas/nuevo.html')