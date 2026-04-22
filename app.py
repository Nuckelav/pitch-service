from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "API OK"

@app.route("/process-audio", methods=["POST"])
def process():
    return {"status": "python funcionando"}

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))