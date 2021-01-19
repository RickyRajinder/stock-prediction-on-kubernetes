import base64
import socket
from time import sleep

import pandas as pd
import redis

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NODE_ADDRESS = '127.0.0.1'
S3_SERVICE_NAME = 's3-service'
S3_SERVICE_PORT = 8080


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@app.route('/', methods=['GET', 'POST'])
def get_message():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":

        # Get data received from javascript
        data = request.get_json()

        df = pd.read_csv('companylist.csv')
        symbols = list(df.Symbol)
        symbol = str(data["days"]['name']).upper()
        days = data['days']['days']
        if symbol not in symbols:
            resp = {"message": "Please enter a valid NASDAQ stock ticker."}
            return jsonify(resp)
        elif not isInt(data['days']['days']):
            resp = {"message": "Please enter an integer for number of days."}
            return jsonify(resp)
        requestID = data['requestID']['randInt']
        sock = socket.socket()
        sock.connect((S3_SERVICE_NAME, S3_SERVICE_PORT))
        msg = requestID + "," + symbol + "," + days
        sock.send(msg.encode('ascii'))
        sock.close()
        r = redis.Redis(host=NODE_ADDRESS)
        price = r.get(symbol + "_price_" + requestID)
        while price is None:
            sleep(0.05)
            price = r.get(symbol + "_price_" + requestID)
        price = price.decode("ascii")
        graph = r.get(symbol + "_" + requestID)
        while price is None:
            sleep(0.05)
            graph = r.get(symbol + "_" + requestID)
        graph = base64.encodebytes(graph)
        resp = {"message": "The predicted price for " + symbol + " for " + days + " days from now is " + str(price),
                "graph": graph}

        print(data)

        return jsonify(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
