import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ExchangeProvider:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.cache_bcv = TTLCache(maxsize=1, ttl=1800)
        self.cache_binance = TTLCache(maxsize=1, ttl=3600)
        self.bcv_url = "https://www.bcv.org.ve/"
        self.binance_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    # -------------------------
    # BCV
    # -------------------------
    def get_bcv_rates(self):

        if "bcv" in self.cache_bcv:
            return self.cache_bcv["bcv"]

        rates = {"USD": 0.0, "EUR": 0.0}

        try:
            response = requests.get(
                self.bcv_url,
                headers=self.headers,
                timeout=10,
                verify=False
            )

            if response.status_code != 200:
                return rates

            soup = BeautifulSoup(response.text, "html.parser")

            dolar = soup.find("div", id="dolar")
            euro = soup.find("div", id="euro")

            if dolar:
                strong = dolar.find("strong")
                if strong:
                    valor = strong.text.strip().replace(".", "").replace(",", ".")
                    rates["USD"] = round(float(valor), 2)

            if euro:
                strong = euro.find("strong")
                if strong:
                    valor = strong.text.strip().replace(".", "").replace(",", ".")
                    rates["EUR"] = round(float(valor), 2)

            self.cache_bcv["bcv"] = rates
            return rates

        except Exception as e:
            print("Error BCV:", e)
            return rates

    # -------------------------
    # BINANCE
    # -------------------------
    def get_binance_p2p(self):

        if "binance" in self.cache_binance:
            return self.cache_binance["binance"]

        payload = {
            "asset": "USDT",
            "fiat": "VES",
            "merchantCheck": True,
            "page": 1,
            "rows": 1,
            "tradeType": "BUY",
            "publisherType": "merchant",
            "payTypes": ["PagoMovil"]
        }

        try:
            response = requests.post(
                self.binance_url,
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if response.status_code != 200:
                return 0.0

            data = response.json()

            if data.get("data"):
                price = round(float(data["data"][0]["adv"]["price"]), 2)
                self.cache_binance["binance"] = price
                print("Precio Binance:", price)
                return price
                print("Precio Binance:", price)
            return 0.0
            print("Error Binance: No data returned")
        except Exception as e:
            print("Error Binance:", e)
            return 0.0
    print("ExchangeProvider cargado")
    
    # -------------------------
    # CONSOLIDADO
    # -------------------------
    def get_all_rates(self):

        bcv = self.get_bcv_rates()
        binance = self.get_binance_p2p()

        return {
            "bcv_usd": bcv.get("USD", 0.0),
            "bcv_eur": bcv.get("EUR", 0.0),
            "p2p_ves": binance
        }
        
           