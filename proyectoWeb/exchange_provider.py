import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential
import urllib3
import random
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ExchangeProvider:
    def __init__(self):
        self.session = requests.Session()
        # Cache: BCV (6h), Binance (10 min) para no ser baneado
        self.cache = TTLCache(maxsize=20, ttl=21600) 
        self.last_valid_rates = {"USD": 0.0, "EUR": 0.0}
        
        self.bcv_url = "https://bcv.org.ve"
        self.binance_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def get_headers(self, is_binance=False):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        headers = {
            "User-Agent": ua,
            "Accept": "application/json" if is_binance else "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9",
        }
        if is_binance:
            headers.update({
                "Origin": "https://p2p.binance.com",
                "Referer": "https://binance.com",
                "Content-Type": "application/json"
            })
        return headers

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def safe_request(self, method, url, is_binance=False, **kwargs):
        # Timeouts largos son vitales para el BCV
        response = self.session.request(
            method, url, timeout=25, verify=False, 
            headers=self.get_headers(is_binance), **kwargs
        )
        response.raise_for_status()
        return response

    def get_bcv_rates(self):
        if "bcv" in self.cache: return self.cache["bcv"]

        try:
            # Plan A: Scraper Oficial
            resp = self.safe_request("GET", self.bcv_url)
            soup = BeautifulSoup(resp.text, "html.parser")
            rates = {}
            items = {"USD": "dolar", "EUR": "euro"}

            for code, element_id in items.items():
                container = soup.find("div", {"id": element_id})
                if container and container.find("strong"):
                    # Limpieza profunda de strings (quita puntos de miles y cambia coma por punto)
                    raw_val = container.find("strong").text.strip()
                    clean_val = raw_val.replace(".", "").replace(",", ".")
                    rates[code] = round(float(clean_val), 2)

            if rates.get("USD"):
                self.cache["bcv"] = rates
                self.last_valid_rates.update(rates)
                return rates
            raise ValueError("HTML no parseable")

        except Exception as e:
            print(f"⚠ BCV Principal falló: {e}. Intentando DolarApi...")
            # Plan B: API Espejo (DolarApi)
            try:
                res = requests.get("https://dolarapi.com", timeout=10)
                val = res.json().get("promedio")
                fallback = {"USD": float(val), "EUR": 0.0}
                self.cache["bcv"] = fallback
                return fallback
            except:
                return self.last_valid_rates

    def get_headers(self, is_binance=False):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        headers = {
            "User-Agent": ua,
            "Accept": "application/json" if is_binance else "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9",
        }
        if is_binance:
            headers.update({
                "Origin": "https://binance.com",
                "Referer": "https://binance.com",
                "Content-Type": "application/json",
                "clienttype": "web"  # <--- ESTO ES VITAL PARA QUE NO DE 0.0
            })
        return headers

    def get_binance_p2p(self):
        if "binance" in self.cache: return self.cache["binance"]

        # Configuración para tasa real de venta (lo que recibes en Bs)
        payload = {
            "asset": "USDT", 
            "fiat": "VES", 
            "merchantCheck": True,
            "page": 1, 
            "rows": 5, 
            "tradeType": "SELL", # SELL para ver a cuánto te compran tus USDT
            "publisherType": "merchant", 
            "payTypes": ["PagoMovil"] # Sin espacio
        }

        try:
            resp = self.safe_request("POST", self.binance_url, json=payload, is_binance=True)
            data = resp.json()
            
            if data.get("data") and len(data["data"]) > 0:
                # Extraemos el precio del primer anuncio verificado
                price = float(data["data"][0]["adv"]["price"])
                print(f"Binance P2P detectado: {price} VES")
                self.cache["binance"] = price
                return round(price, 2)
            else:
                print("⚠ Binance no retornó anuncios válidos.")
        except Exception as e:
            print(f"⚠ Binance falló: {e}")
        return 0.0
