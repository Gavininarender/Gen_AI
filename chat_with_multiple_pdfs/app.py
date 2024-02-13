import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings 
from langchain.embeddings import HuggingFaceInstructEmbeddings  # free resource for embeddings 
from langchain.vectorstores import FAISS   # to store in our local disk and it runs locally 
from langchain.memory import ConversationBufferMemory  # storing chat history in memory 
from langchain.chains import ConversationalRetrievalChain  # allow to chat with our text, vector and having memory 
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import os



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf) # reading all pdf files

        for page in pdf_reader.pages: # reading all pages in pdf
            page = page.extract_text()
            text = text + page
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000, 
        chunk_overlap = 300,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks 


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()  # it takes more time to load vectors and it requires charges to pay 
    #embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")  # free of charges for embeddings 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question}) # it returns both (Q AND A) by pair, we need only answer
    st.session_state.chat_history = response['chat_history']  

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
def main():
    load_dotenv()
    st.set_page_config(page_title="You can Chat with Multiple PDFs file",
                       page_icon = r"D:\Generative_AI\multiple_pdfs_chat\abcd.jpeg")
    

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("You can Chat with Multiple PDFs :books:")
    user_question = st.text_input("Ask any question about your documents:")
    # Adding a "Submit" button
    if st.button("Submit"):
        if user_question:
            handle_userinput(user_question)


    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload Your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            
            with st.spinner("Loading....."):
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)  # all multiple 
                #st.write(raw_text)

                # get the text chunks 
                text_chunks = get_text_chunks(raw_text)
                #st.write(text_chunks)

                # create vectore store 
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                # st.session_state --> used to avoid run whole code when user run the code by multiple times 
                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.write("Completed Process")


if __name__ == "__main__":
    main()








