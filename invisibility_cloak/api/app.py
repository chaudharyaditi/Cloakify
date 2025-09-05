from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

COLOR_FILE = "color.json"

def get_color():
    if os.path.exists(COLOR_FILE):
        with open(COLOR_FILE) as f:
            return json.load(f).get("color", "red")
    return "red"

def set_color(color):
    with open(COLOR_FILE, "w") as f:
        json.dump({"color": color}, f)

@app.route("/", methods=["GET"])
def index():
    color = get_color()
    return render_template("index.html", color=color)

@app.route("/set_color", methods=["POST"])
def set_cloak_color():
    color = request.form.get("color", "red")
    set_color(color)
    return jsonify({"status": "ok", "color": color})

# Vercel expects app callable named `app`
