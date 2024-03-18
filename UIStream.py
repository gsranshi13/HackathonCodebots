# import libraries
import streamlit as st
import requests
#from bs4 import BeautifulSoup
# from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
# from langchain.vectorstores import DocArrayInMemorySearch
from langchain_community.vectorstores import DocArrayInMemorySearch
import vertexai
from langchain_google_vertexai import VertexAI
# from langchain.llms import VertexAI
# from langchain.embeddings import VertexAIEmbeddings
# from langchain_community.embeddings import VertexAIEmbeddings
from langchain_google_vertexai import VertexAIEmbeddings

import os
import PyPDF2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/gurpreetsingh/Downloads/total-pad-417307-b8a7dfa5e743.json"

# vertexai.init(project="liquid-streamer-417216", location="us-west2")

llm = VertexAI(
    model_name="text-bison@001",
    max_output_tokens=256,
    temperature=0.1,
    top_p=0.8,
    top_k=40,
    verbose=True, )

embeddings = VertexAIEmbeddings()



def extract_text_from_pdf(input_file):
    pdf_reader = PyPDF2.PdfReader(input_file)
    text = ""
    with open("temp.txt", "w", encoding='utf-8') as file:
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            file.write(page.extract_text() + "\n")


@st.cache_resource
def create_langchain_index1(input_file):
    print("--indexing---")
    extract_text_from_pdf(input_file)
    loader = TextLoader("temp.txt", encoding='utf-8')
    # data = loader.load()

    index = VectorstoreIndexCreator(vectorstore_cls=DocArrayInMemorySearch, embedding=embeddings).from_loaders([loader])
    return index




# @st.cache_resource
# def get_basic_page_details(input_text,summary_query,tweet_query,ln_query):
#     index = create_langchain_index(input_text)
#     summary_response = index.query(summary_query)
#     tweet_response = index.query(tweet_query)
#     ln_response = index.query(ln_query)

#     return summary_response,tweet_response,ln_response


@st.cache_data
def get_response(input_text, query):
    print(f"--querying---{query}")
    response = index.query(query, llm=llm)
    return response


st.title('Question and Answering')

input_file = st.file_uploader("Provide the PDF", type=["pdf"])
print("Input File")
print(input_file)
summary_response = ""
tweet_response = ""
ln_response = ""
# if st.button("Load"):
if input_file:
    index = create_langchain_index1(input_file)
    summary_query = "Write a 100 words summary of the pdf"
    summary_response = get_response(input_file, summary_query)

    tweet_query = "Write a twitter tweet about pdf"
    tweet_response = get_response(input_file, tweet_query)

    ln_query = "Write a linkedin post for the pdf"
    ln_response = get_response(input_file, ln_query)

    with st.expander('Page Summary'):
        st.info(summary_response)

    with st.expander('Tweet'):
        st.info(tweet_response)

    with st.expander('LinkedIn Post'):
        st.info(ln_response)

st.session_state.input_text = ''
question = st.text_input("Ask a question from the PDF you shared...")
if st.button("Go"):
    if question:
        index = create_langchain_index1(input_file)
        response = get_response(input_file, question)
        st.write(response)
    else:
        st.warning("Please enter a question.")
