import os
import sys
import time
from flask import Flask, jsonify
from flask_cors import CORS

# আপনার রিপোজিটরির ফোল্ডারটি পাইথন পাথে যোগ করা হচ্ছে
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    # আপনার ফোল্ডার থেকে ইমপোর্ট
    from quotexapi.stable_api import Quotex
except Exception as e:
    print(f"Error importing local quotexapi: {e}")

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
    return jsonify({"status": "online", "message": "API running using local folder"})

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
