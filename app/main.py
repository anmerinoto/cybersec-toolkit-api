from flask import Flask, request, jsonify, send_file
import hashlib, base64, math, qrcode
from io import BytesIO

app = Flask(__name__)

@app.route("/api/v1/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/v1/hash", methods=["POST"])
def get_hash():
    data = request.json.get("data", "")
    hashed = hashlib.sha256(data.encode()).hexdigest()
    return jsonify({"input": data, "sha256": hashed})

@app.route("/api/v1/entropy", methods=["POST"])
def entropy():
    data = request.json.get("data", "")
    prob = [float(data.count(c)) / len(data) for c in dict.fromkeys(list(data))]
    entropy_value = - sum([p * math.log2(p) for p in prob])
    return jsonify({"input": data, "entropy": entropy_value})

@app.route("/api/v1/password/strength", methods=["POST"])
def password_strength():
    pwd = request.json.get("password", "")
    score = 0
    if len(pwd) >= 8: score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c in "!@#$%^&*()_+" for c in pwd): score += 1
    return jsonify({"password": pwd, "strength": score})

@app.route("/api/v1/qr", methods=["POST"])
def generate_qr():
    data = request.json.get("data", "")
    qr_img = qrcode.make(data)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/api/v1/base64", methods=["POST"])
def encode_base64():
    data = request.json.get("data", "")
    encoded = base64.b64encode(data.encode()).decode()
    return jsonify({"input": data, "base64": encoded})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
