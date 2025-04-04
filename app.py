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

    message = f"⏱️ Your {duration}-minute focus session has begun! I’m cheering you on — stay present, stay kind to yourself. 🦊✨"
    note = "While I can’t track the time or alert you when it ends (GPT isn’t great at time travel… yet), I’ll be right here when you return."
    suggestion = "When you’re done, say 'log my session' and I’ll record your progress!"
    tip = "Put your phone face-down — your future self will thank you. 💡📴"

    return jsonify({
        "message": message,
        "note": note,
        "suggestion": suggestion,
        "tip": tip,
        "duration": duration
    })

@app.route("/openapi.yaml", methods=["GET"])
def serve_openapi():
    return send_file("openapi.yaml", mimetype="application/yaml")

@app.route("/privacy-policy", methods=["GET"])
def privacy_policy():
    return """
    <h1>OutFoxed Privacy Policy</h1>
    <p>This is a student portfolio project. No personal data is stored or shared.</p>
    """
@app.route("/demo")
def demo_page():
    return """
    <html>
      <head>
        <title>OutFoxed Demo</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background-color: #fefcf8;
            color: #333;
            padding: 2rem;
          }
          h1 {
            color: #ff6b00;
          }
          button {
            background-color: #ff6b00;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 1rem;
            border-radius: 8px;
            cursor: pointer;
          }
          button:hover {
            background-color: #e35c00;
          }
          .response {
            margin-top: 1rem;
            padding: 1rem;
            background-color: #f0f0f0;
            border-radius: 6px;
            white-space: pre-wrap;
          }
          .links {
            margin-top: 2rem;
          }
          .links a {
            display: block;
            margin: 0.3rem 0;
            color: #007acc;
            text-decoration: none;
          }
        </style>
      </head>
      <body>
        <h1>🦊 OutFoxed API Demo</h1>
        <p>This is a live test of the Pomodoro timer action connected to ChatGPT.</p>

        <button onclick="startTimer()">Start 25-Minute Timer</button>
        <div class="response" id="result"></div>

        <div class="links">
          <h3>🔗 Related Links</h3>
          <a href="/openapi.yaml" target="_blank">📄 OpenAPI Spec</a>
          <a href="/privacy-policy" target="_blank">🔐 Privacy Policy</a>
          <a href="https://chat.openai.com/gpts" target="_blank">🧠 Launch OutFoxed GPT</a>
        </div>

        <script>
          function startTimer() {
            fetch('/start-timer', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ duration: 25 })
            })
            .then(response => response.json())
            .then(data => {
              document.getElementById('result').innerText = JSON.stringify(data, null, 2);
            })
            .catch(error => {
              document.getElementById('result').innerText = "Error: " + error;
            });
          }
        </script>
      </body>
    </html>
    """
@app.route("/log-session", methods=["POST"])
def log_session():
    data = request.get_json()
    summary = data.get("summary", "No summary provided.")
    mood = data.get("mood", "neutral")
    category = data.get("category", "general")

    message = (
        f"🎉 Session logged successfully!\n\n"
        f"You completed: “{summary}” under the **{category}** category.\n"
        f"Mood: *{mood}* — Nice work closing the loop! 🦊✅"
    )

    return jsonify({
        "message": message,
        "summary": summary,
        "mood": mood,
        "category": category
    })

# Temporary in-memory task list (restarts when server restarts)
tasks = []

@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title")
    category = data.get("category", "general")
    due_date = data.get("dueDate", None)

    if not title:
        return jsonify({"error": "Task title is required."}), 400

    task = {
        "title": title,
        "category": category,
        "dueDate": due_date
    }

    tasks.append(task)

    return jsonify({
        "message": f"📝 Task added: '{title}' under **{category}**.",
        "task": task
    })
@app.route("/get-tasks", methods=["GET"])
def get_tasks():
    category = request.args.get("category")

    if category:
        filtered_tasks = [task for task in tasks if task.get("category") == category]
        return jsonify({
            "message": f"📋 Tasks in category: {category}",
            "tasks": filtered_tasks
        })

    return jsonify({
        "message": "📋 All current tasks:",
        "tasks": tasks
    })
@app.route("/complete-task", methods=["POST"])
def complete_task():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Task title is required to complete it."}), 400

    for task in tasks:
        if task["title"].lower() == title.lower():
            tasks.remove(task)
            return jsonify({
                "message": f"✅ Task '{title}' marked as complete and removed from your list!"
            })

    return jsonify({
        "message": f"⚠️ Task '{title}' not found in your current list. Double-check the title?"
    }), 404

if __name__ == "__main__":
    print("Starting OutFoxed API server...")
    app.run(debug=True, host="0.0.0.0", port=10000)







