# routes/reportes.py
from flask import Blueprint, render_template
from routes.auth import login_required

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reportes')
@login_required
def dashboard():
    """Dashboard de reportes"""
    return render_template('reportes/dashboard.html')