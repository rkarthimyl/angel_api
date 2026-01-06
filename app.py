from flask import Flask, request, jsonify
import pyotp
from SmartApi import SmartConnect
import angelOne
import symbolToken as Symbols
import requests
import pandas as pd

# ================= CONFIG =================
API_KEY = "Ox6PLQdO"
UID = "k119712"
PWD = "0607"
TOTP_KEY = "EOUHTBBYJ6IVDBSKKEA3YCE7VQ"

app = Flask(__name__)
smartApi = SmartConnect(API_KEY)

url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
data = requests.get(url).json()
df = pd.DataFrame(data)
df['strike'] = pd.to_numeric(df['strike'], errors='coerce').fillna(0).astype(int)
df['expiry'] = pd.to_datetime(df['expiry'], errors='coerce')
# ================= LOGIN (ONCE) =================
def login_once():

    totp = pyotp.TOTP(TOTP_KEY).now()
    data = smartApi.generateSession(UID, PWD, totp)

    if data['status'] == False:
        print(data)
    else:
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        feedToken = smartApi.getfeedToken()

        res = smartApi.getProfile(refreshToken)
        smartApi.generateToken(refreshToken)
        res=res['data']['exchanges']
        
    #data = requests.get(url).json()
    
    print("✅ Angel One logged in (in-memory token)")

# ================= API ENDPOINT =================
@app.route("/get-nifty-token", methods=["POST"])
def get_nifty_token():
    body = request.json
    strike = body.get("strike")

    if not strike:
        return jsonify({"error": "strike is required"})
    
    symbol, token, expiry = Symbols.get_nifty_token(df,strike)
    return jsonify({
        "symbol": symbol,
        "token": token,
        "expiry": expiry
    })

@app.route("/get-sensex-token", methods=["POST"])
def get_sensex_token():
    body = request.json
    strike = body.get("strike")

    if not strike:
        return jsonify({"error": "strike is required"})
    
    symbol, token, expiry = Symbols.get_sensex_token(df,strike)
    ltp = getLTP("BFO", symbol, token)
    return jsonify({
        "symbol": symbol,
        "token": token,
        "expiry": expiry,
        "ltp": ltp
    })


@app.route("/get-sensex-around", methods=["POST"])
def get_sensex_around():
    body = request.json
    strike = body.get("strike")

    if not strike:
        return jsonify({"error": "strike is required"})
    results = []
    num = int(strike[:-2])      # 84400
    opt = strike[-2:]           # "CE"
    num -= 600                  # add 100
    for i in range(10):
        num += 100
        new_strike = f"{num}{opt}"
        symbol, token, expiry = Symbols.get_sensex_token(df,new_strike)
        ltp = getLTP("BFO", symbol, token)
        results.append({
            "symbol": symbol,
            "token": token,
            "expiry": expiry,
            "ltp": ltp
        })

    return jsonify({
        "results": results
    })

def getLTP(exchange, tradingsymbol, symboltoken):
    ltp_data = smartApi.ltpData(
        exchange=exchange,
        tradingsymbol=tradingsymbol,
        symboltoken=symboltoken
    )
    return ltp_data['data']['ltp']  


@app.route("/place-order", methods=["POST"])
def place_order():
    body = request.json
    strike = body.get("strike")

    orderid = angelOne.place_Order(smartApi);
    
    return jsonify({
        "Status": orderid
    })

@app.route("/orders", methods=["POST"])
def orders():
    orders = smartApi.orderBook()
    data = orders['data']
    return jsonify({
        "orders": data
        
    })


@app.route("/open-position", methods=["POST"])
def open_position():
    positions = smartApi.position()
    open_positions = [
        p for p in positions['data']
        if int(p['netqty']) != 0
    ]
    data = open_positions
    return jsonify({
        "orders": data
        
    })


# ================= START =================
if __name__ == "__main__":
    login_once()   # 🔥 LOGIN ONLY ONCE
    app.run(debug=True, port=5000)
