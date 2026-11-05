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

    def get_all_rates(self):
        """Este es el método que tu service.py está buscando"""
        bcv = self.get_bcv_rates()
        p2p = self.get_binance_p2p()
        return {
            "bcv_usd": bcv.get("USD", 0.0),
            "bcv_eur": bcv.get("EUR", 0.0),
            "p2p_ves": p2p
        }

    def get_bcv_rates(self):
        """
        Solución híbrida: USD desde API (automático) y EUR fijo (para evitar el fallo de la API).
        """
        rates = {"USD": 0.0, "EUR": 0.0}
        try:
            # 1. Obtener USD (desde DolarAPI, que sí está funcionando)
            resp_usd = self.session.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=10)
            if resp_usd.status_code == 200:
                rates["USD"] = float(resp_usd.json().get("promedio", 0.0))
            
            # 2. Obtener EUR (Fijado con el valor oficial del BCV para evitar el error 1.01)
            # Según la imagen del BCV del 05/11/2026, el Euro está en 1006.03263992
            rates["EUR"] = 1006.03
            
        except Exception as e:
            print(f"Error obteniendo tasas BCV: {e}")
            # Si la API del dólar falla, al menos aseguramos que el Euro no se rompa
            rates["EUR"] = 1006.03
            
        return rates

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
