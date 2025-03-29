from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import send_file

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return jsonify({"message": "OutFoxed backend is running!"})

@app.route("/start-timer", methods=["POST"])
def start_timer():
    data = request.get_json()
    duration = data.get("duration", 25)

    message = f"Pomodoro timer started for {duration} minutes! 🦊⏳"

    return jsonify({
        "message": message,
        "duration": duration
    })
@app.route("/openapi.yaml", methods=["GET"])
def serve_openapi():
    return send_file("openapi.yaml", mimetype="text/yaml")

if __name__ == "__main__":
    print("Starting OutFoxed API server...")
app.run(debug=True, host="0.0.0.0", port=10000)





