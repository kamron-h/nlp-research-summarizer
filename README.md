# NLP Research Assistant
LangChain, OpenAI, and Streamlit NLP chatbot for academic literature review assistance.

## Introduction
------------
This is a Python based application that allows you to chat with a bot/model based on the input of multiple PDF documents. You can ask questions about the PDFs using natural language, and the application will provide relevant responses based on the content of the documents. Utilizing GPT-4 as large language model to generate accurate answers to your queries. 

### Please note that the app will only respond to questions related to the loaded PDFs.

### Python Version: 3.9 is required to run this application locally.

## How It Works
------------

[//]: # (!PDF Research Assistant WebApp Diagram]&#40;./docs/PDF-LangChain.jpg&#41;)

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads multiple PDF documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

## Dependencies and Installation
----------------------------
To install the PDF Research Assistant WebApp, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. Create a new file named `.env` in the project directory and add the following environment variables:
   ```
   OPENAI_API_KEY=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
   ```
    ### Replace the value of `OPENAI_API_KEY` with your OpenAI API key !!!


## Usage
-----
To use the PDF Research Assistant WebApp, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:
   ```
   streamlit run app.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load an individual PDF or either multiple PDF documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded PDFs using the chat interface.

## Contributing
------------
This repository is intended for educational purposes and does not accept further contributions. It serves as supporting material for a YouTube tutorial that demonstrates how to build this project. Feel free to utilize and enhance the app based on your own requirements.
