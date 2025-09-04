from flask import Flask, render_template_string, request
import json

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
  <head><title>Cloak Color Picker</title></head>
  <body>
    <h2>Pick a cloak color</h2>
    <form method="POST">
      <select name="color">
        <option value="red">Red</option>
        <option value="blue">Blue</option>
        <option value="green">Green</option>
      </select>
      <button type="submit">Set Color</button>
    </form>
    <p>Current Color: {{ color }}</p>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    color = "red"
    if request.method == "POST":
        color = request.form["color"]
        # Save to file so main.py can read it
        with open("color.json", "w") as f:
            json.dump({"color": color}, f)
    else:
        try:
            with open("color.json") as f:
                color = json.load(f)["color"]
        except:
            pass
    return render_template_string(HTML, color=color)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

