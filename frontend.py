import streamlit as st
import requests

st.title("📝 Auto-Quiz Generator (Ollama)")

# PDF Upload
uploaded_file = st.file_uploader("Upload Textbook PDF", type="pdf")
if uploaded_file:
    if st.button("Generate Quiz"):
        response = requests.post(
            "http://localhost:5000/generate_quiz",
            files={"file": uploaded_file}
        ).json()
        quiz = response["quiz"]
        st.write("### Generated Quiz")
        st.text(quiz)

# Answer Grading
st.divider()
st.subheader("Grade Your Answer")
question = st.text_input("Question")
correct_answer = st.text_input("Correct Answer")
user_answer = st.text_input("Your Answer")

if st.button("Check Answer"):
    response = requests.post(
        "http://localhost:5000/grade",
        json={
            "question": question,
            "correct_answer": correct_answer,
            "user_answer": user_answer
        }
    ).json()
    st.success(f"Result: {response['result']}")