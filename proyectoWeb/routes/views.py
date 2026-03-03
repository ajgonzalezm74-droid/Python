from flask import Blueprint, render_template,request
from exchange_provider import ExchangeProvider
from services.tasas_service import guardar_si_cambia
from services.analisis_service import calcular_variacion_rango, obtener_historial_por_rango
from models import HistorialTasa
from extensions import db
from sqlalchemy import distinct



# Crear Blueprint primero
views = Blueprint("views", __name__)


@views.route("/")
def inicio():
    return render_template("index.html")

@views.route("/acerca")
def acerca():
    return render_template("acerca.html")

#-----------------
#CALCULADORA
#-----------------  
@views.route("/calculadora")
def calculadora():

    provider = ExchangeProvider()
    tasas = provider.get_all_rates()
    
    
    guardar_si_cambia("bcv_usd", tasas["bcv_usd"])
    guardar_si_cambia("bcv_eur", tasas["bcv_eur"])
    guardar_si_cambia("p2p_ves", tasas["p2p_ves"])
    
    return render_template("calculadora.html", tasas=tasas)
# -------------------------
# TENDENCIA
# -------------------------
@views.route("/tendencia", methods=["GET", "POST"])
def tendencia():

    tipos = db.session.query(HistorialTasa.tipo).distinct().all()
    tipos = [t[0] for t in tipos]

    if request.method == "POST":
        tipo = request.form.get("tipo")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        

        resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)

        

        return render_template(
            "tendencia.html",
            tipos=tipos,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo=tipo,
            resultado=resultado
        )

    return render_template("tendencia.html", tipos=tipos)
# -------------------------
# HISTORIAL
# -------------------------
@views.route("/historial", methods=["GET", "POST"])
def historial():

    tipos = db.session.query(HistorialTasa.tipo).distinct().all()
    tipos = [t[0] for t in tipos]

    
    registros = None
    fecha_inicio = None
    fecha_fin = None
    

    if request.method == "POST":
        tipo = request.form["tipo"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]

        registros = obtener_historial_por_rango(tipo, fecha_inicio, fecha_fin)
        
    return render_template(
        "historial.html",
        tipos=tipos,
        registros=registros,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


# -------------------------
# HISTORIAL TENDENCIA
# -------------------------
@views.route("/historial-tendencia", methods=["GET", "POST"])
def historial_tendencia():

    tipos = db.session.query(HistorialTasa.tipo).distinct().all()
    tipos = [t[0] for t in tipos]
    
    datos = None
    resultado = None

    fecha_inicio = None
    fecha_fin = None

    if request.method == "POST":
        tipo = request.form["tipo"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]

        datos = obtener_historial_por_rango(tipo, fecha_inicio, fecha_fin)
        if datos:
            resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
        else:
            resultado = None

    return render_template(
    "historial_tendencia.html",
    tipos=tipos,
    datos=datos,
    resultado=resultado,
    fecha_inicio=fecha_inicio,
    fecha_fin=fecha_fin
    
)



@views.route("/contacto")
def contacto():
    return render_template("contacto.html")

