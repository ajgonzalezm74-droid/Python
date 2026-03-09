from flask import Blueprint, render_template,request
from exchange_provider import ExchangeProvider
from services.tasas_service import guardar_si_cambia, actualizar_todo
from services.analisis_service import calcular_variacion_rango, obtener_historial_por_rango
from models import HistorialTasa
from extensions import db
from sqlalchemy import distinct




# Crear Blueprint primero
views = Blueprint("views", __name__)


@views.route("/")
def inicio():
         # Esto hace que se ejecute al abrir la página del proyecto
    actualizar_todo()  # <--- Esto dispara la lógica al abrir la web
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
    # Dentro del route /calculadora
    print("Actualizando tasas desde calculadora...")
    print("Obteniendo tasas...")
    print("BCV USD:", provider.get_bcv_rates().get("USD", "Error"))
    print("BCV EUR:", provider.get_bcv_rates().get("EUR", "Error"))
    print("P2P VES:", provider.get_binance_p2p())   
    try:
        binance = provider.get_binance_p2p()  # intento real
        # 🔹 Protección total
        if not binance or binance <= 0:
            raise ValueError("Binance inválido")
        guardar_si_cambia("p2p_ves", binance)
    except Exception as e:
        print("⚠ Error Binance:", e)
        # 🔹 Fallback: última válida en BD
        ultima = (
            HistorialTasa.query
            .filter_by(tipo="p2p_ves")
            .order_by(HistorialTasa.fecha.desc())
            .first()
        )
        binance = ultima.valor if ultima else 0.0  # 0 solo si nunca hay registro

    tasas = {
        "bcv_usd": HistorialTasa.query.filter_by(tipo="bcv_usd").order_by(HistorialTasa.fecha.desc()).first().valor,
        "bcv_eur": HistorialTasa.query.filter_by(tipo="bcv_eur").order_by(HistorialTasa.fecha.desc()).first().valor,
        "p2p_ves": binance
    }
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
    
    #tasas = actualizar_todo() # Se asegura de tener lo último al calcular
    
    return render_template("contacto.html")

