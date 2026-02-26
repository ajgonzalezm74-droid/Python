import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class AnalizadorBCV:
    def __init__(self):
        self.url_base = "https://www.bcv.org.ve"

    def consultar_rango(self, fecha_inicio, fecha_fin):
        """
        fecha_inicio y fecha_fin en formato 'DD-MM-YYYY'
        """
        inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
        fin = datetime.strptime(fecha_fin, "%d-%m-%Y")
        
        fechas_lista = []
        tasas_lista = []

        actual = inicio
        while actual <= fin:
            # Solo consultamos días de semana (Lunes a Viernes)
            if actual.weekday() < 5:
                dia_str = actual.strftime("%d/%m/%Y")
                tasa = self._extraer_tasa(dia_str)
                
                if isinstance(tasa, float):
                    fechas_lista.append(actual.strftime("%d-%b"))
                    tasas_lista.append(tasa)
            
            actual += timedelta(days=1)
        
        self._generar_grafico(fechas_lista, tasas_lista)

    def _extraer_tasa(self, fecha_str):
        # Simulación de la lógica de scraping por fecha del BCV
        # En producción, aquí iría el request filtrando por la fecha_str
        try:
            # Para el ejemplo, simulamos una pequeña variación para el gráfico
            import random
            return round(54.10 + random.uniform(-0.5, 0.5), 2)
        except:
            return None

    def _generar_grafico(self, fechas, tasas):
        plt.figure(figsize=(10, 6))
        
        # Estilo moderno: Barras con color degradado (simulado)
        barras = plt.bar(fechas, tasas, color='#4FC3F7', edgecolor='#0288D1', alpha=0.7)
        
        # Añadir etiquetas de valor sobre cada barra
        for barra in barras:
            yval = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2, yval + 0.01, yval, ha='center', va='bottom', fontsize=9)

        plt.title('Tendencia Tasa BCV (USD)', fontsize=14, fontweight='bold', color='#333')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Tasa (VES)', fontsize=12)
        plt.ylim(min(tasas) - 0.5, max(tasas) + 0.5) # Ajustar escala para ver mejor la variación
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        
        plt.tight_layout()
        plt.show()

# --- USO DEL CÓDIGO ---
analizador = AnalizadorBCV()
# Consultamos, por ejemplo, la primera semana de febrero
analizador.consultar_rango("02-02-2026", "10-02-2026")
