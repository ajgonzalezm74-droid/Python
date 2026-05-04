
from flask import Flask, render_template, jsonify
from exchange_provider import ExchangeProvider
import os

app = Flask(__name__)

# Crear una instancia del proveedor de tasas
exchange = ExchangeProvider()

@app.route('/')
def index():
    """Página principal - Calculadora"""
    return render_template('calculadora.html')

@app.route('/api/tasas')
def api_tasas():
    """Devuelve las tasas actuales directamente desde ExchangeProvider"""
    try:
        rates = exchange.get_all_rates()
        
        resultado = [
            {'tipo': 'bcv_usd', 'valor': rates.get('bcv_usd', 0)},
            {'tipo': 'bcv_eur', 'valor': rates.get('bcv_eur', 0)},
            {'tipo': 'p2p_ves', 'valor': rates.get('p2p_ves', 0)}
        ]
        
        print(f"📊 Tasas enviadas: {resultado}")  # Para debug
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Valores por defecto si falla
        return jsonify([
            {'tipo': 'bcv_usd', 'valor': 36.50},
            {'tipo': 'bcv_eur', 'valor': 39.20},
            {'tipo': 'p2p_ves', 'valor': 42.80}
        ])

@app.route('/api/actualizar-tasas')
def actualizar_tasas():
    """Forzar actualización y devolver tasas frescas"""
    try:
        rates = exchange.get_all_rates()
        return jsonify({
            'success': True,
            'rates': rates
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("🚀 Calculadora iniciada en http://localhost:" + str(port))
    app.run(debug=True, host='0.0.0.0', port=port)
