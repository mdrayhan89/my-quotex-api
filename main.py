import os
import time
from flask import Flask, jsonify
from quotexpy import Quotex

app = Flask(__name__)

# সরাসরি আপনার ডিটেইলস এখানে বসিয়ে দেওয়া হলো
EMAIL = "trrayhanislam786@gmail.com"
PASSWORD = "Mdrayhana655"

# কোটেক্স কানেকশন সেটআপ
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
    return jsonify({"status": "online", "message": "Quotex API is running"})

@app.route('/api/candles', methods=['GET'])
def get_all_candles():
    if not connect_client():
        return jsonify({"status": "error", "message": "Could not connect to Quotex"})
    
    # আপনার সেই ২৭টি পেয়ারের লিস্ট
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
            # প্রতিটি পেয়ারের শেষ ক্যান্ডেল নেওয়া হচ্ছে
            candles = client.get_candles(asset, 60, 1, time.time())
            if candles:
                results[asset] = candles[-1]
        except:
            continue
            
    return jsonify({"status": "success", "data": results})

# নির্দিষ্ট পেয়ারের শেষ ১০০ ক্যান্ডেল দেখার জন্য নতুন রুট
@app.route('/api/candles/<pair>', methods=['GET'])
def get_pair_candles(pair):
    if not connect_client():
        return jsonify({"status": "error", "message": "Could not connect to Quotex"})
    
    try:
        # ১০০টি ক্যান্ডেল রিকোয়েস্ট
        data = client.get_candles(pair, 60, 100, time.time())
        return jsonify({"status": "success", "pair": pair, "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    # Render এর পোর্টের সাথে তাল মিলিয়ে রান করা
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
