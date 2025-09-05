from flask import Flask, render_template_string, Response, request
import json
from main import generate_frames, set_cloak_color

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>🪄 Invisibility Cloak</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #1e3c72, #2a5298);
      color: white;
      text-align: center;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    h1 {
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
      animation: glow 2s infinite alternate;
    }

    h3 {
      margin-top: 2rem;
      font-weight: 500;
    }

    @keyframes glow {
      from { text-shadow: 0 0 5px #ff4b1f, 0 0 10px #ff9068; }
      to { text-shadow: 0 0 20px #ff9068, 0 0 30px #ff4b1f; }
    }

    form {
      background: rgba(255, 255, 255, 0.1);
      padding: 1rem 2rem;
      border-radius: 15px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 20px rgba(0,0,0,0.3);
      display: inline-block;
    }

    select, button {
      font-family: 'Poppins', sans-serif;
      font-size: 1rem;
      padding: 0.5rem 1rem;
      margin: 0.5rem;
      border-radius: 8px;
      border: none;
      outline: none;
      transition: 0.3s ease-in-out;
    }

    select {
      background: #fff;
      color: #333;
      cursor: pointer;
    }

    button {
      background: linear-gradient(45deg, #ff4b1f, #ff9068);
      color: white;
      font-weight: 600;
      cursor: pointer;
    }

    button:hover {
      transform: scale(1.05);
      box-shadow: 0 5px 15px rgba(255,144,104,0.6);
    }

    img {
      margin-top: 1.5rem;
      border-radius: 20px;
      border: 4px solid rgba(255,255,255,0.7);
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      max-width: 90%;
      height: auto;
    }
  </style>
</head>
<body>
  <h1>🪄 Invisibility Cloak</h1>
  <form method="POST" action="/set_color">
    <label for="color">Choose your cloak color:</label>
    <select name="color" id="color">
      <option value="red">❤️ Red</option>
      <option value="blue">💙 Blue</option>
      <option value="green">💚 Green</option>
    </select>
    <button type="submit">✨ Activate</button>
  </form>
  <h3>Live Cloak Effect</h3>
  <img src="{{ url_for('video_feed') }}" width="640" height="480">
</body>
</html>

"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/set_color", methods=["POST"])
def set_color():
    color = request.form["color"]
    set_cloak_color(color)  # update main.py color
    with open("color.json", "w") as f:
        json.dump({"color": color}, f)
    return render_template_string(HTML)

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)
