import pyBCV

bcv = pyBCV.Currency()
usd_rate = bcv.get_rate(currency_code='USD')

print(f"Tasa USD BCV: {usd_rate}")
