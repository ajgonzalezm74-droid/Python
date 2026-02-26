from flask import Flask, render_template
from flask import Flask, jsonify
from providers import ExchangeProvider # Importamos tu nueva clase

app = Flask(__name__)
provider = ExchangeProvider()  # instancia del proveedor




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/calculadora')
def calculadora():
    try:
        # 1. Llamamos a los métodos a través de la instancia 'provider'
        # provider.get_all_rates() ya consolida todo y maneja la cache
        tasas_raw = provider.get_all_rates() 

        # 2. Preparamos el diccionario exactamente como lo espera tu HTML
        # Asegúrate de usar los nombres que definiste en el método get_all_rates()
        return render_template('calculadora.html', tasas=tasas_raw)
        
    except Exception as e:
        print(f"Error en la ruta calculadora: {e}")
        # Retornamos valores en 0 para que la página no "explote" si algo falla
        tasas_error = {"bcv_usd": 0.0, "bcv_eur": 0.0, "p2p_ves": 0.0}
        return render_template('calculadora.html', tasas=tasas_error)

if __name__ == '__main__':
    app.run(debug=True)
