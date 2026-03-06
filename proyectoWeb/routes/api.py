from flask import Blueprint, jsonify,request
import os
from services.ia_service import obtener_respuesta_ia
from services.analisis_service import calcular_variacion_rango


api = Blueprint("api", __name__)

@api.route("/api/variacion/<tipo>/<fecha_inicio>/<fecha_fin>")
def variacion(tipo, fecha_inicio, fecha_fin):
    resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
    return jsonify({"variacion": resultado})


@api.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({"respuesta": "No se recibió JSON"}), 400

    pregunta = data.get("pregunta")

    if not pregunta:
        return jsonify({"respuesta": "No enviaste ninguna pregunta."}), 400

    respuesta = obtener_respuesta_ia(pregunta)

    return jsonify({"respuesta": respuesta})