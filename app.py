from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods= ['GET', 'POST'])
def get_message():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":

        # Get data received from javascript
        data = request.get_json()

        resp = {"message": "Your name is " + data["name"] }
       

        print(data)

        return jsonify(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)