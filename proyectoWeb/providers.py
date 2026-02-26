import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache # TTL = Time To Live (Tiempo de vida)

class ExchangeProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        # Creamos una cache: máximo 1 item, que expire en 600 segundos (10 minutos)
        self.cache = TTLCache(maxsize=1, ttl=600)
        self.bcv_url = "https://www.bcv.org.ve/"
        self.binance_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def get_bcv_rates(self):
        rates = {"USD": 0.0, "EUR": 0.0}
        try:
            response = requests.get(self.bcv_url, verify=False, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for key, div_id in {"USD": "dolar", "EUR": "euro"}.items():
                div = soup.find("div", id=div_id)
                if div:
                    tag = div.find("strong")
                    if tag:
                        # Usamos get_text() para mayor claridad y seguridad
                        raw_value = tag.get_text(strip=True).replace(',', '.').replace(',', '.')
                        # El replace('.', '') arriba es por si el BCV usa puntos de miles (ej: 1.050,50)
                        rates[key] = round(float(raw_value), 2)
            return rates
        except Exception as e:
            print(f"Error parseando BCV: {e}")
            return rates

    def get_binance_p2p(self):
        # ... (mismo código de antes con tradeType: "BUY")
        payload = {
            "asset": "USDT", "fiat": "VES", "merchantCheck": True,
            "page": 1, "rows": 1, "tradeType": "BUY",
            "publisherType": "merchant", "payTypes": ["PagoMovil"]
        }
        try:
            res = requests.post(self.binance_url, json=payload, headers=self.headers, timeout=10)
            data = res.json()
            if data['success'] and data['data']:
                return round(float(data['data'][0]['adv']['price']), 2)
            return 0.0
        except: return 0.0

    def get_all_rates(self):
        """
        Este método ahora revisa si hay datos en la cache antes 
        de intentar hacer las peticiones de nuevo.
        """
        # Si las tasas ya están guardadas y no han expirado, las devuelve de una
        if "tasas" in self.cache:
            print("--- Cargando desde Cache ---")
            return self.cache["tasas"]

        # Si no están en cache, las busca en internet
        print("--- Buscando tasas nuevas en la Web ---")
        bcv = self.get_bcv_rates()
        tasas_frescas = {
            "bcv_usd": bcv["USD"],
            "bcv_eur": bcv["EUR"],
            "p2p_ves": self.get_binance_p2p()
        }
        
        # Guarda el resultado en la cache
        self.cache["tasas"] = tasas_frescas
        return tasas_frescas