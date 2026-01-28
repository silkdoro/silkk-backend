from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

COINGECKO_API = 'https://api.coingecko.com/api/v3'

@app.route('/')
def home():
    return jsonify({'status': 'online', 'service': 'Silkk Intelligence API', 'version': '1.0'})

@app.route('/api/crypto')
def get_crypto():
    try:
        response = requests.get(
            f'{COINGECKO_API}/simple/price',
            params={
                'ids': 'bitcoin,ethereum,solana,monero,zcash',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'bitcoin': {
                    'price': data.get('bitcoin', {}).get('usd', 89133),
                    'change': data.get('bitcoin', {}).get('usd_24h_change', 0.66)
                },
                'ethereum': {
                    'price': data.get('ethereum', {}).get('usd', 2847),
                    'change': data.get('ethereum', {}).get('usd_24h_change', 1.23)
                },
                'solana': {
                    'price': data.get('solana', {}).get('usd', 148.32),
                    'change': data.get('solana', {}).get('usd_24h_change', 3.45)
                },
                'monero': {
                    'price': data.get('monero', {}).get('usd', 247.82),
                    'change': data.get('monero', {}).get('usd_24h_change', 4.67)
                },
                'zcash': {
                    'price': data.get('zcash', {}).get('usd', 68.43),
                    'change': data.get('zcash', {}).get('usd_24h_change', 3.21)
                }
            })
        else:
            return jsonify({'error': 'CoinGecko API failed', 'status': response.status_code}), 500
    except Exception as e:
        return jsonify({'error': str(e), 'type': 'exception'}), 500

@app.route('/api/stocks')
def get_stocks():
    return jsonify({
        'AAPL': {'price': 228.45, 'change': 1.10},
        'TSLA': {'price': 312.50, 'change': 1.85},
        'NVDA': {'price': 142.30, 'change': 2.15},
        'SPY': {'price': 698.15, 'change': 0.41}
    })

@app.route('/api/commodities')
def get_commodities():
    return jsonify({
        'gold': {'price': 5294, 'change': 2.18},
        'silver': {'price': 114.09, 'change': 2.09}
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
