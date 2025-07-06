from flask import Flask, request, jsonify
from quiz_utils import extract_text_from_pdf, generate_quiz
import os

app = Flask(__name__)

@app.route("/generate_quiz", methods=["POST"])
def api_generate_quiz():
    file = request.files["file"]
    num_questions = int(request.form.get("num_questions", 3))
    
    text = extract_text_from_pdf(file)
    quiz = generate_quiz(text, num_questions=num_questions)
    return jsonify({"quiz": quiz})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  # Changed from 5000 to 5001