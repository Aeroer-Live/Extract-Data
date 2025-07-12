from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parser import process_file

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    data = process_file(filepath)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)