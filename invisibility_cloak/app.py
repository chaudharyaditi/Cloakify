from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def get_color():
    try:
        with open("color.json") as f:
            return json.load(f).get("color", "red")
    except FileNotFoundError:
        return "red"

def set_color(color):
    with open("color.json", "w") as f:
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

if __name__ == "__main__":
    app.run(debug=True)
