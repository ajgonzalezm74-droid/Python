import requests
from bs4 import BeautifulSoup
from datetime import datetime

def obtener_tasa_bcv(fecha_consulta):
    # Nota: El BCV usualmente muestra la tasa vigente. 
    # Para históricos específicos, la URL suele cambiar, pero esta consulta
    # sirve para verificar la información actual con la fecha que elijas registrar.
    url = "https://www.bcv.org.ve"
    
    try:
        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        dolar_contenedor = soup.find('div', id='dolar')
        euro_contenedor = soup.find('div', id='euro')
        
        if dolar_contenedor and euro_contenedor:
            tasa_usd = dolar_contenedor.find('strong').text.strip().replace(',', '.')
            tasa_eur = euro_contenedor.find('strong').text.strip().replace(',', '.')
            
            return {
                "fecha": fecha_consulta,
                "USD": round(float(tasa_usd), 2),
                "EUR": round(float(tasa_eur), 2)
            }
        else:
            return "No se encontraron los elementos. Es posible que el diseño del BCV haya cambiado."

    except Exception as e:
        return f"Error: {e}"

# --- Interacción con el usuario ---
fecha_user = input("📅 Ingresa la fecha de la tasa (DD/MM/AAAA): ")

# Validamos que sea una fecha real antes de proceder
try:
    datetime.strptime(fecha_user, "%d/%m/%Y")
    resultado = obtener_tasa_bcv(fecha_user)

    if isinstance(resultado, dict):
        print(f"\n✅ Tasas para el {resultado['fecha']}:")
        print(f"💵 Dólar: {resultado['USD']} VES")
        print(f"💶 Euro: {resultado['EUR']} VES")
    else:
        print(resultado)
except ValueError:
    print("❌ Formato de fecha inválido. Usa DD/MM/AAAA (ejemplo: 11/02/2026).")
