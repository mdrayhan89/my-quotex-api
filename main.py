import os
import json
import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS
from quotexapi.stable_api import Quotex

app = Flask(__name__)
CORS(app)

# সেশন ফাইল ঠিক করার লজিক
session_file = "session.json"
if not os.path.exists(session_file) or os.stat(session_file).st_size == 0:
    with open(session_file, "w") as f:
        json.dump({}, f)

ASSETS = ["USDINR_otc", "XAUUSD_otc", "USDBDT_otc", "NZDUSD_otc"] # পেয়ারগুলো এখানে দিন
live_data = {}

def start_quotex():
    # Render-এর Environment Variables থেকে ডাটা নেবে
    email = os.environ.get("trrayhanislam786@gmail.com")
    password = os.environ.get("Mdrayhan@655")
    
    if not email or not password:
        print("Error: EMAIL or PASSWORD environment variables not set!")
        return

    api = Quotex(email=email, password=password)
    print("Connecting to Quotex on Render...")
    
    check, reason = api.connect()
    
    if check:
        print("Successfully Connected!")
        while True:
            for asset in ASSETS:
                try:
                    data = api.get_realtime_candles(asset)
                    if data:
                        live_data[asset] = data
                except:
                    continue
            time.sleep(1)
    else:
        print(f"Failed to connect: {reason}")

@app.route('/api/candles')
def get_candles():
    return jsonify(live_data)

if __name__ == '__main__':
    threading.Thread(target=start_quotex, daemon=True).start()
    # Render সাধারণত 10000 পোর্ট ব্যবহার করে, তাই এটি ডাইনামিক রাখা হয়েছে
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)