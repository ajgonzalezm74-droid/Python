import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
import re

class ExchangeProvider:
    def __init__(self):
        self.session = requests.Session()
        self.cache = TTLCache(maxsize=20, ttl=600) # 10 min
        self.bcv_url = "https://bcv.org.ve"
        # Mantenemos tu URL de Binance intacta
        self.binance_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def get_headers(self, is_binance=False):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        headers = {"User-Agent": ua}
        if is_binance:
            headers.update({
                "Content-Type": "application/json",
                "clienttype": "web" # VITAL
            })
        return headers
    #------------------------------------------------------------------------------------
    def get_bcv_rates(self):
    """
    Obtiene las tasas de USD y EUR del BCV en una sola consulta.
    """
    rates = {"USD": 0.0, "EUR": 0.0}
    try:
        # Endpoint unificado: devuelve dólar oficial + euro oficial
        resp = self.session.get("https://ve.dolarapi.com/v1/cotizaciones", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Recorrer la lista, filtrar por fuente oficial
            for item in data:
                if item.get("fuente") == "oficial":
                    moneda = item.get("moneda")
                    promedio = float(item.get("promedio", 0.0))
                    if moneda == "USD":
                        rates["USD"] = promedio
                    elif moneda == "EUR":
                        rates["EUR"] = promedio
    except Exception as e:
        print(f"Error obteniendo tasas BCV: {e}")
    return rates

    
    # -----------------------------------------------------------------------------------
    def get_binance_p2p(self):
        # --- TU CÓDIGO DE BINANCE INTACTO ---
        payload = {
            "asset": "USDT", "fiat": "VES", "merchantCheck": True,
            "page": 1, "rows": 3, "tradeType": "SELL",
            "publisherType": "merchant", "payTypes": ["PagoMovil"]
        }
        try:
            resp = self.session.post(self.binance_url, json=payload, 
                                    headers=self.get_headers(True), timeout=15)
            data = resp.json()
            if data.get("data"):
                # Acceso correcto a la lista de anuncios
                return float(data["data"][0]["adv"]["price"])
        except Exception as e:
            print(f"Binance error: {e}")
        return 0.0
