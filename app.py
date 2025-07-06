from flask import Flask, request, jsonify
from quiz_utils import extract_text_from_pdf, generate_quiz, grade_answer
import os

app = Flask(__name__)

@app.route("/generate_quiz", methods=["POST"])
def api_generate_quiz():
    file = request.files["file"]
    text = extract_text_from_pdf(file)
    quiz = generate_quiz(text)
    return jsonify({"quiz": quiz})

@app.route("/grade", methods=["POST"])
def api_grade():
    data = request.json
    result = grade_answer(
        question=data["question"],
        correct_answer=data["correct_answer"],
        user_answer=data["user_answer"]
    )
    return jsonify({"result": result.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)