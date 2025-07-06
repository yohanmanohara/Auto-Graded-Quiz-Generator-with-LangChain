from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import sys

try:
    # Initialize Ollama LLM with new package
    llm = OllamaLLM(model="llama3")
    
    # Test the connection using .invoke() instead of __call__
    llm.invoke("Test prompt to verify connection")
except Exception as e:
    print(f"Error connecting to Ollama: {str(e)}")
    print("Please make sure:")
    print("1. Ollama is installed (https://ollama.ai/)")
    print("2. You've pulled the model (e.g., 'ollama pull llama3')")
    print("3. The Ollama server is running (run 'ollama serve')")
    sys.exit(1)

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        return "".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

def generate_quiz(text, question_type="mcq", num_questions=3):
    template = f"""
    Generate {num_questions} {question_type} questions from this text:
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
    ...


    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
        partial_variables={"question_type": question_type}
    )
    chain = prompt | llm
    return chain.invoke({"text": text})

