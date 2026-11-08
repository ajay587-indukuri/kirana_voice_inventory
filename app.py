from flask import Flask, render_template, request, jsonify
from api import transcribe_audio, extract_order

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe():

    if "audio" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio = request.files["audio"]

    if audio.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        transcript = transcribe_audio(audio)

        return jsonify({
            "success": True,
            "transcript": transcript
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    if not data or not data.get("transcript"):
        return jsonify({
            "success": False,
            "error": "Transcript is missing"
        }), 400
    try:
        order = extract_order(data["transcript"])
        return jsonify({
            "success": True,
            "order": order
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
