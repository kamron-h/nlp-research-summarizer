from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        # Manually create a PdfReader instance
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  # Ensure there's text to add
                text += page_text
        # No need to explicitly close the PdfReader as it does not lock the file
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)


def handle_userinput(user_question):
    # TODO: Implement the handle_userinput function without using st.write
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    display_chat_messages(st.session_state.chat_history)


def display_chat_messages(messages):
    # TODO: Implement the display_chat_messages function withot using st.write
    for msg_index, message in enumerate(messages):
        if msg_index % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assistant')
def chat_page():
    return render_template('assistant.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        pdf_text = get_pdf_text([uploaded_file.filename])
        text_chunks = get_text_chunks(pdf_text)
        vectorstore = get_vectorstore(text_chunks)
        conversation_chain = get_conversation_chain(vectorstore)
        return jsonify({'message': 'PDF uploaded successfully!'})
    return jsonify({'message': 'No file uploaded!'})

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

@app.route('/get_response', methods=['POST'])
def get_response():
    user_question = request.form['question']
    response = process_question(user_question)  # Your chatbot logic here
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 