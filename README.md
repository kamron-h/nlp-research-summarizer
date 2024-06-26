

# NLP Research Assistant
#### LangChain, OpenAI, PgVector, and Flask NLP chatbot for academic literature review assistance.

## Description

* This is a Python based application that allows you to chat with a bot/model based on the input of multiple PDF documents. You can ask questions about the PDFs using natural language, and the application will provide relevant responses based on the content of the documents. Utilizing GPT-4 as large language model to generate accurate answers to your queries.


## How It Works

[//]: # (!PDF Research Assistant WebApp Diagram]&#40;./docs/PDF-LangChain.jpg&#41;)

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads multiple PDF documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.


## Installation

### Prerequisites

* Python 3.9 ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* pip (usually installed with Python)

### Steps

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/Vamp-ECU/nlp-research-summarizer]
    cd project-name
    ```


2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv env 
    source env/bin/activate
    ```
    
* If you're using Windows, the activation command is:
    
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**

     ```bash
    pip install -r requirements.txt
    ```
4.  **Set up the environment variables:**

    Create a `.env` file in the root directory of the project and add the following variables:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ```

    Replace `your_openai_api_key` with your OpenAI API key.

### Running the Application

1.  **Make sure your virtual environment is activated (if you created one).**

2.  **Start the Flask development server:**

    ```bash
    flask run
    ```

    * This typically starts the app at: http://127.0.0.1:5000/

### Usage

To use the MultiPDF Chat App, follow these steps:

* Open the provided URL (e.g.,  http://127.0.0.1:5000/) in your web browser.

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

2. Navigate to the Assistant page.

3. Load multiple PDF documents into the app by following the provided instructions.

4. Ask questions in natural language about the loaded PDFs using the chat interface.


### Important Points:

* **Security:** When using pickle, be aware that unpickling data can execute arbitrary code if the data is crafted by a malicious user. Only unpickle data you trust.
* **Redis Configuration:** The above example assumes Redis is running on localhost with the default port 6379. Adjust these settings as necessary.
* **Session Management:** We’re using Flask’s session.sid as the Redis key for storing each user’s vectorstore. Ensure your Flask session is securely configured.

## Contributing
This repository is intended for educational purposes and does not accept further contributions.
