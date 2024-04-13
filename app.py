import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from flask import Flask, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
import redis
import pickle
from uuid import uuid4
import openai

from redis.exceptions import RedisError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('OPENAI_API_KEY')


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
    return render_template('index.html')


@app.route('/assistant')
def chat_page():
    session_id = get_session_id()  # Assuming you have a function to retrieve or create a session ID
    return render_template('assistant.html', session_id=session_id)


@app.route('/team')
def team_page():
    return render_template('team.html')


@app.route('/pricing')
def pricing_page():
    return render_template('pricing.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


# @app.route('/upload_pdf', methods=['POST'])
# def upload_pdf():
#     uploaded_file = request.files.get('pdf_file')
#     if uploaded_file and uploaded_file.filename != '':
#         # Set the directory where files should be saved
#         save_directory = 'pdfs'
#         if not os.path.exists(save_directory):
#             os.makedirs(save_directory)
#
#         # Secure the filename and create the full path
#         filename = secure_filename(uploaded_file.filename)
#         file_path = os.path.join(save_directory, filename)
#
#         # Save the file to the specified directory
#         uploaded_file.save(file_path)
#
#         # After saving, you might want to process the PDF
#         pdf_text = get_pdf_text(file_path)
#         return jsonify({'message': 'PDF uploaded successfully!', 'pdf_text': pdf_text})
#     return jsonify({'message': 'No file uploaded!'})


def process_all_pdfs(directory_path):
    """Process all PDF files within the specified directory."""
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            try:
                pdf_text = get_pdf_text(file_path)
                session_id = get_session_id()  # Generate or retrieve session ID
                store_text_in_cache(pdf_text, session_id)  # Store the extracted text
                print(f"Processed {filename} successfully.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")


def get_pdf_text(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        pdf_reader = PdfReader(file_path)  # Open the PDF file
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text  # Append the text of each page to the text variable
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    # Retrieve list of files from the request
    uploaded_files = request.files.getlist('pdf_files')  # Adjust name according to your form

    if not uploaded_files:
        return jsonify({'message': 'No files uploaded'}), 400

    for uploaded_file in uploaded_files:
        # Check if the file is a PDF by checking its filename attribute
        if uploaded_file.filename.endswith('.pdf'):
            filename = secure_filename(uploaded_file.filename)
            unique_id = os.urandom(6).hex()  # Short unique ID
            filename = f"{unique_id}_{filename}"
            file_path = os.path.join('uploaded_pdfs', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            uploaded_file.save(file_path)

            try:
                pdf_text = get_pdf_text(file_path)
                session_id = get_session_id()
                store_text_in_cache(pdf_text, session_id)
                print(f"Uploaded and processed {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue  # Continue processing other files even if one fails

    # Return a response after all files are processed
    return render_template('assistant.html', message='All files uploaded and processed')


def store_text_in_cache(text, session_id):
    try:
        print(f"Storing text for session_id: {session_id}")
        # Ensure the session_id is a string and handle encoding within Redis
        success = redis_client.set(str(session_id), text)
        if success:
            print("Storage successful")
        else:
            print("Storage failed")
    except Exception as e:
        print(f"Error while storing text in cache: {e}")


def get_text_from_cache(session_id):
    try:
        print(f"Retrieving text for session_id: {session_id}")
        # Ensure the session_id is a string
        text = redis_client.get(str(session_id))
        if text:
            print("Text retrieval successful")
            return text
        else:
            print("No text found in cache")
            return None
    except Exception as e:
        print(f"Error retrieving text from cache: {e}")
        return None


@app.route('/answer_question', methods=['POST'])
def answer_question():
    session_id = request.args.get('session_id')
    question = request.json.get('question')
    if session_id is None:
        return jsonify({'message': 'Session ID is missing.'}), 400

    print(f"Question: {question}")
    print(f"Session ID: {session_id}")

    context = get_text_from_cache(session_id)
    if context:
        answer = ask_openai(question, context)
        return jsonify({'answer': answer})
    else:
        return jsonify({'message': 'No document context available. Please upload a document first.'})


def ask_openai(question, context):
    """Ask a question to OpenAI using the provided context with the chat completions endpoint."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the chat model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        # Extracting text from the first response choice
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "I'm unable to retrieve an answer at the moment."


def get_session_id():
    """Generate or retrieve a unique session ID."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())
    return session['session_id']


if __name__ == '__main__':
    app.run(debug=True)
