from flask import Blueprint, jsonify,request
import os
from services.ia_service import obtener_respuesta_ia
from services.analisis_service import calcular_variacion_rango
from models import HistorialTasa  # Asegúrate de que la ruta sea correcta
import re
from datetime import datetime
from services.tasas_service import actualizar_todo



api = Blueprint("api", __name__)

@api.route("/api/variacion/<tipo>/<fecha_inicio>/<fecha_fin>")
def variacion(tipo, fecha_inicio, fecha_fin):
    resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
    return jsonify({"variacion": resultado})



@api.route('/chat', methods=['POST'])
def chat():
    pregunta = request.json.get("pregunta").lower()
    
    # 1. Intentar detectar fechas en el texto (formato dd-mm-aaaa)
    fechas = re.findall(r'\d{2}-\d{2}-\d{4}', pregunta)
    
    query = HistorialTasa.query
    
    # 2. Si el usuario puso un rango de fechas, filtramos la BD
    if len(fechas) >= 2:
        fecha_inicio = datetime.strptime(fechas[0], '%d-%m-%Y')
        fecha_fin = datetime.strptime(fechas[1], '%d-%m-%Y')
        registros = query.filter(HistorialTasa.fecha.between(fecha_inicio, fecha_fin)).all()
    else:
        # Si no hay fechas, enviamos los últimos 15 registros por defecto
        registros = query.order_by(HistorialTasa.fecha.desc()).limit(15).all()
    
    # 3. Se los pasamos a la función de la IA
    respuesta = obtener_respuesta_ia(pregunta)
    
    return jsonify({"respuesta": respuesta})
