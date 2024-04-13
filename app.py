import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template


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
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    display_chat_messages(st.session_state.chat_history)


def display_chat_messages(messages):
    for msg_index, message in enumerate(messages):
        if msg_index % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main_page():
    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)


def about_page():
    st.title("About")
    st.markdown("""
    - **Project**: The PDF Chatbot, hosted by 'David' and integrated with Streamlit, revolutionizes the way users interact with PDF documents. This innovative web application allows users to upload multiple PDFs, which are then processed for content analysis. Once processed, users can engage in natural language conversations with 'David' to extract information, ask questions, or request summaries about the contents of the PDFs. Whether for research, studying, or information retrieval, the PDF Chatbot offers a user-friendly and efficient way to explore and extract insights from PDF documents.

    - **Developers**:
        - **Mehki Corpening**: Majoring in computer science and graduating in May. Have experience with Python, Java, HTML/CSS, and plan on using these skills to build create new projects.
        - **Robert Fernald**: A brief description about Team member 2, their role in the project, and any fun facts they'd like to share.
        - **Kamron Hopkins**: Passionate about creating user-friendly software, with skills in Swift, Java, Python, HTML5/CSS, and AI. Continuously learning new programming languages and tech stacks for personal projects and academic pursuits.
    """)



def home_page():
    st.title("Welcome to the PDF Chatbot, hosted by 'David'!")
    st.write("This is a Streamlit integrated web app that allows you to chat with 'David' about the contents of multiple PDF documents of your choice.")
    st.write("To get started, upload your PDF documents and click the 'Process' button. Once the processing is complete, you can ask 'David' questions about the contents of the PDFs.")
    st.write("You can navigate to the 'Streamlit Chatbot Page' to start chatting with 'David'...")
    st.write("You can also navigate to the 'About' page to learn more about the project and the developers involved.")
    st.write("Enjoy chatting with 'David'! :smiley:")
    st.image("david.png",)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Define pages in the main function
    pages = {
        "Home": home_page,
        "About": about_page,
        "Streamlit Chatbot Page": main_page
    }

    # Navigation menu at the top of the sidebar
    with st.sidebar:
        page = st.selectbox("Navigate", list(pages.keys()))

        # Add a custom "margin" (spacing) below the navigation
        st.markdown("<div style='margin-bottom: 7em;'></div>", unsafe_allow_html=True)

        # File uploader moved below the navigation menu
        pdf_docs = st.file_uploader("Upload your PDFs here", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Ready to chat!")
                else:
                    st.error("Please upload at least one PDF document.")

    # Call the page rendering function based on the user's selection
    pages[page]()


if __name__ == '__main__':
    main()
