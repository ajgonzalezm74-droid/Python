import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
import re

class ExchangeProvider:
    def __init__(self):
        self.session = requests.Session()
        self.cache = TTLCache(maxsize=20, ttl=600) # 10 min para pruebas
        self.bcv_url = "https://bcv.org.ve"
        #self.binance_url = "https://binance.com"
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
        try:
            resp = self.session.get(self.bcv_url, headers=self.get_headers(), timeout=20, verify=False)
            soup = BeautifulSoup(resp.text, "html.parser")
            rates = {}
            for code, e_id in [("USD", "dolar"), ("EUR", "euro")]:
                container = soup.find("div", {"id": e_id})
                if container and container.find("strong"):
                    val = container.find("strong").text.strip().replace(",", ".")
                    rates[code] = round(float(re.sub(r'[^\d.]', '', val)), 2)
            return rates
        except: return {"USD": 0.0, "EUR": 0.0}

    def get_binance_p2p(self):
        # Payload simplificado al máximo para evitar el error de JSON
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
