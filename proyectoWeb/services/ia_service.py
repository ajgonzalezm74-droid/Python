from models import HistorialTasa
from extensions import db
import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


# --------------------------------------------------
# Parser inteligente financiero
# --------------------------------------------------

def parse_pregunta_financiera(texto):

    texto = texto.lower()

    tipo = None

    if "bcv" in texto and "usd" in texto:
        tipo = "bcv_usd"

    # Detectar fechas en la pregunta
    fechas = re.findall(r"\d{2}-\d{2}-\d{4}", texto)

    hoy = datetime.now().date()

    fecha_inicio = None
    fecha_fin = None

    # Manejo de palabras clave temporales
    if "hoy" in texto:
        fecha_inicio = hoy
        fecha_fin = hoy

    elif "ayer" in texto:
        fecha_inicio = hoy - timedelta(days=1)
        fecha_fin = fecha_inicio

    elif len(fechas) == 2:
        # Rango de fechas explícito
        fecha_inicio = datetime.strptime(fechas[0], "%d-%m-%Y").date()
        fecha_fin = datetime.strptime(fechas[1], "%d-%m-%Y").date()

    elif len(fechas) == 1:
        fecha_inicio = datetime.strptime(fechas[0], "%d-%m-%Y").date()
        fecha_fin = fecha_inicio

    return tipo, fecha_inicio, fecha_fin


# --------------------------------------------------
# IA Principal
# --------------------------------------------------

def obtener_respuesta_ia(pregunta_usuario):

    try:

        # 🔥 Parser inteligente
        tipo, fecha_inicio, fecha_fin = parse_pregunta_financiera(pregunta_usuario)

        # Si detecta intención financiera + fecha → consultar BD directo
        if tipo and fecha_inicio and fecha_fin:

            registros = HistorialTasa.query.filter(
                db.func.date(HistorialTasa.fecha) >= fecha_inicio,
                db.func.date(HistorialTasa.fecha) <= fecha_fin,
                HistorialTasa.tipo == tipo
            ).order_by(HistorialTasa.fecha.asc()).all()

            if registros:

                respuesta = "Datos encontrados:\n"

                for r in registros:
                    respuesta += f"{r.fecha.strftime('%d-%m-%Y')} - {r.valor}\n"

                return respuesta

            return "No encontré datos en ese rango."
        # --------------------------------------------------
        # Si no hay consulta específica → usar IA para redactar respuesta
        # --------------------------------------------------

        registros = (
            HistorialTasa.query
            .order_by(HistorialTasa.fecha.desc())
            .limit(10)
            .all()
        )

        contexto_db = "Últimas tasas registradas:\n"

        for r in registros:
            contexto_db += f"{r.fecha} - {r.tipo}: {r.valor}\n"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"""
Eres el asistente financiero de AJG Solution.

Usa únicamente los datos proporcionados.
Si no encuentras la información en los datos, responde que no está disponible.

Datos:
{contexto_db}
"""
                },
                {
                    "role": "user",
                    "content": pregunta_usuario
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        print("Error IA:", e)
        return "No pude procesar la solicitud."