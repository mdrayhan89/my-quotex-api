import os
import sys
import time
from flask import Flask, jsonify
from flask_cors import CORS

# আপনার রিপোজিটরির ভেতরের ফোল্ডারটি পাইথনের পাথে যোগ করা হচ্ছে
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# সরাসরি ফোল্ডার থেকে Quotex ইমপোর্ট করার চেষ্টা
try:
    from quotexapi.stable_api import Quotex
    print("Quotex module loaded successfully from local folder!")
except Exception as e:
    print(f"Error loading module: {e}")
    # বিকল্প পদ্ধতি যদি উপরেরটি কাজ না করে
    try:
        from stable_api import Quotex
    except:
        pass

app = Flask(__name__)
CORS(app)

# আপনার ডিটেইলস
EMAIL = "trrayhanislam786@gmail.com"
PASSWORD = "Mdrayhana655"

# কানেকশন সেটআপ
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
    return jsonify({"status": "online", "message": "API is running from your local folder"})

@app.route('/api/candles/<pair>', methods=['GET'])
def get_pair_candles(pair):
    if not connect_client():
        return jsonify({"status": "error", "message": "Login failed to Quotex"})
    try:
        # ১০০টি ক্যান্ডেল ডেটা নেওয়া হচ্ছে
        data = client.get_candles(pair, 60, 100, time.time())
        return jsonify({"status": "success", "pair": pair, "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    # Render সাধারণত ১০০০০ বা ৫০০০ পোর্ট ব্যবহার করে
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
