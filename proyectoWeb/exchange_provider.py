import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_fixed
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ExchangeProvider:

    def __init__(self):

        print("ExchangeProvider cargado")

        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Cache profesional
        self.cache_bcv = TTLCache(maxsize=1, ttl=36000)
        self.cache_binance = TTLCache(maxsize=1, ttl=3600)

        self.bcv_url = "https://www.bcv.org.ve/"
        self.binance_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    # =====================================================
    # RETRY DECORATOR (MUY IMPORTANTE EN PRODUCCIÓN)
    # =====================================================

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def safe_request(self, method, url, **kwargs):

        response = requests.request(
            method,
            url,
            timeout=10,
            verify=False,
            **kwargs
        )

        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}")

        return response

    # =====================================================
    # BCV SCRAPER PROFESIONAL
    # =====================================================

    def get_bcv_rates(self):

        if "bcv" in self.cache_bcv:
            return self.cache_bcv["bcv"]

        rates = {"USD": 0.0, "EUR": 0.0}

        try:
            response = self.safe_request(
                "GET",
                self.bcv_url,
                headers=self.headers
            )

            soup = BeautifulSoup(response.text, "html.parser")

            mapping = {
                "dolar": "USD",
                "euro": "EUR"
            }

            for div_id, key in mapping.items():

                block = soup.find("div", id=div_id)

                if block:

                    strong = block.find("strong")

                    if strong:

                        try:
                            value = float(
                                strong.text.strip()
                                .replace(".", "")
                                .replace(",", ".")
                            )

                            # 🔥 Protección anti dato corrupto
                            if value > 0:
                                rates[key] = round(value, 2)

                        except ValueError:
                            pass

            self.cache_bcv["bcv"] = rates
            return rates

        except Exception as e:

            print("Error BCV:", e)
            return rates

    # =====================================================
    # BINANCE P2P PROFESIONAL
    # =====================================================

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

            response = self.safe_request(
                "POST",
                self.binance_url,
                json=payload,
                headers=self.headers
            )

            data = response.json()

            price = 0.0

            if data.get("data"):

                price = float(
                    data["data"][0]["adv"]["price"]
                )

            # Protección financiera
            if price > 0:
                price = round(price, 2)
                self.cache_binance["binance"] = price
                print("Precio Binance:", price)

            return price

        except Exception as e:

            print("Error Binance:", e)
            return 0.0

    # =====================================================
    # CONSOLIDADO
    # =====================================================

    def get_all_rates(self):

        bcv = self.get_bcv_rates()
        binance = self.get_binance_p2p()

        return {
            "bcv_usd": bcv.get("USD", 0.0),
            "bcv_eur": bcv.get("EUR", 0.0),
            "p2p_ves": binance
        }