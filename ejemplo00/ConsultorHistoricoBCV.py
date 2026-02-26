import requests
from bs4 import BeautifulSoup
from datetime import datetime

class ConsultorBCV:
    def __init__(self):
        # URL del histórico de tipos de cambio del BCV
        self.url_base = "https://www.bcv.org.ve"

    def obtener_por_fecha(self, dia, mes, año):
        """
        Consulta la tasa de una fecha específica.
        Formato esperado: dia='05', mes='02', año='2026'
        """
        # El BCV permite filtrar por parámetros en la URL o navegar por su tabla
        # Para simplificar, esta función busca en la tabla de resultados
        params = {
            'field_fecha_valor_value[value][date]': f"{dia}/{mes}/{año}"
        }
        
        try:
            # Bypass de verificación SSL para portales gubernamentales
            response = requests.get(self.url_base, params=params, verify=False, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos la fila que coincida con la fecha en la tabla de resultados
            # El BCV organiza esto en tablas con clases específicas
            tabla = soup.find('table', {'class': 'views-table'})
            
            if not tabla:
                return f"No se encontraron registros para el {dia}/{mes}/{año}."

            # Extraemos el valor del Dólar (USD)
            # Nota: El índice de la columna puede variar según la actualización del sitio
            fila = tabla.find('tbody').find('tr')
            tasa_raw = fila.find('td', {'class': 'views-field-field-tasa-valor'}).text.strip()
            
            # Limpiamos y redondeamos
            tasa_final = round(float(tasa_raw.replace(',', '.')), 2)
            
            return f"Tasa BCV ({dia}/{mes}/{año}): {tasa_final:.2f} VES"

        except Exception as e:
            return f"Error al consultar la fecha: {e}"

# --- Ejemplo de uso ---
consultor = ConsultorBCV()
print(consultor.obtener_por_fecha('10', '02', '2026'))
