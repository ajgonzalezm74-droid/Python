from flask import Blueprint, render_template
from models.cobranzas import Cobranza
from models.pagos import Pago
from models import db
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():

    ingresos = db.session.query(func.sum(Cobranza.monto)).scalar() or 0
    gastos = db.session.query(func.sum(Pago.monto)).scalar() or 0

    balance = ingresos - gastos

    return render_template(
        "dashboard.html",
        ingresos=ingresos,
        gastos=gastos,
        balance=balance
    )