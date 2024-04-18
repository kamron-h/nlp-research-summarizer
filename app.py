
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from flask import Flask, request, jsonify, render_template, session
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename
import redis
from uuid import uuid4
import openai

from redis.exceptions import RedisError
# from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pdfplumber


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('OPENAI_API_KEY')
model = SentenceTransformer('all-MiniLM-L6-v2')  # Load a pre-trained Sentence Transformer model

# Redis Configuration for session handling and data caching
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=os.getenv('REDIS_PORT', 6379),
        password=os.getenv('REDIS_PASSWORD'),
        ssl=os.getenv('REDIS_SSL', 'False').lower() in ['true', '1', 't'],
        decode_responses=True  # Automatically decode responses to Unicode, use it if you prefer not handling decoding manually
    )
except RedisError as e:
    print(f"Redis connection error: {e}")


@app.route('/')
def home():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('index.html', session_id=session_id)


@app.route('/assistant')
def chat_page():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('assistant.html', session_id=session_id)


@app.route('/team')
def team_page():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('team.html', session_id=session_id)


@app.route('/pricing')
def pricing_page():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('pricing.html', session_id=session_id)


@app.route('/login')
def login_page():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('login.html', session_id=session_id)


@app.route('/register')
def register_page():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('register.html', session_id=session_id)


# Initialize FAISS index
dimension = 384  # Adjust dimension size based on the model output
index = faiss.IndexFlatL2(dimension)


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    uploaded_files = request.files.getlist('pdf_files')
    if not uploaded_files:
        return jsonify({'message': 'No files uploaded'}), 400

    session_id = get_session_id()
    all_texts = []

    for uploaded_file in uploaded_files:
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join('temporary_pdfs', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            uploaded_file.save(file_path)

            text = extract_text_from_pdf(file_path)
            if text:
                all_texts.append(text)
            os.remove(file_path)  # Make sure file is deleted after reading

    combined_text = '\n'.join(all_texts)
    store_text_in_cache(combined_text, session_id)  # Store combined text in Redis
    return jsonify({'message': f'Processed {len(uploaded_files)} files', 'session_id': session_id})


def store_text_in_cache(text, session_id):
    try:
        # Ensure the session_id is a string and handle encoding within Redis
        success = redis_client.set(str(session_id), text)
        if success:
            print(f"Storing text for session_id: {session_id} - Storage successful")
        else:
            print(f"Storing text for session_id: {session_id} - Storage failed")
    except Exception as e:
        print(f"Error while storing text in cache for session_id {session_id}: {e}")


def get_text_from_cache(session_id):
    try:
        # Ensure the session_id is a string
        text = redis_client.get(str(session_id))
        if text:
            print(f"Retrieving text for session_id: {session_id} - Text retrieval successful")
            return text
        else:
            print(f"Retrieving text for session_id: {session_id} - No text found in cache")
            return None
    except Exception as e:
        print(f"Error retrieving text from cache for session_id {session_id}: {e}")
        return None


def ask_openai(question, context):
    """Ask a question to OpenAI using the provided context with the latest API method."""
    try:
        prompt = f"{context.strip()}\n\n###\n\n{question.strip()}"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['text'].strip()  # Extracting the text from the response
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "I'm unable to retrieve an answer at the moment."


@app.route('/answer_question', methods=['POST'])
def answer_question():
    session_id = request.args.get('session_id')
    question = request.json.get('question')
    if session_id is None:
        return jsonify({'message': 'Session ID is missing.'}), 400

    context = get_text_from_cache(session_id)  # Retrieve document context stored in Redis

    if context:
        answer = ask_openai(question, context)
        return jsonify({'answer': answer})
    else:
        return jsonify({'message': 'No document context available. Please upload a document first.'})


def extract_text_from_pdf(file_path):
    text = ""
    print(f"Reading PDF: {file_path}")
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                print(f"Extracting text from page {page.page_number}")
                page_text = page.extract_text()
                if page_text:
                    print(page_text[:100])  # Print first 100 characters of the extracted text
                    text += page_text + '\n'
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text


def get_session_id():
    """Generate or retrieve a unique session ID."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())
    return session['session_id']


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
