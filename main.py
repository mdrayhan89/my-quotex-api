import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
from quotexapi.stable_api import Quotex

app = Flask(__name__)
CORS(app)

# আপনার ডিটেইলস
EMAIL = "trrayhanislam786@gmail.com"
PASSWORD = "Mdrayhana655"

client = Quotex(email=EMAIL, password=PASSWORD)

def connect_client():
    if not client.check_connect():
        print("Connecting to Quotex...")
        check, message = client.connect()
        if check:
            print("Login Successful!")
        else:
            print(f"Login Failed: {message}")
        return check
    return True

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Quotex API is running smoothly!"})

@app.route('/api/candles', methods=['GET'])
def get_all_candles():
    if not connect_client():
        return jsonify({"status": "error", "message": "Login failed"})
    
    asset_list = [
        "USDINR_otc", "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", 
        "AUDUSD_otc", "USDCAD_otc", "USDCHF_otc", "NZDUSD_otc",
        "EURGBP_otc", "EURJPY_otc", "GBPJPY_otc", "AUDJPY_otc",
        "EURAUD_otc", "EURCAD_otc", "GBPAUD_otc", "GBPCAD_otc",
        "AUDCAD_otc", "CADJPY_otc", "CHFJPY_otc", "AUDCHF_otc",
        "CADCHF_otc", "EURNZD_otc", "GBPNZD_otc", "AUDNZD_otc",
        "NZDJPY_otc", "NZDCAD_otc", "NZDCHF_otc"
    ]
    
    results = {}
    for asset in asset_list:
        try:
            candles = client.get_candles(asset, 60, 1, time.time())
            if candles:
                results[asset] = candles[-1]
        except:
            continue
    return jsonify({"status": "success", "data": results})

@app.route('/api/candles/<pair>', methods=['GET'])
def get_pair_candles(pair):
    if not connect_client():
        return jsonify({"status": "error", "message": "Login failed"})
    try:
        data = client.get_candles(pair, 60, 100, time.time())
        return jsonify({"status": "success", "pair": pair, "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
