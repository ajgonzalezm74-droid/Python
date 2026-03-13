from flask import Blueprint, jsonify, request
import os
from services.ia_service import obtener_respuesta_ia
from services.analisis_service import calcular_variacion_rango
from models import HistorialTasa
import re
from datetime import datetime
from services.tasas_service import actualizar_todo, db # Importamos db también

api = Blueprint("api", __name__)

# --- NUEVA RUTA PARA LA CALCULADORA ---
@api.route("/tasas") # Si el prefix es /api, esto será /api/tasas
def obtener_tasas():
    """Endpoint que consume el JS de la calculadora"""
    try:
        # 1. Intentar actualizar (trae de BCV/Binance y guarda si cambió)
        actualizar_todo()
        
        # 2. Consultar los últimos valores de la BD para responder al JS
        def get_last(tipo):
            res = HistorialTasa.query.filter_by(tipo=tipo).order_by(HistorialTasa.fecha.desc()).first()
            return res.valor if res else 0.0

        return jsonify({
            "bcv_usd": get_last("bcv_usd"),
            "bcv_eur": get_last("bcv_eur"),
            "p2p_ves": get_last("p2p_ves"),
            "status": "success"
        })
    except Exception as e:
        print(f"Error en API tasas: {e}")
        return jsonify({"error": str(e)}), 500

# --- TUS RUTAS ANTERIORES (Limpiamos el prefijo /api si ya está en el Blueprint) ---

@api.route("/variacion/<tipo>/<fecha_inicio>/<fecha_fin>")
def variacion(tipo, fecha_inicio, fecha_fin):
    resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
    return jsonify({"variacion": resultado})

@api.route('/chat', methods=['POST'])
def chat():
    # ... (tu código de chat actual se mantiene igual)
    pregunta = request.json.get("pregunta").lower()
    respuesta = obtener_respuesta_ia(pregunta)
    return jsonify({"respuesta": respuesta})
