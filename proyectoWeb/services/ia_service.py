import os
from openai import OpenAI
from models import HistorialTasa
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
#print("API KEY detectada:", os.getenv("OPENAI_API_KEY"))

if not api_key:
    print("❌ ERROR: No se encontró la API KEY")
else:
    print("✅ API KEY cargada correctamente")


def obtener_respuesta_ia(pregunta_usuario):

    try:

        client = OpenAI(api_key=api_key)

        registros = (
            HistorialTasa.query
            .order_by(HistorialTasa.fecha.desc())
            .limit(10)
            .all()
        )

        contexto_db = "Precios actuales:\n"

        for r in registros:
            contexto_db += f"{r.tipo}: {r.valor}\n"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Eres el asistente de AJG Solution. Usa estos datos: {contexto_db}"
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