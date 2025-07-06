from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader

import sys
try:
    # Initialize Ollama LLM with error handling
    llm = Ollama(model="llama3")  # or "mistral"
    
    # Test the connection
    llm("Test prompt to verify connection")
except Exception as e:
    print(f"Error connecting to Ollama: {str(e)}")
    print("Please make sure:")
    print("1. Ollama is installed (https://ollama.ai/)")
    print("2. You've pulled the model (e.g., 'ollama pull llama3')")
    print("3. The Ollama server is running (run 'ollama serve')")
    sys.exit(1)



def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "".join(page.extract_text() for page in reader.pages)

# Quiz Generation
def generate_quiz(text, question_type="mcq"):
    template = """
    Generate 3 {question_type} questions from this text:
    {text}

    Format:
    - Question: [question]
    - Options: A) [opt1], B) [opt2], C) [opt3], D) [opt4]
    - Correct Answer: [letter]
    """ if question_type == "mcq" else """
    Generate 3 true/false questions from:
    {text}

    Format:
    - Question: [question]
    - Correct Answer: True/False
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
        partial_variables={"question_type": question_type}
    )
    chain = prompt | llm
    return chain.invoke({"text": text})

# Answer Grading
def grade_answer(question, correct_answer, user_answer):
    grading_prompt = f"""
    Is the user's answer correct?
    Question: {question}
    Correct Answer: {correct_answer}
    User's Answer: {user_answer}

    Reply ONLY 'Correct' or 'Incorrect'.
    """
    return llm.invoke(grading_prompt)