from flask import Flask, render_template, jsonify, redirect, url_for, request
import os, json
from datetime import datetime
from ..agent import FoodMatchAgent

BASE = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(BASE, "logs", "logs.json")

app = Flask(__name__)

def load_assignments():
    if not os.path.exists(LOG_PATH):
        return []
    try:
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
            # sort newest first by timestamp if available
            def ts(a):
                try:
                    return datetime.fromisoformat(a.get("timestamp","").replace("Z",""))
                except Exception:
                    return datetime.min
            return sorted(data, key=ts, reverse=True)
    except Exception:
        return []

@app.route("/", methods=["GET"])
def index():
    assignments = load_assignments()
    total = len(assignments)
    return render_template("index.html", assignments=assignments, total=total)

@app.route("/api/assignments", methods=["GET"])
def api_assignments():
    return jsonify({
        "count": len(load_assignments()),
        "results": load_assignments()
    })

@app.route("/run", methods=["POST"])
def run_agent():
    agent = FoodMatchAgent()
    _ = agent.run("Run batch matching")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
    
if __name__ == "__main__":
    # Run on a separate port from ADK if you also use adk web
    app.run(host="127.0.0.1", port=5057, debug=False)
