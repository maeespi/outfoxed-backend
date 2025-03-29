from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return jsonify({"message": "OutFoxed backend is running!"})

if __name__ == "__main__":
    print("Starting OutFoxed API server...")
    app.run(debug=True)
    