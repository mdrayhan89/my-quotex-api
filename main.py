import os
import sys
import time
from flask import Flask, jsonify
from flask_cors import CORS

# আপনার ফোল্ডারটিকে পাইথন পাথে যুক্ত করা হচ্ছে
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    # আপনার লোকাল ফোল্ডার 'quotexapi' থেকে ইমপোর্ট করা হচ্ছে
    from quotexapi.stable_api import Quotex
    print("Local Quotex API loaded successfully!")
except Exception as e:
    print(f"Error loading local quotexapi: {e}")

app = Flask(__name__)
CORS(app)

# আপনার ডিটেইলস (স্ক্রিনশট অনুযায়ী)
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
    return jsonify({"status": "online", "message": "API is running from local folder"})

@app.route('/api/candles/<pair>', methods=['GET'])
def get_pair_candles(pair):
    if not connect_client():
        return jsonify({"status": "error", "message": "Login failed to Quotex"})
    try:
        # ১০০টি ক্যান্ডেল ডেটা
        data = client.get_candles(pair, 60, 100, time.time())
        return jsonify({"status": "success", "pair": pair, "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
