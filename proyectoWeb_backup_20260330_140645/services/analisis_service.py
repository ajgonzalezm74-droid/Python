from models import HistorialTasa
from sqlalchemy import and_
from extensions import db
from datetime import datetime, timedelta

def obtener_historial_por_rango(tipo, fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")- timedelta(days=1)
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)    
    return HistorialTasa.query.filter(
        HistorialTasa.tipo == tipo,
        HistorialTasa.fecha.between(fecha_inicio, fecha_fin)
    ).order_by(HistorialTasa.fecha.asc()).all()



def calcular_variacion_rango(tipo, fecha_inicio, fecha_fin):

    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")- timedelta(days=1)
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)    

    registro_inicial = (
        HistorialTasa.query
        .filter(HistorialTasa.tipo == tipo)
        .filter(HistorialTasa.fecha >= fecha_inicio)
        .order_by(HistorialTasa.fecha.asc())
        .first()
    )

    registro_final = (
        HistorialTasa.query
        .filter(HistorialTasa.tipo == tipo)
        .filter(HistorialTasa.fecha <= fecha_fin)
        .order_by(HistorialTasa.fecha.desc())
        .first()
    )

    if not registro_inicial or not registro_final:
        return {
            "valor_inicial": 0,
            "valor_final": 0,
            "variacion": 0
        }

    valor_inicial = registro_inicial.valor
    valor_final = registro_final.valor

    variacion = ((valor_final - valor_inicial) / valor_inicial) * 100

    resultado = {
        "valor_inicial": valor_inicial,
        "valor_final": valor_final,
        "variacion": round(variacion, 2)
    }

    print("Variación calculada:", resultado)

    return resultado