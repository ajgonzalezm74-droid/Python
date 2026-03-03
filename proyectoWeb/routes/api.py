from flask import Blueprint, jsonify
#from services.analisis_service import calcular_variacion
from services.analisis_service import calcular_variacion_rango


api = Blueprint("api", __name__)

@api.route("/api/variacion/<tipo>/<fecha_inicio>/<fecha_fin>")
def variacion(tipo, fecha_inicio, fecha_fin):
    resultado = calcular_variacion_rango(tipo, fecha_inicio, fecha_fin)
    return jsonify({"variacion": resultado})